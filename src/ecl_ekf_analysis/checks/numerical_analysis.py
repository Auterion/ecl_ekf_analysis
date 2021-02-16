# /usr/bin/env python3
"""
the numerical analysis
"""
from pyulog import ULog
import numpy as np

from ecl_ekf_analysis.checks.base_check import Check
from ecl_ekf_analysis.check_data_interfaces.check_data import CheckType, CheckStatisticType
import ecl_ekf_analysis.config.thresholds as thresholds


class NumericalCheck(Check):
    """
    the numerical check.
    """
    def __init__(self, ulog: ULog):
        """
        :param ulog:
        """
        super().__init__(
            ulog, check_type=CheckType.FILTER_FAULT_STATUS)


    def calc_statistics(self) -> None:
        """
        :return:
        """
        estimator_status_data = self.ulog.get_dataset('estimator_status').data

        filter_fault_flag = self.add_statistic(CheckStatisticType.FILTER_FAULT_FLAG)
        filter_fault_flag.value = float(
            np.amax(estimator_status_data['filter_fault_flags']))
        filter_fault_flag.thresholds.failure = thresholds.ecl_filter_fault_flag_failure()
