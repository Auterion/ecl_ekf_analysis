# /usr/bin/env/ python3
"""
base classes for running checks
"""

from enum import IntEnum
from typing import Optional


#pylint: disable=too-few-public-methods
class Thresholds():
    """
    threshold struct.
    """
    def __init__(self, warning: Optional[float] = None, failure: Optional[float] = None) -> None:
        self.warning = warning
        self.failure = failure


class CheckStatisticType(IntEnum):
    """
    an enum for the check statistic type
    """
    UNDEFINED = 0
    ESTIMATOR_FAILURE_MAX = 1
    ESTIMATOR_FAILURE_AVG = 2
    ESTIMATOR_FAILURE_WINDOWED_AVG = 3
    INNOVATION_AMBER_PCT = 4
    INNOVATION_AMBER_WINDOWED_PCT = 5
    INNOVATION_RED_PCT = 6
    INNOVATION_RED_WINDOWED_PCT = 7
    FAIL_RATIO_PCT = 8
    FAIL_RATIO_WINDOWED_PCT = 9
    IMU_CONING_MAX = 10
    IMU_CONING_AVG = 11
    IMU_CONING_WINDOWED_AVG = 12
    IMU_HIGH_FREQ_DELTA_ANGLE_MAX = 13
    IMU_HIGH_FREQ_DELTA_ANGLE_AVG = 14
    IMU_HIGH_FREQ_DELTA_ANGLE_WINDOWED_AVG = 15
    IMU_HIGH_FREQ_DELTA_VELOCITY_MAX = 16
    IMU_HIGH_FREQ_DELTA_VELOCITY_AVG = 17
    IMU_HIGH_FREQ_DELTA_VELOCITY_WINDOWED_AVG = 18
    IMU_OBSERVED_ANGLE_ERROR_AVG = 19
    IMU_OBSERVED_ANGLE_ERROR_WINDOWED_AVG = 20
    IMU_OBSERVED_VELOCITY_ERROR_AVG = 21
    IMU_OBSERVED_VELOCITY_ERROR_WINDOWED_AVG = 22
    IMU_OBSERVED_POSITION_ERROR_AVG = 23
    IMU_OBSERVED_POSITION_ERROR_WINDOWED_AVG = 24
    IMU_DELTA_ANGLE_BIAS_AVG = 25
    IMU_DELTA_ANGLE_BIAS_WINDOWED_AVG = 26
    IMU_DELTA_VELOCITY_BIAS_AVG = 27
    IMU_DELTA_VELOCITY_BIAS_WINDOWED_AVG = 28
    FILTER_FAULT_FLAG = 29


    @property
    def type_name(self) -> str:
        """
        return the enum as a str
        :return:
        """
        return self._name_


class CheckStatistic():
    """
    check statistic struct.
    """
    def __init__(
            self, statistic_type: CheckStatisticType = CheckStatisticType.UNDEFINED,
            value: Optional[float] = None, thresholds: Optional[Thresholds] = None,
            statistic_instance: int = 0) -> None:
        self.statistic_type = statistic_type
        self.statistic_instance = statistic_instance
        self.value = value
        self.thresholds = thresholds if thresholds is not None else Thresholds()


class CheckStatus(IntEnum):
    """
    an enum for the analysis result to enable comparisons
    """
    UNDEFINED = 0
    PASS = 1
    WARNING = 2
    FAIL = 3
    DOES_NOT_APPLY = 4


    @property
    def status_name(self) -> str:
        """
        return the enum as a str
        :return:
        """
        return self._name_

    @property
    def legacy_name(self) -> str:
        """
        return the enum as a legacy str (capitalized)
        :return:
        """
        return self._name_.capitalize()


class CheckType(IntEnum):
    """
    an enum for the check type
    """
    UNDEFINED = 0
    MAGNETOMETER_STATUS = 1
    MAGNETIC_HEADING_STATUS = 2
    VELOCITY_SENSOR_STATUS = 3
    POSITION_SENSOR_STATUS = 4
    HEIGHT_SENSOR_STATUS = 5
    HEIGHT_ABOVE_GROUND_SENSOR_STATUS = 6
    AIRSPEED_SENSOR_STATUS = 7
    SIDESLIP_SENSOR_STATUS = 8
    IMU_VIBRATION_STATUS = 9
    IMU_BIAS_STATUS = 10
    IMU_OUTPUT_PREDICTOR_STATUS = 11
    OPTICAL_FLOW_STATUS = 12
    FILTER_FAULT_STATUS = 13


    @property
    def type_name(self) -> str:
        """
        return the enum as a str
        :return:
        """
        return self._name_


class CheckStatisticsList(list):
    """
    check statistics list struct.
    """
    def add(self) -> CheckStatistic:
        """
        :return:
        """
        statistic = CheckStatistic()
        self.append(statistic)
        return statistic


class CheckResult():
    """
    check statistic struct.
    """
    def __init__(
            self, status: CheckStatus = CheckStatus.UNDEFINED,
            check_type: CheckType = CheckType.UNDEFINED) -> None:
        self.status = status
        self.check_type = check_type
        self.statistics = CheckStatisticsList()

