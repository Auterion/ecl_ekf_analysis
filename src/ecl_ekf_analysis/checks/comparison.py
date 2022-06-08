# /usr/bin/env/ python3
"""
functions for comparing test results.
"""
import pytest


def compare_float_values(
        value_name: str,
        log_id: str,
        analysis_value: float,
        ground_truth_value: float,
        parent_name: str = '',
        rel_tol: float = 1e-6,
        abs_tol: float = 1e-12) -> None:
    """
    :param value_name:
    :param analysis_value:
    :param ground_truth_value:
    :return:
    """
    # pylint: disable=unidiomatic-typecheck
    assert isinstance(analysis_value, type(ground_truth_value)), \
        f'analysis result type {str(type(analysis_value)):s} is different' \
        f'to the ground truth type {str(type(ground_truth_value)):s} ' \
        f'in {value_name:s} in {log_id:s}'
    if isinstance(ground_truth_value, float):
        assert analysis_value == pytest.approx(ground_truth_value, rel=rel_tol, abs=abs_tol), \
            f'{parent_name:s} {value_name:s} statistic was' \
            f'different to ground truth statistic in {log_id:s}'


def compare_check_analysis_result_ground_truth(
        check_result: dict, ground_truth_check_result: dict, log_id: str,
        rel_tol: float = 1e-6, abs_tol: float = 1e-12) -> None:
    """
    compares the analysis result of a check to the ground truth
    :param check_status:
    :param check_data:
    :param ground_truth_data:
    :return:
    """
    assert check_result['type'] == ground_truth_check_result['type'], \
        f'analysis check result type {check_result["type"]:s} differed from' \
        f'ground truth {ground_truth_check_result["type"]:s} in {log_id:s}'

    assert check_result['status'] == ground_truth_check_result['status'], \
        f'analysis check result status {check_result["status"]:s} in' \
        f'{check_result["type"]:s} differed from ground truth' \
        f'{ground_truth_check_result["status"]:s} in {log_id:s}'

    assert len(check_result['statistics']) == len(ground_truth_check_result['statistics']), \
        f'number of check statistics of {check_result["type"]:s} in' \
        f'{log_id:s} from analysis differed to number of ground ' \
        f'truth statistics.'

    for check_statistic, ground_truth_check_statistic in zip(
            check_result['statistics'], ground_truth_check_result['statistics']):

        assert check_statistic['type'] == ground_truth_check_statistic['type'], \
            f'analysis check statistic type {check_statistic["type"]:s} differed from' \
            f'ground truth {ground_truth_check_statistic["type"]:s} in {log_id:s}'

        assert check_statistic['instance'] == ground_truth_check_statistic['instance'], \
            f'analysis check statistic instance {check_statistic["instance"]:s} differed' \
            f'from ground truth {ground_truth_check_statistic["instance"]:s} in {log_id:s}'

        compare_float_values(
            check_statistic['type'],
            log_id,
            check_statistic['value'],
            ground_truth_check_statistic['value'],
            parent_name=check_result['type'],
            rel_tol=rel_tol,
            abs_tol=abs_tol)

        compare_float_values(
            f"{check_statistic['type']:s} failure threshold",
            log_id,
            check_statistic['thresholds']['failure'],
            ground_truth_check_statistic['thresholds']['failure'],
            parent_name=check_result['type'],
            rel_tol=rel_tol,
            abs_tol=abs_tol)

        compare_float_values(
            f"{check_statistic['type']:s} warning threshold",
            log_id,
            check_statistic['thresholds']['warning'],
            ground_truth_check_statistic['thresholds']['warning'],
            parent_name=check_result['type'],
            rel_tol=rel_tol,
            abs_tol=abs_tol)
