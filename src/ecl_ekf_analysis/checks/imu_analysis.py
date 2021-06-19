# /usr/bin/env python3
"""
the imu analysis
"""
from typing import Dict

import numpy as np
from pyulog import ULog

import ecl_ekf_analysis.config.params as params
import ecl_ekf_analysis.config.thresholds as thresholds
from ecl_ekf_analysis.analysis.in_air_detector import InAirDetector
from ecl_ekf_analysis.check_data_interfaces.check_data import (
    CheckStatisticType,
    CheckType,
)
from ecl_ekf_analysis.checks.base_check import Check
from ecl_ekf_analysis.log_processing.analysis import (
    calculate_stat_from_signal,
    calculate_windowed_mean_per_airphase,
)
from ecl_ekf_analysis.log_processing.data_version_handling import (
    get_output_tracking_error_message,
)


class IMU_Bias_Check(Check):
    """
    the attitude check.
    """

    def __init__(self, ulog: ULog):
        """
        :param ulog:
        """
        super().__init__(ulog, check_type=CheckType.IMU_BIAS_STATUS)
        self._in_air_detector_no_ground_effects = InAirDetector(
            ulog,
            min_flight_time_seconds=params.iad_min_flight_duration_seconds(),
            in_air_margin_seconds=params.iad_in_air_margin_seconds(),
        )
        messages = {elem.name for elem in self.ulog.data_list}
        self._estimator_states_msg = (
            "estimator_states" if "estimator_states" in messages else "estimator_status"
        )

    def run_precondition(self) -> bool:
        """
        :return:
        """
        precondition: bool = True

        messages = {elem.name for elem in self.ulog.data_list}

        if "estimator_states" not in messages and "estimator_status" not in messages:
            precondition = False

        return precondition

    def calculate_metrics(self) -> Dict[str, list]:
        """
        calculates the estimator status metrics
        :return:
        """
        estimator_states_data = self.ulog.get_dataset(self._estimator_states_msg).data

        imu_metrics = dict()

        for signal in [
            "states[10]",
            "states[11]",
            "states[12]",
            "states[13]",
            "states[14]",
            "states[15]",
        ]:
            imu_metrics["{:s}_windowed_mean".format(signal)] = calculate_windowed_mean_per_airphase(
                estimator_states_data,
                self._estimator_states_msg,
                signal,
                self._in_air_detector_no_ground_effects,
                window_len_s=params.ecl_window_len_s(),
            )

        return imu_metrics

    def calc_statistics(self) -> None:
        """
        :return:
        """
        imu_metrics = self.calculate_metrics()
        estimator_states_data = self.ulog.get_dataset(self._estimator_states_msg).data

        # summarize biases from all six possible states
        imu_state_metrics = dict()
        for signal in [
            "states[10]",
            "states[11]",
            "states[12]",
            "states[13]",
            "states[14]",
            "states[15]",
        ]:
            imu_state_metrics["{:s}_windowed_mean".format(signal)] = float(
                max(
                    [np.max(phase) for _, phase in imu_metrics["{:s}_windowed_mean".format(signal)]]
                )
            )

        # delta angle bias windowed
        imu_delta_angle_bias_avg = self.add_statistic(
            CheckStatisticType.IMU_DELTA_ANGLE_BIAS_AVG, statistic_instance=0
        )

        imu_delta_angle_bias_avg.value = float(
            np.sqrt(
                np.sum(
                    [
                        np.square(
                            calculate_stat_from_signal(
                                estimator_states_data,
                                self._estimator_states_msg,
                                signal,
                                self._in_air_detector_no_ground_effects,
                                np.median,
                            )
                        )
                        for signal in ["states[10]", "states[11]", "states[12]"]
                    ]
                )
            )
        )
        imu_delta_angle_bias_avg.thresholds.warning = thresholds.imu_delta_angle_bias_warning_avg()

        # delta angle bias windowed
        imu_delta_angle_bias_windowed_avg = self.add_statistic(
            CheckStatisticType.IMU_DELTA_ANGLE_BIAS_WINDOWED_AVG, statistic_instance=0
        )

        imu_delta_angle_bias_windowed_avg.value = float(
            np.sqrt(
                np.sum(
                    [
                        np.square(imu_state_metrics[signal])
                        for signal in [
                            "states[10]_windowed_mean",
                            "states[11]_windowed_mean",
                            "states[12]_windowed_mean",
                        ]
                    ]
                )
            )
        )

        # delta velocity bias
        imu_delta_velocity_bias_avg = self.add_statistic(
            CheckStatisticType.IMU_DELTA_VELOCITY_BIAS_AVG, statistic_instance=0
        )

        imu_delta_velocity_bias_avg.value = float(
            np.sqrt(
                np.sum(
                    [
                        np.square(
                            calculate_stat_from_signal(
                                estimator_states_data,
                                self._estimator_states_msg,
                                signal,
                                self._in_air_detector_no_ground_effects,
                                np.median,
                            )
                        )
                        for signal in ["states[13]", "states[14]", "states[15]"]
                    ]
                )
            )
        )
        imu_delta_velocity_bias_avg.thresholds.warning = (
            thresholds.imu_delta_velocity_bias_warning_avg()
        )

        # delta velocity bias windowed
        imu_delta_velocity_bias_windowed_avg = self.add_statistic(
            CheckStatisticType.IMU_DELTA_VELOCITY_BIAS_WINDOWED_AVG,
            statistic_instance=0,
        )

        imu_delta_velocity_bias_windowed_avg.value = float(
            np.sqrt(
                np.sum(
                    [
                        np.square(imu_state_metrics[signal])
                        for signal in [
                            "states[13]_windowed_mean",
                            "states[14]_windowed_mean",
                            "states[15]_windowed_mean",
                        ]
                    ]
                )
            )
        )


