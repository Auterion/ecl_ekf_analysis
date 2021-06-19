# /usr/bin/env python3
"""
This module contains helper functions for analysis of some of the flight control flags.
"""
from typing import Tuple

import numpy as np


def detect_flag_value_changes(flag: np.ndarray) -> Tuple[list, list]:
    """
    detects changes in the value of flag and handles the edge cases
    :param flag: an array of integers of 0 and 1s: the assumption is 1 present a phase, while
    0 does not.
    :return: a Tuple of
    """
    phase_starts = list()
    phase_ends = list()

    if np.any(flag > 0):
        # find the indices of all phase starts and endings
        phase_starts = np.where(np.diff(flag) > 0)[0].tolist()
        phase_ends = np.where(np.diff(flag) < 0)[0].tolist()

        # check for activation at start.
        if len(phase_starts) == 0 or ((len(phase_ends) > 0) and (phase_ends[0] < phase_starts[0])):
            print("Flag was activated at start. Take first timestamp value as start point.")
            phase_starts = [-1] + phase_starts
        # correct for offset: add 1 to start list
        phase_starts = [phase_start + 1 for phase_start in phase_starts]

        if len(phase_ends) < len(phase_starts):
            print("No final phase end detected. Assume last timestamp is end.")
            phase_ends += [len(flag) - 1]

    assert len(phase_ends) == len(phase_starts), (
        "FlagValueChanges: different number of " "phase starts and phase ends."
    )

    return phase_starts, phase_ends
