#! /usr/bin/env python3
"""
Testing some specific functions for signal processing.
"""
import numpy as np

from ecl_ekf_analysis.signal_processing.flag_analysis import detect_flag_value_changes


def test_detect_flag_value_changes():
    """
    tests corner cases of the detect_flag_value_changes function
    :param testing_args:
    :return:
    """
    assert detect_flag_value_changes(np.empty(0, dtype=int)) == ([], []), \
        'empty array was not handled correctly'

    # input: 1 1 1 1 1  1 1 1 1 1  1 1 1 1 1  1 1 1 1 1
    assert detect_flag_value_changes(np.ones(20, dtype=int)) == ([0], [19]), \
        'always active flag should yield one phase from flight start to end'
    # input: 0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0 0
    assert detect_flag_value_changes(np.zeros(20, dtype=int)) == ([], []), \
        'always active flag should not yield a flight phase'
    # input: 0 0 0 0 0  0 0 0 0 0  1 1 1 1 1  1 1 1 1 1
    assert detect_flag_value_changes(
        np.concatenate((np.zeros(10, dtype=int), np.ones(10, dtype=int)))) == ([10], [19]), \
        'position phase not detected correctly'
    # input: 1 1 1 1 1  1 1 1 1 1  0 0 0 0 0  0 0 0 0 0
    assert detect_flag_value_changes(
        np.concatenate((np.ones(10, dtype=int), np.zeros(10, dtype=int)))) == ([0], [9]), \
        'position phase not detected correctly'
    # input: 0 0 0 0 0  1 1 1 1 1  0 0 0 0 0  0 0 0 0 0
    assert detect_flag_value_changes(np.concatenate(
        (np.zeros(5, dtype=int), np.ones(5, dtype=int), np.zeros(10, dtype=int)))) == ([5], [9]), \
        'position phase not detected correctly'
    # input: 0 0 0 0 0  1 1 1 1 1  0 0 0 0 0  1 1 1 1 1
    assert detect_flag_value_changes(np.concatenate(
        (np.zeros(5, dtype=int), np.ones(5, dtype=int),
         np.zeros(5, dtype=int), np.ones(5, dtype=int)))) == ([5, 15], [9, 19]), \
        'position phase not detected correctly'
    # input: 1 1 1 1 1  0 0 0 0 0  1 1 1 1 1  0 0 0 0 0
    assert detect_flag_value_changes(np.concatenate(
        (np.ones(5, dtype=int), np.zeros(5, dtype=int),
         np.ones(5, dtype=int), np.zeros(5, dtype=int)))) == ([0, 10], [4, 14]), \
        'position phase not detected correctly'
    # input: 0 0 0 0  1 1 1 1  0 0 0 0  1 1 1 1  0 0 0 0
    assert detect_flag_value_changes(np.concatenate(
        (np.zeros(4, dtype=int), np.ones(4, dtype=int), np.zeros(4, dtype=int),
         np.ones(4, dtype=int), np.zeros(4, dtype=int)))) == ([4, 12], [7, 15]), \
        'position phase not detected correctly'
    # input: 1 1 1 1  0 0 0 0  1 1 1 1  0 0 0 0  1 1 1 1
    assert detect_flag_value_changes(np.concatenate(
        (np.ones(4, dtype=int), np.zeros(4, dtype=int), np.ones(4, dtype=int),
         np.zeros(4, dtype=int), np.ones(4, dtype=int)))) == ([0, 8, 16], [3, 11, 19]), \
        'position phase not detected correctly'