class IMU_Output_Predictor_Check(Check):
    """
    the attitude check.
    """

    def __init__(self, ulog: ULog):
        """
        :param ulog:
        """
        super().__init__(ulog, check_type=CheckType.IMU_OUTPUT_PREDICTOR_STATUS)
        self._in_air_detector_no_ground_effects = InAirDetector(
            ulog,
            min_flight_time_seconds=params.iad_min_flight_duration_seconds(),
            in_air_margin_seconds=params.iad_in_air_margin_seconds(),
        )

    def calculate_metrics(self) -> Dict[str, list]:
        """
        calculates the estimator status metrics
        :return:
        """
        output_tracking_error_msg = get_output_tracking_error_message(self.ulog)
        output_tracking_error_data = self.ulog.get_dataset(output_tracking_error_msg).data

        imu_metrics = dict()

        # calculates the median of the output tracking error ekf innovations
        for signal, result in [
            ("output_tracking_error[0]", "output_obs_ang_err_median"),
            ("output_tracking_error[1]", "output_obs_vel_err_median"),
            ("output_tracking_error[2]", "output_obs_pos_err_median"),
        ]:
            # calculate a windowed version of the stat:
            # TODO: currently takes the mean instead of median
            imu_metrics["{:s}_windowed_mean".format(result)] = calculate_windowed_mean_per_airphase(
                output_tracking_error_data,
                output_tracking_error_msg,
                signal,
                self._in_air_detector_no_ground_effects,
                window_len_s=params.ecl_window_len_s(),
            )

        return imu_metrics

    def calc_statistics(self) -> None:
        """
        :return:
        """
        imu_metrics = self.calculate_metrics()

        output_tracking_error_msg = get_output_tracking_error_message(self.ulog)
        output_tracking_error_data = self.ulog.get_dataset(output_tracking_error_msg).data

        # observed angle error statistic average
        imu_observed_angle_error_avg = self.add_statistic(
            CheckStatisticType.IMU_OBSERVED_ANGLE_ERROR_AVG, statistic_instance=0
        )
        imu_observed_angle_error_avg.value = float(
            calculate_stat_from_signal(
                output_tracking_error_data,
                output_tracking_error_msg,
                "output_tracking_error[0]",
                self._in_air_detector_no_ground_effects,
                np.median,
            )
        )
        imu_observed_angle_error_avg.thresholds.warning = (
            thresholds.imu_observed_angle_error_warning_avg()
        )

        # observed angle error statistic average windowed
        imu_observed_angle_error_windowed_avg = self.add_statistic(
            CheckStatisticType.IMU_OBSERVED_ANGLE_ERROR_WINDOWED_AVG,
            statistic_instance=0,
        )

        imu_observed_angle_error_windowed_avg.value = float(
            max(
                [
                    metric.max()
                    for _, metric in imu_metrics["output_obs_ang_err_median_windowed_mean"]
                ]
            )
        )

        # observed velocity error statistic average
        imu_observed_velocity_error_avg = self.add_statistic(
            CheckStatisticType.IMU_OBSERVED_VELOCITY_ERROR_AVG, statistic_instance=0
        )
        imu_observed_velocity_error_avg.value = float(
            calculate_stat_from_signal(
                output_tracking_error_data,
                output_tracking_error_msg,
                "output_tracking_error[1]",
                self._in_air_detector_no_ground_effects,
                np.median,
            )
        )
        imu_observed_velocity_error_avg.thresholds.warning = (
            thresholds.imu_observed_velocity_error_warning_avg()
        )

        # observed velocity error statistic average windowed
        imu_observed_velocity_error_windowed_avg = self.add_statistic(
            CheckStatisticType.IMU_OBSERVED_VELOCITY_ERROR_WINDOWED_AVG,
            statistic_instance=0,
        )

        imu_observed_velocity_error_windowed_avg.value = float(
            max(
                [
                    metric.max()
                    for _, metric in imu_metrics["output_obs_vel_err_median_windowed_mean"]
                ]
            )
        )

        # observed position error statistic average
        imu_observed_position_error_avg = self.add_statistic(
            CheckStatisticType.IMU_OBSERVED_POSITION_ERROR_AVG, statistic_instance=0
        )
        imu_observed_position_error_avg.value = float(
            calculate_stat_from_signal(
                output_tracking_error_data,
                output_tracking_error_msg,
                "output_tracking_error[2]",
                self._in_air_detector_no_ground_effects,
                np.median,
            )
        )
        imu_observed_position_error_avg.thresholds.warning = (
            thresholds.imu_observed_position_error_warning_avg()
        )

        # observed position error statistic average windowed
        imu_observed_position_error_windowed_avg = self.add_statistic(
            CheckStatisticType.IMU_OBSERVED_POSITION_ERROR_WINDOWED_AVG,
            statistic_instance=0,
        )

        imu_observed_position_error_windowed_avg.value = float(
            max(
                [
                    metric.max()
                    for _, metric in imu_metrics["output_obs_pos_err_median_windowed_mean"]
                ]
            )
        )


