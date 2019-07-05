#! /usr/bin/env python3
"""
function collection for calculation ecl ekf metrics.
"""

from typing import Dict, List, Tuple, Optional, Callable

from pyulog import ULog
import numpy as np

from analysis.in_air_detector import Airtime, InAirDetector
from signal_processing.smooth_filt_rolling import smooth_1d_boundaries

def calculate_ecl_ekf_metrics(
        ulog: ULog, innov_flags: Dict[str, float], innov_fail_checks: List[str],
        sensor_checks: List[str], in_air: InAirDetector, in_air_no_ground_effects: InAirDetector,
        red_thresh: float = 1.0, amb_thresh: float = 0.5, window_len_s: float = 30.0) -> \
        Tuple[dict, dict]:
    """
    calculate the ecl ekf metrics.
    :param ulog:
    :param innov_flags:
    :param innov_fail_checks:
    :param sensor_checks:
    :param in_air:
    :param in_air_no_ground_effects:
    :param red_thresh:
    :param amb_thresh:
    :return:
    """

    sensor_metrics_stats, sensor_metrics_signals = calculate_sensor_metrics(
        ulog, sensor_checks, in_air, in_air_no_ground_effects,
        red_thresh=red_thresh, amb_thresh=amb_thresh, window_len_s=window_len_s)

    innov_fail_metrics_stats, innov_fail_metrics_signals = calculate_innov_fail_metrics(
        innov_flags, innov_fail_checks, in_air, in_air_no_ground_effects, window_len_s=window_len_s)

    imu_metrics_stats, imu_metrics_signals = calculate_imu_metrics(
        ulog, in_air_no_ground_effects, window_len_s=window_len_s)

    estimator_status_data = ulog.get_dataset('estimator_status').data

    # Check for internal filter nummerical faults
    ekf_metrics_stats = {'filter_faults_max': float(
        np.amax(estimator_status_data['filter_fault_flags']))}
    # TODO - process these bitmask's when they have been properly documented in the uORB topic
    # estimator_status['health_flags']
    # estimator_status['timeout_flags']

    # combine the metrics
    combined_metrics_stats = dict()
    combined_metrics_stats.update(imu_metrics_stats)
    combined_metrics_stats.update(sensor_metrics_stats)
    combined_metrics_stats.update(innov_fail_metrics_stats)
    combined_metrics_stats.update(ekf_metrics_stats)

    combined_metrics_signals = dict()
    combined_metrics_signals.update(imu_metrics_signals)
    combined_metrics_signals.update(sensor_metrics_signals)
    combined_metrics_signals.update(innov_fail_metrics_signals)

    return combined_metrics_stats, combined_metrics_signals


