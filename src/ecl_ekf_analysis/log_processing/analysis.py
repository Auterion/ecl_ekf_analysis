#! /usr/bin/env python3
"""
function collection for calculation ecl ekf metrics.
"""
from typing import Dict, Callable, Tuple, List, Optional

import numpy as np

from ecl_ekf_analysis.analysis.in_air_detector import InAirDetector, Airtime
from ecl_ekf_analysis.signal_processing.smooth_filt_rolling import smooth_1d_boundaries


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
