# /usr/bin/env/ python3
"""
functions for comparing test results.
"""
import pytest


def compare_float_values(
        value_name: str, log_id: str, analysis_value: float, ground_truth_value: float,
        parent_name: str = '', rel_tol: float = 1e-6, abs_tol: float = 1e-12) -> None:
    """
    :param value_name:
    :param analysis_value:
    :param ground_truth_value:
    :return:
    """
    # pylint: disable=unidiomatic-typecheck
    assert type(analysis_value) == type(ground_truth_value), \
        'analysis result type {:s} is different to the ground truth type {:s} ' \
        'in {:s} in {:s}'.format(
            str(type(analysis_value)),
            str(type(ground_truth_value)), value_name, log_id)
    if isinstance(ground_truth_value, float):
        assert analysis_value == pytest.approx(ground_truth_value, rel=rel_tol, abs=abs_tol), \
            '{:s} {:s} statistic was different to ground truth statistic in {:s}'.format(
                parent_name, value_name, log_id)


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
        'analysis check result type {:s} differed from ground truth {:s} in {:s}'.format(
            check_result['type'], ground_truth_check_result['type'], log_id)

    assert check_result['status'] == ground_truth_check_result['status'], \
        'analysis check result status {:s} in {:s} differed from ground truth {:s} in {:s}'.format(
            check_result['status'], check_result['type'], ground_truth_check_result['status'],
            log_id)

    assert len(check_result['statistics']) == len(ground_truth_check_result['statistics']), \
        'number of check statistics of {:s} in {:s} from analysis differed to number of ground ' \
        'truth statistics.'.format(check_result['type'], log_id)

    for check_statistic, ground_truth_check_statistic in zip(
            check_result['statistics'], ground_truth_check_result['statistics']):

        assert check_statistic['type'] == ground_truth_check_statistic['type'], \
            'analysis check statistic type {:s} differed from ground truth {:s} in {:s}'.format(
                check_statistic['type'], ground_truth_check_statistic['type'], log_id)

        assert check_statistic['instance'] == ground_truth_check_statistic['instance'], \
            'analysis check statistic instance {:s} differed from ground truth {:s} in {:s}'.format(
                check_statistic['instance'], ground_truth_check_statistic['instance'], log_id)

        compare_float_values(
            check_statistic['type'], log_id, check_statistic['value'],
            ground_truth_check_statistic['value'], parent_name=check_result['type'],
            rel_tol=rel_tol, abs_tol=abs_tol)

        compare_float_values(
            f"{check_statistic['type']:s} failure threshold", log_id,
            check_statistic['thresholds']['failure'],
            ground_truth_check_statistic['thresholds']['failure'], parent_name=check_result['type'],
            rel_tol=rel_tol, abs_tol=abs_tol)

        compare_float_values(
            f"{check_statistic['type']:s} warning threshold", log_id,
            check_statistic['thresholds']['warning'],
            ground_truth_check_statistic['thresholds']['warning'], parent_name=check_result['type'],
            rel_tol=rel_tol, abs_tol=abs_tol)
