# /usr/bin/env/ python3
"""
utility functions for check data.
"""
from typing import List
from ecl_ekf_analysis.check_data_interfaces.check_data import (CheckResult, CheckStatistic,
                                                               CheckStatisticType, CheckStatus,
                                                               CheckType)

def deserialize_check_statistic(check_statistic: CheckStatistic) -> dict:
    """
    deserialize a CheckStatistic proto structure into a python dictionary.
    :param check_statistic:
    :return:
    """
    return {
        'type': check_statistic.statistic_type.name,
        'value': check_statistic.value,
        'instance': check_statistic.statistic_instance,
        'thresholds': {
            'warning': check_statistic.thresholds.warning,
            'failure': check_statistic.thresholds.failure
        }
    }


def deserialize_check_result(check_result: CheckResult) -> dict:
    """
    deserialize a CheckResult structure into a python dictionary.
    :param check_result:
    :return:
    """
    check_result_dict = {
        'status': check_result.status.name,
        'type': check_result.check_type.name,
        'statistics': []
    }
    for check_statistic in check_result.statistics:
        check_result_dict['statistics'].append(deserialize_check_statistic(check_statistic))
    return check_result_dict


def deserialize_check_results(check_results: List[CheckResult]) -> List[dict]:
    """
    deserialize a list of CheckResult structures into a python list.
    :param check_result:
    :return:
    """
    return [deserialize_check_result(check_result) for check_result in check_results]


def serialize_check_statistic(check_statistic_dict: dict) -> CheckStatistic:
    """
    serialize a python check statistic dict into a CheckStatistic structure.
    :param check_result:
    :return:
    """
    check_statistic = CheckStatistic()
    check_statistic.type = CheckStatisticType[check_statistic_dict.get('type', 'UNDEFINED')]
    check_statistic.value = check_statistic_dict.get('value')
    check_statistic.statistic_instance = check_statistic_dict.get('instance', 0)
    check_statistic.thresholds.warning = check_statistic_dict.get('thresholds').get('warning')
    check_statistic.thresholds.failure = check_statistic_dict.get('thresholds').get('failure')
    return check_statistic


def serialize_check_result(check_result_dict: dict) -> CheckResult:
    """
    serialize a python check result dict into a CheckResult structure.
    :param check_result:
    :return:
    """
    check_result = CheckResult()
    check_result.status = CheckStatus[check_result_dict.get('status', 'UNDEFINED')]
    check_result.type = CheckType[check_result_dict.get('type', 'UNDEFINED')]
    check_result.statistics.extend(
        [serialize_check_statistic(check_statistic)
         for check_statistic in check_result_dict.get('statistics')]
    )
    return check_result


def serialize_check_results(check_results: List[dict]) -> List[CheckResult]:
    """
    serialize a python list of check results into a list of CheckResult structures.
    :param check_result:
    :return:
    """
    return [serialize_check_result(check_result) for check_result in check_results]