class IMU_Vibration_Check(Check):
    """
    the attitude check.
    """

    def __init__(self, ulog: ULog):
        """
        :param ulog:
        """
        super().__init__(ulog, check_type=CheckType.IMU_VIBRATION_STATUS)
        self._in_air_detector_no_ground_effects = InAirDetector(
            ulog,
            min_flight_time_seconds=params.iad_min_flight_duration_seconds(),
            in_air_margin_seconds=params.iad_in_air_margin_seconds(),
        )

    def calculate_metrics(self) -> Dict[str, list]:
        """
        calculates the estimator status metrics
        :return:
        """
        estimator_status_data = self.ulog.get_dataset("estimator_status").data

        imu_metrics = dict()

        # calculates peak and mean for IMU vibration checks
        for signal, result in [
            ("vibe[0]", "imu_coning"),
            ("vibe[1]", "imu_hfdang"),
            ("vibe[2]", "imu_hfdvel"),
        ]:

            imu_metrics["{:s}_windowed_mean".format(result)] = calculate_windowed_mean_per_airphase(
                estimator_status_data,
                "estimator_status",
                signal,
                self._in_air_detector_no_ground_effects,
                window_len_s=params.ecl_window_len_s(),
            )

        return imu_metrics

    def calc_coning_statistics(self, imu_metrics: dict, estimator_status_data: dict) -> None:
        """
        calculates the statistics for the coning metric
        :param estimator_status_data:
        :return:
        """
        # max coning
        imu_coning_max = self.add_statistic(CheckStatisticType.IMU_CONING_MAX, statistic_instance=0)
        imu_coning_max.value = float(
            calculate_stat_from_signal(
                estimator_status_data,
                "estimator_status",
                "vibe[0]",
                self._in_air_detector_no_ground_effects,
                np.amax,
            )
        )
        imu_coning_max.thresholds.warning = thresholds.imu_coning_warning_max()

        # avg coning
        imu_coning_avg = self.add_statistic(CheckStatisticType.IMU_CONING_AVG, statistic_instance=0)
        imu_coning_avg.value = float(0.0)

        if imu_coning_max.value > 0.0:
            imu_coning_avg.value = float(
                calculate_stat_from_signal(
                    estimator_status_data,
                    "estimator_status",
                    "vibe[0]",
                    self._in_air_detector_no_ground_effects,
                    np.mean,
                )
            )

        # windowed avg coning
        imu_coning_windowed_avg = self.add_statistic(
            CheckStatisticType.IMU_CONING_WINDOWED_AVG, statistic_instance=0
        )
        imu_coning_windowed_avg.value = float(
            max([np.max(signal) for _, signal in imu_metrics["imu_coning_windowed_mean"]])
        )
        imu_coning_windowed_avg.thresholds.warning = thresholds.imu_coning_warning_rolling_avg()

    def calc_high_freq_delta_angle_statistics(
        self, imu_metrics: dict, estimator_status_data: dict
    ) -> None:
        """
        calculates the statistics for the high frequency delta angle metric
        :param estimator_status_data:
        :return:
        """
        # max high frequency delta angle
        imu_high_freq_delta_angle_max = self.add_statistic(
            CheckStatisticType.IMU_HIGH_FREQ_DELTA_ANGLE_MAX, statistic_instance=0
        )
        imu_high_freq_delta_angle_max.value = float(
            calculate_stat_from_signal(
                estimator_status_data,
                "estimator_status",
                "vibe[1]",
                self._in_air_detector_no_ground_effects,
                np.amax,
            )
        )
        imu_high_freq_delta_angle_max.thresholds.warning = (
            thresholds.imu_high_freq_delta_angle_warning_max()
        )

        # avg high frequency delta angle
        imu_high_freq_delta_angle_avg = self.add_statistic(
            CheckStatisticType.IMU_HIGH_FREQ_DELTA_ANGLE_AVG, statistic_instance=0
        )
        imu_high_freq_delta_angle_avg.value = float(0.0)

        if imu_high_freq_delta_angle_max.value > 0.0:
            imu_high_freq_delta_angle_avg.value = float(
                calculate_stat_from_signal(
                    estimator_status_data,
                    "estimator_status",
                    "vibe[1]",
                    self._in_air_detector_no_ground_effects,
                    np.mean,
                )
            )

        # windowed avg high frequency delta angle
        imu_high_freq_delta_angle_windowed_avg = self.add_statistic(
            CheckStatisticType.IMU_HIGH_FREQ_DELTA_ANGLE_WINDOWED_AVG,
            statistic_instance=0,
        )
        imu_high_freq_delta_angle_windowed_avg.value = float(
            max([np.max(signal) for _, signal in imu_metrics["imu_hfdang_windowed_mean"]])
        )
        imu_high_freq_delta_angle_windowed_avg.thresholds.warning = (
            thresholds.imu_high_freq_delta_angle_warning_rolling_avg()
        )

    def calc_high_freq_delta_velocity_statistics(
        self, imu_metrics: dict, estimator_status_data: dict
    ) -> None:
        """
        calculates the statistics for the high frequency delta velocity metric
        :param estimator_status_data:
        :return:
        """
        # max high frequency delta velocity
        imu_high_freq_delta_velocity_max = self.add_statistic(
            CheckStatisticType.IMU_HIGH_FREQ_DELTA_VELOCITY_MAX, statistic_instance=0
        )
        imu_high_freq_delta_velocity_max.value = float(
            calculate_stat_from_signal(
                estimator_status_data,
                "estimator_status",
                "vibe[2]",
                self._in_air_detector_no_ground_effects,
                np.amax,
            )
        )
        imu_high_freq_delta_velocity_max.thresholds.warning = (
            thresholds.imu_high_freq_delta_velocity_warning_max()
        )

        # avg high frequency delta velocity
        imu_high_freq_delta_velocity_avg = self.add_statistic(
            CheckStatisticType.IMU_HIGH_FREQ_DELTA_VELOCITY_AVG, statistic_instance=0
        )
        imu_high_freq_delta_velocity_avg.value = float(0.0)

        if imu_high_freq_delta_velocity_max.value > 0.0:
            imu_high_freq_delta_velocity_avg.value = float(
                calculate_stat_from_signal(
                    estimator_status_data,
                    "estimator_status",
                    "vibe[2]",
                    self._in_air_detector_no_ground_effects,
                    np.mean,
                )
            )

        # windowed avg high frequency delta velocity
        imu_high_freq_delta_velocity_windowed_avg = self.add_statistic(
            CheckStatisticType.IMU_HIGH_FREQ_DELTA_VELOCITY_WINDOWED_AVG,
            statistic_instance=0,
        )
        imu_high_freq_delta_velocity_windowed_avg.value = float(
            max([np.max(signal) for _, signal in imu_metrics["imu_hfdvel_windowed_mean"]])
        )
        imu_high_freq_delta_velocity_windowed_avg.thresholds.warning = (
            thresholds.imu_high_freq_delta_velocity_warning_rolling_avg()
        )

    def calc_statistics(self) -> None:
        """
        :return:
        """
        imu_metrics = self.calculate_metrics()
        estimator_status_data = self.ulog.get_dataset("estimator_status").data

        self.calc_coning_statistics(imu_metrics, estimator_status_data)
        self.calc_high_freq_delta_angle_statistics(imu_metrics, estimator_status_data)
        self.calc_high_freq_delta_velocity_statistics(imu_metrics, estimator_status_data)
