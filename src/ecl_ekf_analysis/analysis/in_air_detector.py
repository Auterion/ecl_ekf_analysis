# /usr/bin/env/ python3
"""
a class for airtime detection.
"""
from typing import Optional, List
import numpy as np
from pyulog import ULog

from ecl_ekf_analysis.log_processing.custom_exceptions import PreconditionError


#pylint: disable=too-few-public-methods
class Airtime():
    """
    Airtime struct.
    """

    def __init__(self, take_off: float, landing: float):
        self.take_off = take_off
        self.landing = landing


class InAirDetector():
    """
    this class handles airtime detection.
    """

    def __init__(
            self, ulog: ULog, min_flight_time_seconds: float = 0.0,
            in_air_margin_seconds: float = 0.0) -> None:
        """
        initializes an InAirDetector instance.
        :param ulog:
        :param min_flight_time_seconds: set this value to return only airtimes that are at least
        min_flight_time_seconds long
        :param in_air_margin_seconds: removes a margin of in_air_margin_seconds from the airtime
        to avoid ground effects.
        """

        self._ulog = ulog
        self._min_flight_time_seconds = min_flight_time_seconds
        self._in_air_margin_seconds = in_air_margin_seconds

        try:
            self._vehicle_land_detected = ulog.get_dataset(
                'vehicle_land_detected').data
            self._landed = self._vehicle_land_detected['landed']
        except Exception as e:
            self._in_air = []
            raise PreconditionError(
                'InAirDetector: Could not find vehicle land detected message and/or landed field'
                ' and thus not find any airtime.') from e

        self._log_start = self._ulog.start_timestamp / 1.0e6

        self._in_air = self._detect_airtime()

    def _detect_airtime(self) -> List[Airtime]:
        """
        detects the airtime take_off and landing of a ulog.
        :return: a named tuple of ('Airtime', ['take_off', 'landing']) or None.
        """

        # test whether flight was in air at all
        if (self._landed > 0).all():
            print('InAirDetector: always on ground.')
            return []

        # find the indices of all take offs and landings
        take_offs = np.where(np.diff(self._landed) < 0)[0].tolist()
        landings = np.where(np.diff(self._landed) > 0)[0].tolist()

        # check for start in air.
        if len(take_offs) == 0 or (
            (len(landings) > 0) and (
                landings[0] < take_offs[0])):

            print('Started in air. Take first timestamp value as start point.')
            take_offs = [-1] + take_offs

        # correct for offset: add 1 to take_off list
        take_offs = [take_off + 1 for take_off in take_offs]
        if len(landings) < len(take_offs):
            print('No final landing detected. Assume last timestamp is landing.')
            landings += [len(self._landed) - 2]
        # correct for offset: add 1 to landing list
        landings = [landing + 1 for landing in landings]

        assert len(landings) == len(
            take_offs), 'InAirDetector: different number of take offs' ' and landings.'

        in_air = []
        for take_off, landing in zip(take_offs, landings):
            if (self._vehicle_land_detected['timestamp'][landing] / 1e6 -
                    self._in_air_margin_seconds) - \
                    (self._vehicle_land_detected['timestamp'][take_off] / 1e6 +
                     self._in_air_margin_seconds) >= self._min_flight_time_seconds:
                in_air.append(
                    Airtime(
                        take_off=(
                            self._vehicle_land_detected['timestamp'][take_off] -
                            self._ulog.start_timestamp) /
                        1.0e6 +
                        self._in_air_margin_seconds,
                        landing=(
                            self._vehicle_land_detected['timestamp'][landing] -
                            self._ulog.start_timestamp) /
                        1.0e6 -
                        self._in_air_margin_seconds))
        if len(in_air) == 0:
            print('InAirDetector: no airtime detected.')

        return in_air

    @property
    def airtimes(self) -> Optional[List[Airtime]]:
        """
        airtimes
        :return:
        """
        return self._in_air

    @property
    def take_off(self) -> Optional[float]:
        """
        first take off
        :return:
        """
        return self.airtimes[0].take_off if self.airtimes else None

    @property
    def landing(self) -> Optional[float]:
        """
        last landing
        :return: the last landing of the flight.
        """
        return self.airtimes[-1].landing if self.airtimes else None

    @property
    def log_start(self) -> Optional[float]:
        """
        log start
        :return: the start time of the log.
        """
        return self._log_start

    def get_sample_rate(self, dataset: str, multi_instance: int = 0) -> float:
        """
        :param dataset:
        :param multi_instance:
        :return:
        """
        data = self._ulog.get_dataset(
            dataset, multi_instance=multi_instance).data
        sample_rate = data['timestamp'].shape[0] / \
            ((data['timestamp'][-1] - data['timestamp'][0]) * 1.0e-6)

        return sample_rate

    def calc_rolling_window_len(
            self, dataset: str, window_len_s: float, odd: bool = True,
            multi_instance: int = 0) -> int:
        """
        :param dataset:
        :param window_len_s:
        :param odd:
        :param multi_instance:
        :return:
        """
        sample_rate = self.get_sample_rate(
            dataset, multi_instance=multi_instance)
        window_len = int(window_len_s * sample_rate)
        if odd and ((window_len % 2) == 0):
            window_len += 1

        return window_len

    def get_take_off_to_last_landing(self, dataset) -> list:
        """
        return all indices of the log file between the first take_off and the
        last landing.
        :param dataset:
        :return:
        """
        try:
            data = self._ulog.get_dataset(dataset).data
        except BaseException:
            print(f'InAirDetector: {dataset:s} not found in log.')
            return []

        if self.airtimes:
            airtime_indices = np.where(
                ((data['timestamp'] - self._ulog.start_timestamp) / 1.0e6 >=
                 self.airtimes[0].take_off) &
                ((data['timestamp'] - self._ulog.start_timestamp) /
                 1.0e6 < self.airtimes[-1].landing))[0]

        else:
            airtime_indices = []

        return airtime_indices

    def get_total_airtime_for_timestamp(
            self, timestamps: np.ndarray, start_time: Optional[float] = None,
            conversion_factor: Optional[float] = None) -> list:
        """
        :param timestamps:
        :param start_time: an optional start time (in the same unit as timestamps). if not
        specified, the first entry of timestamps is assumed to be the start time.
        :param conversion_factor: the factor to convert the timestamps into seconds. if not
        specified, it's assumed the timestamps are in seconds.
        :return:
        """
        airtime_indices = []
        start_timestamp = timestamps[0] if start_time is None else start_time
        convert = 1.0 if conversion_factor is None else conversion_factor

        if self.airtimes is not None:
            for airtime in self.airtimes:
                airtime_indices.extend(
                    np.where(
                        ((timestamps - start_timestamp) * convert >= airtime.take_off) &
                        ((timestamps - start_timestamp) * convert < airtime.landing))[0])

        return airtime_indices

    def get_airtime(self, dataset: str, multi_instance: int = 0) -> list:
        """
        return all indices of the log file that are in air
        :param dataset:
        :return:
        """
        try:
            data = self._ulog.get_dataset(
                dataset, multi_instance=multi_instance).data
        except Exception as e:
            raise PreconditionError(
                f'InAirDetector: {dataset:s} not found in log.') from e

        return self.get_total_airtime_for_timestamp(
            data['timestamp'],
            start_time=self._ulog.start_timestamp,
            conversion_factor=1.0e-6)

    def get_airtime_per_phase_for_timestamp(
            self, timestamps: np.ndarray, start_time: Optional[float] = None,
            conversion_factor: Optional[float] = None) -> list:
        """
        :param timestamps:
        :param start_time: an optional start time (in the same unit as timestamps). if not
        specified, the first entry of timestamps is assumed to be the start time.
        :param conversion_factor: the factor to convert the timestamps into seconds. if not
        specified, it's assumed the timestamps are in seconds.
        :return:
        """
        airtime_indices = []
        start_timestamp = timestamps[0] if start_time is None else start_time
        convert = 1.0 if conversion_factor is None else conversion_factor

        if self.airtimes is not None:
            for airtime in self.airtimes:
                airtime_indices.append(
                    np.where(
                        ((timestamps - start_timestamp) * convert >= airtime.take_off) &
                        ((timestamps - start_timestamp) * convert < airtime.landing))[0])

        return airtime_indices

    def get_airtime_per_phase(
            self,
            dataset: str,
            multi_instance: int = 0) -> List[list]:
        """
        return all indices of the log file that are in air
        :param dataset:
        :param multi_instance:
        :return:
        """
        try:
            data = self._ulog.get_dataset(
                dataset, multi_instance=multi_instance).data
        except Exception as e:
            raise PreconditionError(
                f'InAirDetector: {dataset:s} not found in log.') from e

        return self.get_airtime_per_phase_for_timestamp(
            data['timestamp'],
            start_time=self._ulog.start_timestamp,
            conversion_factor=1.0e-6)
