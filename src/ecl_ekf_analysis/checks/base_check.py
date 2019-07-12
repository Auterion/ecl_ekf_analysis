# /usr/bin/env/ python3
"""
base classes for running checks
"""
from pyulog import ULog

from check_data_interfaces.check_data import CheckResult, CheckStatistic, CheckType, \
    CheckStatisticType, CheckStatus
from log_processing.custom_exceptions import capture_message


class Check():
    """
    A check interface.
    """
    def __init__(
            self, ulog: ULog, check_type: CheckType = CheckType.UNDEFINED) -> None:
        """
        Initializes the check interface.
        :param ulog: a handle to the open ulog file
        :param thresholds: a dictionary
        """
        self.ulog = ulog
        self._check_result = CheckResult()
        self._check_result.check_type = check_type
        self._error_message = ''
        self._does_apply = True


    def add_statistic(self, check_statistic_type: CheckStatisticType) -> CheckStatistic:
        """
        add a check statistic to the check results
        :param type:
        :return:
        """
        statistic = self._check_result.statistics.add()
        statistic.statistic_type = check_statistic_type
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
    def check_type(self) -> CheckType:
        """
        :return:
        """
        return self._check_result.check_type


    def calc_statistics(self) -> None:
        """
        function interface for running a check: can use the property _ulog and should set the
        _check_status and write _check_statistics
        """


    def run_precondition(self) -> None:
        """
        precondition function that is being run before running the check. meant to assign the
        _does_apply member variable. running the check is skipped, if _does_apply is set to False.
        """


    def run(self) -> None:
        """
        runs the check functions for calculating the statistics and calculates the check status
        :return:
        """
        self.run_precondition()
        if not self._does_apply:
            self._check_result.status = CheckStatus.DOES_NOT_APPLY
            return

        self.calc_statistics()

        for statistic in self._check_result.statistics:

            if statistic.statistic_type == CheckStatisticType.UNDEFINED:
                capture_message('Warning: check statistics type is undefined')

            if self._check_result.status == CheckStatus.UNDEFINED:
                self._check_result.status = CheckStatus.PASS

            if statistic.value is not None:
                if statistic.thresholds.failure is not None and \
                    statistic.value > statistic.thresholds.failure:
                    self._check_result.status = CheckStatus.FAIL
                if statistic.thresholds.warning is not None and \
                    statistic.value > statistic.thresholds.warning:
                    if self._check_result.status != CheckStatus.FAIL:
                        self._check_result.status = CheckStatus.WARNING
