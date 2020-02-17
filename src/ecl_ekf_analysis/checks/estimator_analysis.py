# /usr/bin/env python3
"""
the estimator analysis
"""
from typing import Dict, List, Optional

from pyulog import ULog
import numpy as np

from ecl_ekf_analysis.checks.base_check import Check
from ecl_ekf_analysis.check_data_interfaces.check_data import CheckType, CheckStatisticType
from ecl_ekf_analysis.log_processing.analysis import calculate_windowed_mean_per_airphase, \
    calculate_stat_from_signal
from ecl_ekf_analysis.analysis.in_air_detector import InAirDetector
import ecl_ekf_analysis.config.params as params
import ecl_ekf_analysis.config.thresholds as thresholds
from ecl_ekf_analysis.log_processing.data_version_handling import \
    get_innovation_message_and_field_names


class EstimatorCheck(Check):
    """
    the attitude check.
    """
    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float], control_mode_flags: Dict[str, float],
            check_type: CheckType = CheckType.UNDEFINED, check_id: str = '',
            test_ratio_name: Optional[str] = '', innov_fail_names: Optional[List[str]] = None):
        """
        :param ulog:
        :param innov_flags:
        :param check_type:
        :param check_id:
        :param test_ratio_name:
        :param innov_fail_names:
        """
        super(EstimatorCheck, self).__init__(
            ulog, check_type=check_type)
        self._innov_flags = innov_flags
        self._control_mode_flags = control_mode_flags
        self._check_id = check_id
        self._test_ratio_name = test_ratio_name
        self._test_ratio_message, self._test_ratio_names = None, []

        self._innov_fail_names = innov_fail_names if innov_fail_names is not None else []

        self._in_air_detector_no_ground_effects = InAirDetector(
            ulog, min_flight_time_seconds=params.iad_min_flight_duration_seconds(),
            in_air_margin_seconds=params.iad_in_air_margin_seconds())

        if check_id in ['magnetometer', 'height', 'yaw', 'optical_flow']:
            self._in_air_detector = self._in_air_detector_no_ground_effects
        else:
            self._in_air_detector = InAirDetector(
                ulog, min_flight_time_seconds=params.iad_min_flight_duration_seconds())


    def init_test_ratio_message_and_names(self):
        """
        :return:
        """
        if self._test_ratio_name is not None:
            self._test_ratio_message, self._test_ratio_names = \
                get_innovation_message_and_field_names(
                    self.ulog, self._test_ratio_name, topic='innovation_test_ratio'
                )


    def calc_test_ratio_metrics(self, test_ratio_name: str) -> Dict[str, list]:
        """
        calculates the estimator status metrics
        :return:
        """
        test_ratio_metrics = dict()

        test_ratio_data = self.ulog.get_dataset(self._test_ratio_message).data

        # add windowed metrics
        test_ratio_metrics['{:s}_percentage_red_windowed'.format(self._check_id)] = \
            calculate_windowed_mean_per_airphase(
                test_ratio_data, self._test_ratio_message, test_ratio_name,
                self._in_air_detector, threshold=params.ecl_red_thresh(),
                window_len_s=params.ecl_window_len_s())

        test_ratio_metrics['{:s}_percentage_amber_windowed'.format(self._check_id)] = \
            calculate_windowed_mean_per_airphase(
                test_ratio_data, self._test_ratio_message, test_ratio_name,
                self._in_air_detector, threshold=params.ecl_amb_thresh(),
                window_len_s=params.ecl_window_len_s())

        test_ratio_metrics['{:s}_test_windowed_mean'.format(self._check_id)] = \
            calculate_windowed_mean_per_airphase(
                test_ratio_data, self._test_ratio_message, test_ratio_name,
                self._in_air_detector, window_len_s=params.ecl_window_len_s())

        return test_ratio_metrics


    def calc_innovation_metrics(self) -> Dict[str, list]:
        """
        calculates the innovation metrics
        :return:
        """
        innovation_metrics = dict()

        for innov_fail_name in self._innov_fail_names:
            innovation_metrics['{:s}_windowed_mean'.format(innov_fail_name)] = \
                calculate_windowed_mean_per_airphase(
                    self._innov_flags, 'estimator_status', innov_fail_name,
                    self._in_air_detector_no_ground_effects, threshold=0.5,
                    window_len_s=params.ecl_window_len_s())

        return innovation_metrics


    def calc_estimator_statistics(self) -> None:
        """
        :return:
        """
        for i, test_ratio_name in enumerate(self._test_ratio_names):
            test_ratio_metrics = self.calc_test_ratio_metrics(test_ratio_name)
            test_ratio_data = self.ulog.get_dataset(self._test_ratio_message).data

            innov_red_pct = self.add_statistic(
                CheckStatisticType.INNOVATION_RED_PCT, statistic_instance=i)
            innov_red_pct.value = float(calculate_stat_from_signal(
                test_ratio_data, self._test_ratio_message, test_ratio_name,
                self._in_air_detector, lambda x: 100.0 * np.mean(x > params.ecl_red_thresh())))

            #TODO: remove subtraction of innov_red_pct and tune parameters
            innov_amber_pct = self.add_statistic(
                CheckStatisticType.INNOVATION_AMBER_PCT, statistic_instance=i)
            innov_amber_pct.value = float(calculate_stat_from_signal(
                test_ratio_data, self._test_ratio_message, test_ratio_name, self._in_air_detector,
                lambda x: 100.0 * np.mean(x > params.ecl_amb_thresh()))) - innov_red_pct.value
            innov_amber_pct.thresholds.warning = thresholds.ecl_amber_warning_pct(self._check_id)
            innov_amber_pct.thresholds.failure = thresholds.ecl_amber_failure_pct(self._check_id)

            innov_red_windowed_pct = self.add_statistic(
                CheckStatisticType.INNOVATION_RED_WINDOWED_PCT, statistic_instance=i)
            innov_red_windowed_pct.value = float(max(
                [np.max(metric) for _, metric in test_ratio_metrics[
                    '{:s}_percentage_red_windowed'.format(self._check_id)]]))

            innov_amber_windowed_pct = self.add_statistic(
                CheckStatisticType.INNOVATION_AMBER_WINDOWED_PCT, statistic_instance=i)
            innov_amber_windowed_pct.value = float(max(
                [np.max(metric) for _, metric in test_ratio_metrics[
                    '{:s}_percentage_amber_windowed'.format(self._check_id)]]))

            # the max and mean ratio of samples above / below std dev
            test_ratio_max = self.add_statistic(
                CheckStatisticType.ESTIMATOR_FAILURE_MAX, statistic_instance=i)
            test_ratio_max.value = float(calculate_stat_from_signal(
                test_ratio_data, self._test_ratio_message, test_ratio_name,
                self._in_air_detector, np.amax))

            test_ratio_avg = self.add_statistic(
                CheckStatisticType.ESTIMATOR_FAILURE_AVG, statistic_instance=i)
            test_ratio_avg.value = float(0.0)

            if test_ratio_max.value > 0.0:
                test_ratio_avg.value = float(calculate_stat_from_signal(
                    test_ratio_data, self._test_ratio_message, test_ratio_name,
                    self._in_air_detector, np.mean))

            test_ratio_windowed_avg = self.add_statistic(
                CheckStatisticType.ESTIMATOR_FAILURE_WINDOWED_AVG, statistic_instance=i)

            test_ratio_windowed_avg.value = float(max(
                [float(np.mean(metric)) for _, metric in test_ratio_metrics[
                    '{:s}_test_windowed_mean'.format(self._check_id)]]
            ))


    def calc_innovation_statistics(self) -> None:
        """
        :return:
        """
        innovation_metrics = self.calc_innovation_metrics()

        for i, innov_fail_name in enumerate(self._innov_fail_names):
            innov_stats_fail_pct = self.add_statistic(
                CheckStatisticType.FAIL_RATIO_PCT, statistic_instance=i)

            innov_stats_fail_pct.value = float(calculate_stat_from_signal(
                self._innov_flags, 'estimator_status', innov_fail_name,
                self._in_air_detector_no_ground_effects, lambda x: 100.0 * np.mean(x > 0.5)))
            innov_stats_fail_pct.thresholds.failure = thresholds.ecl_innovation_failure_pct(
                self._check_id)

            innov_stats_fail_windowed_pct = self.add_statistic(
                CheckStatisticType.FAIL_RATIO_WINDOWED_PCT, statistic_instance=i)

            innov_stats_fail_windowed_pct.value = float(max(
                [np.max(metric) for _, metric in innovation_metrics[
                    '{:s}_windowed_mean'.format(innov_fail_name)]]
            ))


    def calc_statistics(self) -> None:
        """
        :return:
        """
        self.init_test_ratio_message_and_names()
        self.calc_estimator_statistics()
        self.calc_innovation_statistics()