def calculate_sensor_metrics(
        ulog: ULog, sensor_checks: List[str], in_air: InAirDetector,
        in_air_no_ground_effects: InAirDetector, red_thresh: float = 1.0,
        amb_thresh: float = 0.5, window_len_s: float = 30.0) -> \
        Tuple[Dict[str, float], Dict[str, Tuple]]:
    """
    calculate the sensor metrics over the whole flight and over windows.
    :param ulog:
    :param sensor_checks:
    :param in_air:
    :param in_air_no_ground_effects:
    :param red_thresh:
    :param amb_thresh:
    :param window_len_s:
    :return:
    """

    estimator_status_data = ulog.get_dataset('estimator_status').data

    sensor_metrics_stats = dict()
    sensor_metrics_signals = dict()

    # calculates peak, mean, percentage above 0.5 std, and percentage above std metrics for
    # estimator status variables
    for signal, result_id in [('hgt_test_ratio', 'hgt'),
                              ('mag_test_ratio', 'mag'),
                              ('vel_test_ratio', 'vel'),
                              ('pos_test_ratio', 'pos'),
                              ('tas_test_ratio', 'tas'),
                              ('hagl_test_ratio', 'hagl')]:

        # only run sensor checks, if they apply.
        if result_id in sensor_checks:

            if result_id in ('mag', 'hgt'):
                in_air_detector = in_air_no_ground_effects
            else:
                in_air_detector = in_air

            # the percentage of samples above / below std dev
            sensor_metrics_stats['{:s}_percentage_red'.format(result_id)] = \
                calculate_stat_from_signal(
                    estimator_status_data, 'estimator_status', signal, in_air_detector,
                    lambda x: 100.0 * np.mean(x > red_thresh))
            sensor_metrics_stats['{:s}_percentage_amber'.format(result_id)] = \
                calculate_stat_from_signal(
                    estimator_status_data, 'estimator_status', signal, in_air_detector,
                    lambda x: 100.0 * np.mean(x > amb_thresh)) - \
                sensor_metrics_stats['{:s}_percentage_red'.format(result_id)]

            # add windowed metrics
            sensor_metrics_signals['{:s}_percentage_red_windowed'.format(result_id)] = \
                calculate_windowed_mean_per_airphase(
                    estimator_status_data, 'estimator_status', signal, in_air_detector,
                    threshold=red_thresh, window_len_s=window_len_s)
            sensor_metrics_signals['{:s}_percentage_amber_windowed'.format(result_id)] = \
                calculate_windowed_mean_per_airphase(
                    estimator_status_data, 'estimator_status', signal, in_air_detector,
                    threshold=amb_thresh, window_len_s=window_len_s)

            sensor_metrics_stats['{:s}_percentage_red_windowed'.format(result_id)] = float(max(
                [np.max(signal) for _, signal in sensor_metrics_signals[
                    '{:s}_percentage_red_windowed'.format(result_id)]]
            ))
            sensor_metrics_stats['{:s}_percentage_amber_windowed'.format(result_id)] = float(max(
                [np.max(signal) for _, signal in sensor_metrics_signals[
                    '{:s}_percentage_amber_windowed'.format(result_id)]]
            ))

            # the peak and mean ratio of samples above / below std dev
            peak = calculate_stat_from_signal(
                estimator_status_data, 'estimator_status', signal, in_air_detector, np.amax)
            if peak > 0.0:
                sensor_metrics_stats['{:s}_test_max'.format(result_id)] = peak
                sensor_metrics_stats['{:s}_test_mean'.format(result_id)] = \
                    calculate_stat_from_signal(
                        estimator_status_data, 'estimator_status', signal, in_air_detector, np.mean)

            sensor_metrics_signals['{:s}_test_windowed_mean'.format(result_id)] = \
                calculate_windowed_mean_per_airphase(
                    estimator_status_data, 'estimator_status', signal, in_air_detector,
                    window_len_s=window_len_s)
            sensor_metrics_stats['{:s}_test_windowed_mean'.format(result_id)] = float(max(
                [float(np.max(signal)) for _, signal in sensor_metrics_signals[
                    '{:s}_test_windowed_mean'.format(result_id)]]
            ))

    return sensor_metrics_stats, sensor_metrics_signals


