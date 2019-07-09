# /usr/bin/env/ python3
"""
utility functions for check data.
"""
from typing import List
from grpc_interfaces.check_data_pb2 import (CheckResult, CheckStatistic, CheckStatisticType,
                                            CheckStatus, CheckType)
import grpc_interfaces.check_data_pb2 as check_data_api


check_status_str_from_enum = {
    check_data_api.CHECK_STATUS_UNDEFINED: "Undefined",
    check_data_api.CHECK_STATUS_PASS: "Pass",
    check_data_api.CHECK_STATUS_WARNING: "Warning",
    check_data_api.CHECK_STATUS_FAIL: "Fail",
    check_data_api.CHECK_STATUS_DOES_NOT_APPLY: "Does_Not_Apply"
}


def deserialize_check_statistic(check_statistic: CheckStatistic) -> dict:
    """
    deserialize a CheckStatistic proto structure into a python dictionary.
    :param check_statistic:
    :return:
    """
    return {
        'type': CheckStatisticType.Name(check_statistic.type),
        'value': check_statistic.value,
        'thresholds': {
            'warning': check_statistic.thresholds.warning.value,
            'failure': check_statistic.thresholds.failure.value
        }
    }


def deserialize_check_result(check_result: CheckResult) -> dict:
    """
    deserialize a CheckResult proto structure into a python dictionary.
    :param check_result:
    :return:
    """
    check_result_dict = {
        'status': CheckStatus.Name(check_result.status),
        'type': CheckType.Name(check_result.type),
        'statistics': list()
    }
    for check_statistic in check_result.statistics:
        check_result_dict['statistics'].append(deserialize_check_statistic(check_statistic))
    return check_result_dict


def deserialize_check_results(check_results: List[CheckResult]) -> List[dict]:
    """
    deserialize a list of CheckResult proto structures into a python list.
    :param check_result:
    :return:
    """
    return [deserialize_check_result(check_result) for check_result in check_results]


def serialize_check_statistic(check_statistic_dict: dict) -> CheckStatistic:
    """
    serialize a python check statistic dict into a CheckStatistic proto structures.
    :param check_result:
    :return:
    """
    check_statistic = CheckStatistic()
    check_statistic.type = CheckStatisticType.Value(check_statistic_dict.get('type'))
    check_statistic.value = check_statistic_dict.get('value')
    check_statistic.thresholds.warning.value = check_statistic_dict.get('thresholds').get('warning')
    check_statistic.thresholds.failure.value = check_statistic_dict.get('thresholds').get('failure')
    return check_statistic


def serialize_check_result(check_result_dict: dict) -> CheckResult:
    """
    serialize a python check result dict into a CheckResult proto structures.
    :param check_result:
    :return:
    """
    check_result = CheckResult()
    check_result.status = CheckStatus.Value(check_result_dict.get('status'))
    check_result.type = CheckType.Value(check_result_dict.get('type'))
    check_result.statistics.extend(
        [serialize_check_statistic(check_statistic)
         for check_statistic in check_result_dict.get('statistics')]
    )
    return check_result


def serialize_check_results(check_results: List[dict]) -> List[CheckResult]:
    """
    serialize a python list of check results into a list of CheckResult proto structures.
    :param check_result:
    :return:
    """
    return [serialize_check_result(check_result) for check_result in check_results]
