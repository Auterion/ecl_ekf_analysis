# /usr/bin/env/ python3
"""
base check runner class
"""

from typing import List, Set, Dict

from ecl_ekf_analysis.log_processing.custom_exceptions import PreconditionError, capture_exception
from ecl_ekf_analysis.check_data_interfaces.check_data import CheckResult, CheckStatus
from ecl_ekf_analysis.check_data_interfaces.check_data_utils import deserialize_check_results, \
    deserialize_check_result
from ecl_ekf_analysis.checks.base_check import Check


class CheckRunner():
    """
    a runner class for checks
    """
    def __init__(self):
        """
        initialize the class
        """
        self._checks = list()
        self._analysis_status = 0
        self._error_message = ''
        self._check_results = list()
        self._results_table = list()


    def append(self, check: Check):
        """

        :param check:
        :return:
        """
        self._checks.append(check)


    def _create_results_table(self) -> Dict[str, tuple]:
        """
        :return:
        """
        results_table = dict()
        for check_result in self._check_results:
            check_name = check_result.check_type.name
            check_status = check_result.status.legacy_name
            check_data = deserialize_check_result(check_result)
            results_table[check_name] = (check_status, '', check_data)

        return results_table


    def run_checks(self):
        """
        runs the checks appended to this check runner.
        :return:
        """
        analyses_statuses = list()
        for check in self._checks:
            try:
                check.run()
                self._check_results.append(check.result)
                analyses_statuses.append(0)
            except PreconditionError as e:
                analyses_statuses.append(-3)
                capture_exception(e)
                check.status = CheckStatus.DOES_NOT_APPLY
                self._error_message += str(e) + '; '
                print(e)
            except RuntimeError as e:
                analyses_statuses.append(-2)
                capture_exception(e)
                check.status = CheckStatus.DOES_NOT_APPLY
                self._error_message += str(e) + '; '
                print(e)
            except Exception as e:
                analyses_statuses.append(-1)
                capture_exception(e)
                check.status = CheckStatus.DOES_NOT_APPLY
                self._error_message += str(e) + '; '
                print(e)

        # merge statuses
        if len(analyses_statuses) > 0:
            # retry the analysis if one of the sub-analyses received an unexpected error
            if any(status == -1 for status in analyses_statuses):
                self._analysis_status = -1
            elif any(status == 0 for status in analyses_statuses):
                # set the checks of all failing analyses to Does Not Apply, such that they don't
                # show up in the results table
                self._analysis_status = 0
            else:
                self._analysis_status = min(analyses_statuses)


    @property
    def results(self) -> List[CheckResult]:
        """
        :return:
        """
        return self._check_results

    @property
    def results_deserialized(self) -> List[dict]:
        """
        :return:
        """
        return deserialize_check_results(self._check_results)

    @property
    def analysis_status(self) -> int:
        """
        :return: the analysis status
        """
        return self._analysis_status

    @analysis_status.setter
    def analysis_status(self, status: int) -> None:
        """
        :param check_status:
        :return:
        """
        self._analysis_status = status

    @property
    def results_table(self) -> Dict[str, tuple]:
        """
        :return: the results table
        """
        return self._create_results_table()


    @property
    def does_not_apply(self) -> Set[str]:
        """
        :return: a set with checks that don't apply
        """
        return {check.check_type.name for check in self._check_results
                if check.status == CheckStatus.DOES_NOT_APPLY}

    @property
    def error_message(self) -> str:
        """
        :return: the error message
        """
        return self._error_message

    @error_message.setter
    def error_message(self, message: str) -> None:
        """
        :param check_status:
        :return:
        """
        self._error_message = message