def calculate_innov_fail_metrics(
        innov_flags: dict, innov_fail_checks: List[str], in_air: InAirDetector,
        in_air_no_ground_effects: InAirDetector, window_len_s: float = 30.0) -> \
        Tuple[Dict[str, float], Dict[str, Tuple]]:
    """
    :param innov_flags:
    :param innov_fail_checks:
    :param in_air:
    :param in_air_no_ground_effects:
    :return:
    """

    innov_fail_metrics_stats = dict()
    innov_fail_metrics_signals = dict()

    # calculate innovation check fail metrics
    for signal_id, signal, result in [('posv', 'posv_innov_fail', 'hgt_fail_percentage'),
                                      ('magx', 'magx_innov_fail', 'magx_fail_percentage'),
                                      ('magy', 'magy_innov_fail', 'magy_fail_percentage'),
                                      ('magz', 'magz_innov_fail', 'magz_fail_percentage'),
                                      ('yaw', 'yaw_innov_fail', 'yaw_fail_percentage'),
                                      ('vel', 'vel_innov_fail', 'vel_fail_percentage'),
                                      ('posh', 'posh_innov_fail', 'pos_fail_percentage'),
                                      ('tas', 'tas_innov_fail', 'tas_fail_percentage'),
                                      ('hagl', 'hagl_innov_fail', 'hagl_fail_percentage'),
                                      ('ofx', 'ofx_innov_fail', 'ofx_fail_percentage'),
                                      ('ofy', 'ofy_innov_fail', 'ofy_fail_percentage')]:

        # only run innov fail checks, if they apply.
        if signal_id in innov_fail_checks:

            if signal_id.startswith('mag') or signal_id == 'yaw' or signal_id == 'posv' or \
                signal_id.startswith('of'):
                in_air_detector = in_air_no_ground_effects
            else:
                in_air_detector = in_air

            innov_fail_metrics_stats[result] = calculate_stat_from_signal(
                innov_flags, 'estimator_status', signal, in_air_detector,
                lambda x: 100.0 * np.mean(x > 0.5))

            innov_fail_metrics_signals['{:s}_windowed_mean'.format(result)] = \
                calculate_windowed_mean_per_airphase(
                    innov_flags, 'estimator_status', signal, in_air_detector,
                    threshold=0.5, window_len_s=window_len_s)

            innov_fail_metrics_stats['{:s}_windowed_mean'.format(result)] = float(max(
                [np.max(signal) for _, signal in innov_fail_metrics_signals[
                    '{:s}_windowed_mean'.format(result)]]
            ))

    return innov_fail_metrics_stats, innov_fail_metrics_signals


def calculate_imu_metrics(
        ulog: ULog, in_air_no_ground_effects: InAirDetector, window_len_s: float = 30.0) -> \
        Tuple[Dict[str, float], Dict[str, Tuple]]:
    """
    calculate the imu metrics.
    :param ulog:
    :param in_air_no_ground_effects:
    :return:
    """

    ekf2_innovation_data = ulog.get_dataset('ekf2_innovations').data

    estimator_status_data = ulog.get_dataset('estimator_status').data

    imu_metrics_stats = dict()
    imu_metrics_signal = dict()

    # calculates the median of the output tracking error ekf innovations
    for signal, result in [('output_tracking_error[0]', 'output_obs_ang_err_median'),
                           ('output_tracking_error[1]', 'output_obs_vel_err_median'),
                           ('output_tracking_error[2]', 'output_obs_pos_err_median')]:
        imu_metrics_stats[result] = calculate_stat_from_signal(
            ekf2_innovation_data, 'ekf2_innovations', signal, in_air_no_ground_effects, np.median)

        # calculate a windowed version of the stat: TODO: currently takes the mean instead of median
        imu_metrics_signal['{:s}_windowed_mean'.format(result)] = \
            calculate_windowed_mean_per_airphase(
                ekf2_innovation_data, 'ekf2_innovations', signal, in_air_no_ground_effects,
                window_len_s=window_len_s)
        imu_metrics_stats['{:s}_windowed_mean'.format(result)] = float(max(
            [np.max(signal) for _, signal in imu_metrics_signal[
                '{:s}_windowed_mean'.format(result)]]
        ))

    # calculates peak and mean for IMU vibration checks
    for signal, result in [('vibe[0]', 'imu_coning'),
                           ('vibe[1]', 'imu_hfdang'),
                           ('vibe[2]', 'imu_hfdvel')]:
        peak = float(calculate_stat_from_signal(
            estimator_status_data, 'estimator_status', signal, in_air_no_ground_effects, np.amax))
        if peak > 0.0:
            imu_metrics_stats['{:s}_peak'.format(result)] = peak
            imu_metrics_stats['{:s}_mean'.format(result)] = float(calculate_stat_from_signal(
                estimator_status_data, 'estimator_status', signal,
                in_air_no_ground_effects, np.mean))

        # calculates a windowed version of the statistic
        imu_metrics_signal['{:s}_windowed_mean'.format(result)] = \
            calculate_windowed_mean_per_airphase(
                estimator_status_data, 'estimator_status', signal, in_air_no_ground_effects,
                window_len_s=window_len_s)
        imu_metrics_stats['{:s}_windowed_mean'.format(result)] = float(max(
            [np.max(signal) for _, signal in imu_metrics_signal[
                '{:s}_windowed_mean'.format(result)]]
        ))

    # IMU bias checks
    imu_metrics_stats['imu_dang_bias_median'] = float(
        np.sqrt(np.sum([np.square(calculate_stat_from_signal(
            estimator_status_data, 'estimator_status', signal,
            in_air_no_ground_effects, np.median)) for signal in
                        ['states[10]', 'states[11]', 'states[12]']])))

    imu_metrics_stats['imu_dvel_bias_median'] = float(
        np.sqrt(np.sum([np.square(calculate_stat_from_signal(
            estimator_status_data, 'estimator_status', signal,
            in_air_no_ground_effects, np.median)) for signal in
                        ['states[13]', 'states[14]', 'states[15]']])))

    # calculate a windowed version of the stat: TODO: currently takes the mean instead of median
    imu_state_metrics = dict()
    for signal in ['states[10]', 'states[11]', 'states[12]', 'states[13]',
                   'states[14]', 'states[15]']:
        imu_metrics_signal['{:s}_windowed_mean'.format(signal)] = \
            calculate_windowed_mean_per_airphase(
                estimator_status_data, 'estimator_status', signal, in_air_no_ground_effects,
                window_len_s=window_len_s)
        imu_state_metrics['{:s}_windowed_mean'.format(signal)] = float(
            max([np.max(phase) for _, phase in
                 imu_metrics_signal['{:s}_windowed_mean'.format(signal)]]
                ))
    imu_metrics_stats['imu_dang_bias_windowed_mean'] = float(
        np.sqrt(np.sum([np.square(imu_state_metrics[signal]) for signal in
                        ['states[10]_windowed_mean', 'states[11]_windowed_mean',
                         'states[12]_windowed_mean']])))
    imu_metrics_stats['imu_dvel_bias_windowed_mean'] = float(
        np.sqrt(np.sum([np.square(imu_state_metrics[signal]) for signal in
                        ['states[13]_windowed_mean', 'states[14]_windowed_mean',
                         'states[15]_windowed_mean']])))

    return imu_metrics_stats, imu_metrics_signal


