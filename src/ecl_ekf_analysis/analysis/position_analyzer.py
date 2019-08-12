# /usr/bin/env/ python3
"""
a class for analyzing UAS position.
"""
from typing import List

import numpy as np
from pyulog import ULog
import intervals

from ecl_ekf_analysis.log_processing.custom_exceptions import PreconditionError
from ecl_ekf_analysis.signal_processing.flag_analysis import detect_flag_value_changes


class PositionAnalyzer():
    """
    this class is used for analyzing UAS position.
    """
    def __init__(self, ulog: ULog) -> None:
        """
        initializes a PositionAnalyzer instance.
        :param ulog:
        """

        self._ulog = ulog
        self._position_intervals = intervals.empty()
        self._vehicle_local_position = None

        try:
            self._vehicle_local_position = self._ulog.get_dataset('vehicle_local_position').data
        except:
            raise PreconditionError(
                'PositionAnalyzer: Could not find vehicle local position message.')

        self._position_intervals = intervals.closed(
            self._ulog.start_timestamp / 1.0e6, self._ulog.last_timestamp / 1.0e6)


    def _above_min_ground_distance_intervals(
            self, ground_distance_meters: float, phase_change_margin_seconds: float = 0.0,
            min_interval_duration_seconds: float = 0.0)  -> intervals.Interval:
        """
        :param ground_distance_meters:
        :return:
        """
        intervals_above_min_ground_distance = intervals.empty()
        if 'dist_bottom' not in self._vehicle_local_position:
            raise PreconditionError('Could not find dist_bottom in vehicle_local_position data.')

        timestamp = self._vehicle_local_position['timestamp']
        dist_bottom = self._vehicle_local_position['dist_bottom']
        if 'dist_bottom_valid' in self._vehicle_local_position:
            timestamp = timestamp[np.where(self._vehicle_local_position['dist_bottom_valid'])]
            dist_bottom = dist_bottom[np.where(self._vehicle_local_position['dist_bottom_valid'])]

        above_min_ground_distance = dist_bottom > ground_distance_meters

        interval_starts, interval_ends = detect_flag_value_changes(
            above_min_ground_distance.astype(int))

        for interval_start, interval_end in zip(interval_starts, interval_ends):
            if (timestamp[interval_end] / 1.0e6 - phase_change_margin_seconds) - \
                    (timestamp[interval_start] / 1.0e6 +
                     phase_change_margin_seconds) >= min_interval_duration_seconds:
                intervals_above_min_ground_distance = intervals_above_min_ground_distance | \
                        intervals.closed(
                            (timestamp[interval_start] - self._ulog.start_timestamp) / \
                            1.0e6 + phase_change_margin_seconds,
                            (timestamp[interval_end] - self._ulog.start_timestamp) / \
                            1.0e6 - phase_change_margin_seconds)

        if intervals_above_min_ground_distance.is_empty():
            print('PositionAnalyzer: flag was never activated.')

        return intervals_above_min_ground_distance


    def set_min_ground_distance(self, ground_distance_meters: float) -> None:
        """
        :param ground_distance_meters:
        :return:
        """
        self._position_intervals = self._above_min_ground_distance_intervals(
            ground_distance_meters, phase_change_margin_seconds=0.0,
            min_interval_duration_seconds=0.0) & self._position_intervals

    def get_valid_position(self, dataset: str, multi_instance: int = 0) -> list:
        """
        return all indices of the log file that are valid in position
        :param dataset:
        :return:
        """
        try:
            data = self._ulog.get_dataset(dataset, multi_instance=multi_instance).data
        except:
            raise PreconditionError('PositionAnalyzer: {:s} not found in log.'.format(dataset))

        valid_position_indices = []

        for interval in self._position_intervals:
            valid_position_indices.extend(
                np.where(
                    ((data['timestamp'] - self._ulog.start_timestamp) / 1.0e6 >=
                     interval.lower) & ((data['timestamp'] - self._ulog.start_timestamp) /
                                        1.0e6 < interval.upper))[0])

        return valid_position_indices


    def get_position_intervals(self, dataset: str, multi_instance: int = 0) -> List[list]:
        """
        return all intervals of the log file that are valid in position
        :param dataset:
        :param multi_instance:
        :return:
        """
        try:
            data = self._ulog.get_dataset(dataset, multi_instance=multi_instance).data
        except:
            raise PreconditionError('PositionAnalyzer: {:s} not found in log.'.format(dataset))

        position_intervals = []

        for interval in self._position_intervals:
            position_intervals.append(
                np.where(((data['timestamp'] - self._ulog.start_timestamp) / 1.0e6 >=
                          interval.lower) &
                         ((data['timestamp'] - self._ulog.start_timestamp) /
                          1.0e6 < interval.upper))[0])

        return position_intervals
