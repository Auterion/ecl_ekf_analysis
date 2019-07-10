# /usr/bin/env python3
"""
the numerical analysis
"""
from typing import Dict

from pyulog import ULog
import numpy as np


from checks.base_check import Check
from grpc_interfaces.check_data_pb2 import CheckType
import grpc_interfaces.check_data_pb2 as check_data_api
from log_processing.analysis import calculate_windowed_mean_per_airphase, calculate_stat_from_signal
from analysis.in_air_detector import InAirDetector
import config.params as params
import config.thresholds as thresholds


class NumericalCheck(Check):
    """
    the attitude check.
    """
    def __init__(self, ulog: ULog):
        """
        :param ulog:
        """
        super(NumericalCheck, self).__init__(
            ulog, check_type=check_data_api.CHECK_TYPE_ECL_FILTER_FAULT_STATUS)


    def calc_statistics(self) -> None:
        """
        :return:
        """
        filter_fault_flag = self.add_statistic(
            check_data_api.CHECK_STATISTIC_TYPE_ECL_FILTER_FAULT_FLAG)