def calculate_stat_from_signal(
        data: Dict[str, np.ndarray], dataset: str, variable: str,
        in_air_det: InAirDetector, stat_function: Callable) -> float:
    """
    :param data:
    :param variable:
    :param in_air_detector:
    :return:
    """

    return float(stat_function(data[variable][in_air_det.get_airtime(dataset)]))


def calculate_windowed_mean_per_airphase(
        data: Dict[str, np.ndarray], dataset: str, variable: str,
        in_air_det: InAirDetector, threshold: Optional[float] = None,
        window_len_s: float = 30.0) -> List[Tuple[Airtime, np.ndarray]]:
    """
    calculates a windowed mean for a thresholded signal. This is needs to be done per airphase,
    as otherwise ground effects might influcence the signal.
    :param data:
    :param variable:
    :param in_air_detector:
    :param stat_function:
    :param window_len_s:
    :return:
    """

    windowed_stats = []

    for airtime, at_indices in zip(in_air_det.airtimes, in_air_det.get_airtime_per_phase(dataset)):

        duration_s = airtime.landing - airtime.take_off
        window_len = int((window_len_s / duration_s) * len(at_indices))
        if (window_len % 2) == 0:
            window_len += 1

        window_len_after_s = duration_s * (window_len / float(len(at_indices)))

        input_signal = data[variable][at_indices]
        if threshold is not None:
            input_signal = 100.0 * (input_signal > threshold)

        smoothed_air_phase = smooth_1d_boundaries(
            input_signal, window_len=window_len, mode='valid', mean_for_short_signals=True)

        smoothed_airtime = Airtime(
            take_off=airtime.take_off + min(window_len_after_s, duration_s) / 2.0,
            landing=airtime.landing - min(window_len_after_s, duration_s) / 2.0)

        windowed_stats.append((smoothed_airtime, smoothed_air_phase))

    return windowed_stats
