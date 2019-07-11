# /usr/bin/env python3
"""
the estimator analysis
"""
from typing import Dict, List, Optional

from pyulog import ULog
import numpy as np


from checks.base_check import Check
from grpc_interfaces.check_data_pb2 import CheckType
import grpc_interfaces.check_data_pb2 as check_data_api
from log_processing.analysis import calculate_windowed_mean_per_airphase, calculate_stat_from_signal
from analysis.in_air_detector import InAirDetector
import config.params as params
import config.thresholds as thresholds


class EstimatorCheck(Check):
    """
    the attitude check.
    """
    def __init__(
            self, ulog: ULog, innov_flags: Dict[str, float], control_mode_flags: Dict[str, float],
            check_type: CheckType = check_data_api.CHECK_TYPE_UNDEFINED, check_id: str = '',
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
        self._innov_fail_names = innov_fail_names
        if self._innov_fail_names is None:
            self._innov_fail_names = list()

        self._in_air_detector_no_ground_effects = InAirDetector(
            ulog, min_flight_time_seconds=params.iad_min_flight_duration_seconds(),
            in_air_margin_seconds=params.iad_in_air_margin_seconds())

        if check_id in ['magnetometer', 'height', 'yaw', 'optical_flow']:
            self._in_air_detector = self._in_air_detector_no_ground_effects
        else:
            self._in_air_detector = InAirDetector(
                ulog, min_flight_time_seconds=params.iad_min_flight_duration_seconds())


    def calc_estimator_status_metrics(self) -> Dict[str, list]:
        """
        calculates the estimator status metrics
        :return:
        """
        estimator_status_metrics = dict()

        estimator_status_data = self.ulog.get_dataset('estimator_status').data

        # add windowed metrics
        estimator_status_metrics['{:s}_percentage_red_windowed'.format(self._check_id)] = \
            calculate_windowed_mean_per_airphase(
                estimator_status_data, 'estimator_status', self._test_ratio_name,
                self._in_air_detector, threshold=params.ecl_red_thresh(),
                window_len_s=params.ecl_window_len_s())

        estimator_status_metrics['{:s}_percentage_amber_windowed'.format(self._check_id)] = \
            calculate_windowed_mean_per_airphase(
                estimator_status_data, 'estimator_status', self._test_ratio_name,
                self._in_air_detector, threshold=params.ecl_amb_thresh(),
                window_len_s=params.ecl_window_len_s())

        estimator_status_metrics['{:s}_test_windowed_mean'.format(self._check_id)] = \
            calculate_windowed_mean_per_airphase(
                estimator_status_data, 'estimator_status', self._test_ratio_name,
                self._in_air_detector, window_len_s=params.ecl_window_len_s())

        return estimator_status_metrics


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

        if self._test_ratio_name is None:
            return

        estimator_status_data = self.ulog.get_dataset('estimator_status').data
        estimator_status_metrics = self.calc_estimator_status_metrics()

        innov_red_pct = self.add_statistic(
            check_data_api.CHECK_STATISTIC_TYPE_ECL_INNOVATION_RED_PCT)
        innov_red_pct.value = float(calculate_stat_from_signal(
            estimator_status_data, 'estimator_status', self._test_ratio_name,
            self._in_air_detector, lambda x: 100.0 * np.mean(x > params.ecl_red_thresh())))

        #TODO: remove subtraction of innov_red_pct and tune parameters
        innov_amber_pct = self.add_statistic(
            check_data_api.CHECK_STATISTIC_TYPE_ECL_INNOVATION_AMBER_PCT)
        innov_amber_pct.value = float(calculate_stat_from_signal(
            estimator_status_data, 'estimator_status', self._test_ratio_name, self._in_air_detector,
            lambda x: 100.0 * np.mean(x > params.ecl_amb_thresh()))) - innov_red_pct.value
        innov_amber_pct.thresholds.warning.value = thresholds.ecl_amber_warning_pct(self._check_id)
        innov_amber_pct.thresholds.failure.value = thresholds.ecl_amber_failure_pct(self._check_id)

        innov_red_windowed_pct = self.add_statistic(
            check_data_api.CHECK_STATISTIC_TYPE_ECL_INNOVATION_RED_WINDOWED_PCT)
        innov_red_windowed_pct.value = float(max(
            [np.max(metric) for _, metric in estimator_status_metrics[
                '{:s}_percentage_red_windowed'.format(self._check_id)]]))

        innov_amber_windowed_pct = self.add_statistic(
            check_data_api.CHECK_STATISTIC_TYPE_ECL_INNOVATION_AMBER_WINDOWED_PCT)
        innov_amber_windowed_pct.value = float(max(
            [np.max(metric) for _, metric in estimator_status_metrics[
                '{:s}_percentage_amber_windowed'.format(self._check_id)]]))

        # the max and mean ratio of samples above / below std dev
        test_ratio_max = self.add_statistic(
            check_data_api.CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_MAX)
        test_ratio_max.value = float(calculate_stat_from_signal(
            estimator_status_data, 'estimator_status', self._test_ratio_name,
            self._in_air_detector, np.amax))

        test_ratio_avg = self.add_statistic(
            check_data_api.CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_AVG)
        test_ratio_avg.value = float(0.0)

        if test_ratio_max.value > 0.0:
            test_ratio_avg.value = float(calculate_stat_from_signal(
                estimator_status_data, 'estimator_status', self._test_ratio_name,
                self._in_air_detector, np.mean))

        test_ratio_windowed_avg = self.add_statistic(
            check_data_api.CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_WINDOWED_AVG)

        test_ratio_windowed_avg.value = float(max(
            [float(np.mean(metric)) for _, metric in estimator_status_metrics[
                '{:s}_test_windowed_mean'.format(self._check_id)]]
        ))


    def calc_innovation_statistics(self) -> None:
        """
        :return:
        """
        innovation_metrics = self.calc_innovation_metrics()

        for innov_fail_name in self._innov_fail_names:
            innov_stats_fail_pct = self.add_statistic(
                check_data_api.CHECK_STATISTIC_TYPE_ECL_FAIL_RATIO_PCT)

            innov_stats_fail_pct.value = float(calculate_stat_from_signal(
                self._innov_flags, 'estimator_status', innov_fail_name,
                self._in_air_detector_no_ground_effects, lambda x: 100.0 * np.mean(x > 0.5)))
            innov_stats_fail_pct.thresholds.failure.value = thresholds.ecl_innovation_failure_pct(
                self._check_id)

            innov_stats_fail_windowed_pct = self.add_statistic(
                check_data_api.CHECK_STATISTIC_TYPE_ECL_FAIL_RATIO_WINDOWED_PCT)

            innov_stats_fail_windowed_pct.value = float(max(
                [np.max(metric) for _, metric in innovation_metrics[
                    '{:s}_windowed_mean'.format(innov_fail_name)]]
            ))


    def calc_statistics(self) -> None:
        """
        :return:
        """
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
            check_type=check_data_api.CHECK_TYPE_ECL_MAGNETOMETER_STATUS,
            check_id='magnetometer', test_ratio_name='mag_test_ratio',
            innov_fail_names=['magx_innov_fail', 'magy_innov_fail', 'magz_innov_fail'])


    def run_precondition(self) -> None:
        """
        :return:
        """
        self._does_apply = np.amax(self._control_mode_flags['yaw_aligned']) > 0.5


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
        super(MagneticHeadingCheck, self).__init__(
            ulog, innov_flags, control_mode_flags,
            check_type=check_data_api.CHECK_TYPE_ECL_MAGNETIC_HEADING_STATUS,
            check_id='yaw', test_ratio_name=None, innov_fail_names=['yaw_innov_fail'])


    def run_precondition(self) -> None:
        """
        :return:
        """
        self._does_apply = np.amax(self._control_mode_flags['yaw_aligned']) > 0.5


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
            check_type=check_data_api.CHECK_TYPE_ECL_VELOCITY_SENSOR_STATUS,
            check_id='velocity', test_ratio_name='vel_test_ratio',
            innov_fail_names=['vel_innov_fail'])


    def run_precondition(self) -> None:
        """
        :return:
        """
        self._does_apply = np.amax(self._control_mode_flags['using_gps']) > 0.5


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
            check_type=check_data_api.CHECK_TYPE_ECL_POSITION_SENSOR_STATUS,
            check_id='position', test_ratio_name='pos_test_ratio',
            innov_fail_names=['posh_innov_fail'])


    def run_precondition(self) -> None:
        """
        :return:
        """
        self._does_apply = params.ecl_pos_checks_when_sensors_not_fused() or np.amax(
            self._control_mode_flags['using_gps']) > 0.5 or np.amax(
                self._control_mode_flags['using_evpos']) > 0.5


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
            check_type=check_data_api.CHECK_TYPE_ECL_HEIGHT_SENSOR_STATUS,
            check_id='height', test_ratio_name='hgt_test_ratio',
            innov_fail_names=['posv_innov_fail'])


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
            check_type=check_data_api.CHECK_TYPE_ECL_HEIGHT_ABOVE_GROUND_SENSOR_STATUS,
            check_id='height_above_ground', test_ratio_name='hagl_test_ratio',
            innov_fail_names=['hagl_innov_fail'])


    def run_precondition(self) -> None:
        """
        :return:
        """
        self._does_apply = np.amax(
            self.ulog.get_dataset('estimator_status').data['hagl_test_ratio']) > 0.0


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
            check_type=check_data_api.CHECK_TYPE_ECL_AIRSPEED_SENSOR_STATUS,
            check_id='airspeed', test_ratio_name='tas_test_ratio',
            innov_fail_names=['tas_innov_fail'])

    def run_precondition(self) -> None:
        """
        :return:
        """
        self._does_apply = np.amax(
            self.ulog.get_dataset('estimator_status').data['tas_test_ratio']) > 0.0


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
            check_type=check_data_api.CHECK_TYPE_ECL_SIDESLIP_SENSOR_STATUS,
            check_id='side_slip', test_ratio_name='beta_test_ratio',
            innov_fail_names=['sli_innov_fail'])

    def run_precondition(self) -> None:
        """
        :return:
        """
        self._does_apply = np.amax(
            self.ulog.get_dataset('estimator_status').data['beta_test_ratio']) > 0.0


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
            check_type=check_data_api.CHECK_TYPE_ECL_OPTICAL_FLOW_STATUS,
            check_id='optical_flow', test_ratio_name=None,
            innov_fail_names=['ofx_innov_fail', 'ofy_innov_fail'])


    def run_precondition(self) -> None:
        """
        :return:
        """
        self._does_apply = np.amax(self._control_mode_flags['using_optflow']) > 0.5
