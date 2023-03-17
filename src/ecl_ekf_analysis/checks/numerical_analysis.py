# /usr/bin/env python3
"""
the numerical analysis
"""
from pyulog import ULog
import numpy as np

from ecl_ekf_analysis.checks.base_check import Check
from ecl_ekf_analysis.check_data_interfaces.check_data import CheckType, CheckStatisticType
from ecl_ekf_analysis.config import thresholds


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
        estimator_status_data = self.ulog.get_dataset('estimator_status_flags').data

        filter_fault_flag = self.add_statistic(
            CheckStatisticType.FILTER_FAULT_FLAG)

        flags = [
        "fs_bad_mag_x",
        "fs_bad_mag_y",
        "fs_bad_mag_z",
        "fs_bad_hdg",
        "fs_bad_mag_decl",
        "fs_bad_airspeed",
        "fs_bad_sideslip",
        "fs_bad_optflow_x",
        "fs_bad_optflow_y",
        "fs_bad_vel_n",
        "fs_bad_vel_e",
        "fs_bad_vel_d",
        "fs_bad_pos_n",
        "fs_bad_pos_e",
        "fs_bad_pos_d",
        "fs_bad_acc_bias",
        "fs_bad_acc_vertical",
        "fs_bad_acc_clipping",
        ]

        filter_fault_flag.value = 0.0

        for flag in flags:
            if np.any(estimator_status_data[flag]):
                filter_fault_flag.value = 1.0
                break

        filter_fault_flag.thresholds.failure = thresholds.ecl_filter_fault_flag_failure()