class MagnetometerCheck(EstimatorCheck):
    """
    the compass check
    """
    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(MagnetometerCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.MAGNETOMETER_STATUS,
            check_id='magnetometer', test_ratio_name='mag_field',
            innov_fail_names=['magx_innov_fail', 'magy_innov_fail', 'magz_innov_fail'])


    def run_precondition(self) -> bool:
        """
        :return:
        """
        return np.amax(self._control_mode_flags['yaw_aligned']) > 0.5


class MagneticHeadingCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        messages = {elem.name for elem in ulog.data_list}
        test_ratio_name = 'heading' if 'estimator_innovation_test_ratios' in messages else None
        super(MagneticHeadingCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.MAGNETIC_HEADING_STATUS,
            check_id='yaw', test_ratio_name=test_ratio_name, innov_fail_names=['yaw_innov_fail'])


    def run_precondition(self) -> bool:
        """
        :return:
        """
        return np.amax(self._control_mode_flags['yaw_aligned']) > 0.5


class VelocityCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(VelocityCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.VELOCITY_SENSOR_STATUS,
            check_id='velocity', test_ratio_name='vel',
            innov_fail_names=['vel_innov_fail'])


    def run_precondition(self) -> bool:
        """
        :return:
        """
        return np.amax(self._control_mode_flags['using_gps']) > 0.5


class GPSVelocityCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(GPSVelocityCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.GPS_VELOCITY_STATUS,
            check_id='gps_velocity', test_ratio_name='gps_vel')


    def run_precondition(self) -> bool:
        """
        :return:
        """
        messages = {elem.name for elem in self.ulog.data_list}
        return 'estimator_innovations' in messages and \
               np.amax(self._control_mode_flags['using_gps']) > 0.5


class EVVelocityCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(EVVelocityCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.EXTERNAL_VISION_VELOCITY_STATUS,
            check_id='ev_velocity', test_ratio_name='ev_vel')


    def run_precondition(self) -> bool:
        """
        :return:
        """
        messages = {elem.name for elem in self.ulog.data_list}
        return 'estimator_innovations' in messages and \
               np.amax(self._control_mode_flags['ev_vel']) > 0.5


class PositionCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(PositionCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.POSITION_SENSOR_STATUS,
            check_id='position', test_ratio_name='pos',
            innov_fail_names=['posh_innov_fail'])


    def run_precondition(self) -> bool:
        """
        :return:
        """
        return params.ecl_pos_checks_when_sensors_not_fused() or np.amax(
            self._control_mode_flags['using_gps']) > 0.5 or np.amax(
                self._control_mode_flags['using_evpos']) > 0.5


class GPSPositionCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(GPSPositionCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.GPS_POSITION_STATUS,
            check_id='gps_position', test_ratio_name='gps_hpos')


    def run_precondition(self) -> bool:
        """
        :return:
        """
        messages = {elem.name for elem in self.ulog.data_list}
        return 'estimator_innovations' in messages and \
               np.amax(self._control_mode_flags['using_gps']) > 0.5


class EVPositionCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(EVPositionCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.EXTERNAL_VISION_POSITION_STATUS,
            check_id='ev_position', test_ratio_name='ev_hpos')


    def run_precondition(self) -> bool:
        """
        :return:
        """
        messages = {elem.name for elem in self.ulog.data_list}
        return 'estimator_innovations' in messages and \
               np.amax(self._control_mode_flags['using_evpos']) > 0.5


class HeightCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(HeightCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.HEIGHT_SENSOR_STATUS,
            check_id='height', test_ratio_name='hgt',
            innov_fail_names=['posv_innov_fail'])


class GPSHeightCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(GPSHeightCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.GPS_HEIGHT_STATUS,
            check_id='gps_height', test_ratio_name='gps_vpos')


    def run_precondition(self) -> bool:
        """
        :return:
        """
        messages = {elem.name for elem in self.ulog.data_list}
        return 'estimator_innovations' in messages and \
               np.amax(self._control_mode_flags['using_gpshgt']) > 0.5


class EVHeightCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(EVHeightCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.EXTERNAL_VISION_HEIGHT_STATUS,
            check_id='ev_height', test_ratio_name='ev_vpos')

    def run_precondition(self) -> bool:
        """
        :return:
        """
        messages = {elem.name for elem in self.ulog.data_list}
        return 'estimator_innovations' in messages and \
               np.amax(self._control_mode_flags['using_evhgt']) > 0.5


class BarometerHeightCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(BarometerHeightCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.BAROMETER_HEIGHT_STATUS,
            check_id='baro_height', test_ratio_name='baro_vpos')

    def run_precondition(self) -> bool:
        """
        :return:
        """
        messages = {elem.name for elem in self.ulog.data_list}
        return 'estimator_innovations' in messages and \
               np.amax(self._control_mode_flags['using_barohgt']) > 0.5


class RangeSensorHeightCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(RangeSensorHeightCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.RANGE_SENSOR_HEIGHT_STATUS,
            check_id='range_sensor_height', test_ratio_name='rng_vpos')

    def run_precondition(self) -> bool:
        """
        :return:
        """
        messages = {elem.name for elem in self.ulog.data_list}
        return 'estimator_innovations' in messages and \
               np.amax(self._control_mode_flags['using_rnghgt']) > 0.5


class HeightAboveGroundCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(HeightAboveGroundCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.HEIGHT_ABOVE_GROUND_SENSOR_STATUS,
            check_id='height_above_ground', test_ratio_name='hagl',
            innov_fail_names=['hagl_innov_fail'])


    def run_precondition(self) -> bool:
        """
        :return:
        """
        test_ratio_msg, test_ratio_field_names = get_innovation_message_and_field_names(
            self.ulog, 'hagl', topic='innovation_test_ratio')
        return np.amax(
            self.ulog.get_dataset(test_ratio_msg).data[test_ratio_field_names[0]]) > 0.0


class AirspeedCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(AirspeedCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.AIRSPEED_SENSOR_STATUS,
            check_id='airspeed', test_ratio_name='airspeed',
            innov_fail_names=['tas_innov_fail'])

    def run_precondition(self) -> bool:
        """
        :return:
        """
        test_ratio_msg, test_ratio_field_names = get_innovation_message_and_field_names(
            self.ulog, 'airspeed', topic='innovation_test_ratio')
        return np.amax(
            self.ulog.get_dataset(test_ratio_msg).data[test_ratio_field_names[0]]) > 0.0


class SideSlipCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(SideSlipCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.SIDESLIP_SENSOR_STATUS,
            check_id='side_slip', test_ratio_name='beta',
            innov_fail_names=['sli_innov_fail'])

    def run_precondition(self) -> bool:
        """
        :return:
        """
        test_ratio_msg, test_ratio_field_names = get_innovation_message_and_field_names(
            self.ulog, 'beta', topic='innovation_test_ratio')
        return np.amax(
            self.ulog.get_dataset(test_ratio_msg).data[test_ratio_field_names[0]]) > 0.0


class OpticalFlowCheck(EstimatorCheck):
    """
    the compass check
    """

    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float],
            control_mode_flags: Dict[str, float]) -> None:
        """
        :param ulog:
        """
        super(OpticalFlowCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=CheckType.OPTICAL_FLOW_STATUS,
            check_id='optical_flow', test_ratio_name=None,
            innov_fail_names=['ofx_innov_fail', 'ofy_innov_fail'])


    def run_precondition(self) -> bool:
        """
        :return:
        """
        return np.amax(self._control_mode_flags['using_optflow']) > 0.5
