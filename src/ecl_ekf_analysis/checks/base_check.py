# /usr/bin/env/ python3
"""
base classes for running checks
"""
from pyulog import ULog

import grpc_interfaces.check_data_pb2 as check_data_api
from grpc_interfaces.check_data_pb2 import CheckResult, CheckStatistic, CheckType, \
    CheckStatisticType, CheckStatus
from log_processing.custom_exceptions import capture_message


class Check():
    """
    A check interface.
    """
    def __init__(
            self, ulog: ULog, check_type: CheckType = check_data_api.CHECK_TYPE_UNDEFINED) -> None:
        """
        Initializes the check interface.
        :param ulog: a handle to the open ulog file
        :param thresholds: a dictionary
        """
        self.ulog = ulog
        self._check_result = CheckResult()
        self._check_result.type = check_type
        self._error_message = ''


    def add_statistic(self, check_statistic_type: CheckStatisticType) -> CheckStatistic:
        """
        add a check statistic to the check results
        :param type:
        :return:
        """
        statistic = self._check_result.statistics.add()
        statistic.type = check_statistic_type
        return statistic


    @property
    def status(self) -> CheckStatus:
        """
        :return:
        """
        return self._check_result.status

    @property
    def result(self) -> CheckResult:
        """
        :return:
        """
        return self._check_result

    @property
    def type(self) -> check_data_api.CheckType:
        """
        :return:
        """
        return self._check_result.type

    def calc_statistics(self) -> None:
        """
        function interface for running a check: can use the property _ulog and should set the
        _check_status and write _check_statistics
        """

    def _precondition(self) -> bool:
        """
        precondition for running the check. the check status is set to does not apply if the
        precondition is not met.
        :return: True by default.
        """
        return True


    def run(self) -> None:
        """
        runs the check functions for calculating the statistics and calculates the check status
        :return:
        """
        if not self._precondition():
            self._check_result.status = check_data_api.CHECK_STATUS_DOES_NOT_APPLY
            return

        self.calc_statistics()

        for statistic in self._check_result.statistics:

            if statistic.type == check_data_api.CHECK_STATISTIC_TYPE_UNDEFINED:
                capture_message('Warning: check statistics type is undefined')

            if self._check_result.status == check_data_api.CHECK_STATUS_UNDEFINED:
                self._check_result.status = check_data_api.CHECK_STATUS_PASS

            if statistic.HasField('thresholds'):
                if statistic.thresholds.HasField('failure') and \
                    statistic.value > statistic.thresholds.failure.value:
                    self._check_result.status = check_data_api.CHECK_STATUS_FAIL
                if statistic.thresholds.HasField('warning') and \
                    statistic.value > statistic.thresholds.warning.value:
                    if self._check_result.status != check_data_api.CHECK_STATUS_FAIL:
                        self._check_result.status = check_data_api.CHECK_STATUS_WARNING
