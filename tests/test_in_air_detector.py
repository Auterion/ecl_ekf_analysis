#! /usr/bin/env python3
"""
Testing the ml log analysis.
"""

import os
import pytest
import numpy as np
from pyulog import ULog
from analysis.detectors import InAirDetector

@pytest.fixture(scope="module")
def testing_args():
    """
    arguments for testing.
    :return: test arguments
    """
    return {'test_flight_logs_path': os.path.join(os.path.dirname(__file__), 'flight_logs'),
            'simple_test_flight_log': 'short_f450_log.ulg',
            'dummy_log_file': 'short_f450_log.ulg'}


def original_take_offs(ulog):
    """

    :param ulog:
    :return:
    """
    in_air_detector = InAirDetector(ulog, min_flight_time_seconds=0.0,
                                    in_air_margin_seconds=0.0)
    airtimes = in_air_detector.airtimes

    assert len(airtimes) == 1
    assert 3.7 < airtimes[0].take_off < 3.8  # 3.797098
    assert 403.9 < airtimes[-1].landing < 404.0  # 403.945201


def always_on_ground(ulog):
    """

    :param ulog:
    :return:
    """
    ts_length = ulog.get_dataset('vehicle_land_detected').data['landed'].shape[0]
    ulog.get_dataset('vehicle_land_detected').data['landed'] = np.ones(ts_length, dtype=int)
    in_air_detector = InAirDetector(ulog, min_flight_time_seconds=0.0,
                                    in_air_margin_seconds=0.0)
    first_take_off = in_air_detector.take_off
    airtimes = in_air_detector.airtimes

    assert first_take_off is None, 'The first take_off is not None.'
    assert len(airtimes) == 0


def always_in_air(ulog):
    """

    :param ulog:
    :return:
    """
    ts_length = ulog.get_dataset('vehicle_land_detected').data['landed'].shape[0]
    ulog.get_dataset('vehicle_land_detected').data['landed'] = np.zeros(ts_length, dtype=int)
    in_air_detector = InAirDetector(
        ulog, min_flight_time_seconds=0.0, in_air_margin_seconds=0.0)
    airtimes = in_air_detector.airtimes

    assert len(airtimes) == 1
    assert airtimes[0].take_off <= 0.0  # for this log the landed timestamp happends to be
    #  earlier than the start timestamp
    assert 405.9 < airtimes[0].landing <= 406.0  # 405.969268


def start_in_air(ulog):
    """

    :param ulog:
    :param ts_length:
    :return:
    """
    ts_length = ulog.get_dataset('vehicle_land_detected').data['landed'].shape[0]
    ulog.get_dataset('vehicle_land_detected').data['landed'] = np.zeros(ts_length, dtype=int)
    ulog.get_dataset('vehicle_land_detected').data['landed'][-1] = 0
    in_air_detector = InAirDetector(
        ulog, min_flight_time_seconds=0.0, in_air_margin_seconds=0.0)
    first_take_off = in_air_detector.take_off
    airtimes = in_air_detector.airtimes

    assert len(airtimes) == 1
    assert airtimes[0].take_off <= 0.0  # for this log the landed timestamp happends to be
    #  earlier than the start timestamp
    assert 405.9 < airtimes[0].landing <= 406.0  # 405.969268


def take_off_at_second_time_stamp(ulog):
    """
    tests whether
    :param ulog:
    :param ts_length:
    :return:
    """
    ts_length = ulog.get_dataset('vehicle_land_detected').data['landed'].shape[0]
    ulog.get_dataset('vehicle_land_detected').data['landed'] = np.zeros(ts_length, dtype=int)
    ulog.get_dataset('vehicle_land_detected').data['landed'][0] = 1
    in_air_detector = InAirDetector(
        ulog, min_flight_time_seconds=0.0, in_air_margin_seconds=0.0)
    airtimes = in_air_detector.airtimes
    assert len(airtimes) == 1


def multiple_take_offs(ulog):
    """
    tests whether multiple take offs can be handled by the in air detector.
    :param ulog:
    :param ts_length:
    :return:
    """
    ts_length = ulog.get_dataset('vehicle_land_detected').data['landed'].shape[0]
    ulog.get_dataset('vehicle_land_detected').data['landed'] = np.zeros(ts_length, dtype=int)
    ulog.get_dataset('vehicle_land_detected').data['landed'][int(ts_length / 2)] = 1
    ulog.get_dataset('vehicle_land_detected').data['landed'][int(ts_length / 2 + 2)] = 1
    ulog.get_dataset('vehicle_land_detected').data['landed'][int(3 * ts_length / 4)] = 1
    ulog.get_dataset('vehicle_land_detected').data['landed'][int(ts_length / 4)] = 1
    in_air_detector = InAirDetector(
        ulog, min_flight_time_seconds=0.0, in_air_margin_seconds=0.0)
    airtimes_no_margin = in_air_detector.airtimes

    assert len(airtimes_no_margin) == 5

    in_air_detector = InAirDetector(
        ulog, min_flight_time_seconds=2.0, in_air_margin_seconds=2.0)

    airtimes_margin = in_air_detector.airtimes

    margin_difference_take_off = airtimes_margin[0].take_off - airtimes_no_margin[0].take_off # 2
    margin_difference_landing = airtimes_no_margin[0].landing - airtimes_margin[0].landing # 2

    assert len(airtimes_margin) == 4
    assert 1.99 < margin_difference_take_off < 2.01, \
        'margin is not applied correctly'
    assert 1.99 < margin_difference_landing < 2.01, \
        'margin is not applied correctly'


def test_in_air_detector_on_flight_log(testing_args):
    """
    tests the basics of the in air detector using the basic test flight log file.
    :param testing_args:
    :return:
    """
    basic_test_log_filename = os.path.join(
        testing_args['test_flight_logs_path'], testing_args['simple_test_flight_log'])
    ulog = ULog(basic_test_log_filename)
    original_take_offs(ulog)


def test_basics_in_air_detector(testing_args):
    """
    tests the basics of the in air detector on a dummy log file.
    :param testing_args:
    :return:
    """

    dummy_log_filename = os.path.join(
        testing_args['test_flight_logs_path'], testing_args['dummy_log_file'])

    ulog = ULog(dummy_log_filename)

    always_on_ground(ulog)
    always_in_air(ulog)
    start_in_air(ulog)
    take_off_at_second_time_stamp(ulog)
    multiple_take_offs(ulog)
