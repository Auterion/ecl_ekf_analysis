#! /usr/bin/env python3
"""
Testing the data version handler.
"""
import os
import pytest
from pyulog import ULog

import ecl_ekf_analysis.log_processing.data_version_handling as dvh


@pytest.fixture(scope="module")
def testing_args():
    """
    arguments for testing.
    :return: test arguments
    """
    flight_logs_path = os.path.join(os.path.dirname(__file__), 'flight_logs')
    log_est_format_v1 = ULog(os.path.join(flight_logs_path, 'short_f450_log.ulg'))
    log_est_format_v2 = ULog(os.path.join(flight_logs_path, 'estimator_innovations.ulg'))

    return {'log_est_format_v1': log_est_format_v1,
            'log_est_format_v2': log_est_format_v2}


def test_get_output_tracking_error_message(testing_args):
    """
        Test if the right message name will be returned for different log file versions
    """

    log_est_format_v1 = testing_args['log_est_format_v1']
    log_est_format_v2 = testing_args['log_est_format_v2']

    output_tracking_error_message = dvh.get_output_tracking_error_message(log_est_format_v1)
    assert output_tracking_error_message == "ekf2_innovations", \
        'returned innovation message {:s} was not ekf2_innovations'.format(
            output_tracking_error_message)
    output_tracking_error_message = dvh.get_output_tracking_error_message(log_est_format_v2)
    assert output_tracking_error_message == "estimator_status", \
        'returned innovation message {:s} was not estimator_status'.format(
            output_tracking_error_message)


def test_get_innovation_message(testing_args):
    """
        Test if the right message name will be returned for different log file versions
    """

    log_est_format_v1 = testing_args['log_est_format_v1']
    log_est_format_v2 = testing_args['log_est_format_v2']

    innovation_message = dvh.get_innovation_message(log_est_format_v1, topic='innovation')
    assert innovation_message == "ekf2_innovations", \
        'returned innovation message {:s} was not ekf2_innovations'.format(innovation_message)
    innovation_message = dvh.get_innovation_message(log_est_format_v2, topic='innovation')
    assert innovation_message == "estimator_innovations", \
        'returned innovation message {:s} was not estimator_innovations'.format(innovation_message)

    innovation_variance_message = dvh.get_innovation_message(
        log_est_format_v1, topic='innovation_variance')
    assert innovation_variance_message == "ekf2_innovations", \
        'returned innovation message {:s} was not ekf2_innovations'.format(
            innovation_variance_message)
    innovation_variance_message = dvh.get_innovation_message(
        log_est_format_v2, topic='innovation_variance')
    assert innovation_variance_message == "estimator_innovation_variances", \
        'returned innovation message {:s} was not estimator_innovation_variances'.format(
            innovation_variance_message)

    innovation_test_ratio_message = dvh.get_innovation_message(
        log_est_format_v1, topic='innovation_test_ratio')
    assert innovation_test_ratio_message == "estimator_status", \
        'returned innovation message {:s} was not estimator_status'.format(
            innovation_test_ratio_message)
    innovation_test_ratio_message = dvh.get_innovation_message(
        log_est_format_v2, topic='innovation_test_ratio')
    assert innovation_test_ratio_message == "estimator_innovation_test_ratios", \
        'returned innovation message {:s} was not estimator_innovation_test_ratios'.format(
            innovation_test_ratio_message)


test_data = [
    ("log_est_format_v1", 'innovation', 'aux_hvel', True),
    ("log_est_format_v1", 'innovation', 'mag_field', True),
    ("log_est_format_v1", 'innovation', 'heading', True),
    ("log_est_format_v1", 'innovation', 'airspeed', True),
    ("log_est_format_v1", 'innovation', 'beta', True),
    ("log_est_format_v1", 'innovation', 'flow', True),
    ("log_est_format_v1", 'innovation', 'hagl', True),
    ("log_est_format_v1", 'innovation', 'drag', True),
    ("log_est_format_v1", 'innovation_variance', 'aux_hvel', False),
    ("log_est_format_v1", 'innovation_variance', 'mag_field', True),
    ("log_est_format_v1", 'innovation_variance', 'heading', True),
    ("log_est_format_v1", 'innovation_variance', 'airspeed', True),
    ("log_est_format_v1", 'innovation_variance', 'beta', True),
    ("log_est_format_v1", 'innovation_variance', 'flow', True),
    ("log_est_format_v1", 'innovation_variance', 'hagl', True),
    ("log_est_format_v1", 'innovation_variance', 'drag', True),
    ("log_est_format_v1", 'innovation_test_ratio', 'mag_field', True),
    ("log_est_format_v1", 'innovation_test_ratio', 'airspeed', True),
    ("log_est_format_v1", 'innovation_test_ratio', 'beta', True),
    ("log_est_format_v1", 'innovation_test_ratio', 'hagl', True),
    ("log_est_format_v2", 'innovation', 'vel_pos', False),
    ("log_est_format_v2", 'innovation', 'gps_vvel', True),
    ("log_est_format_v2", 'innovation', 'gps_hvel', True),
    ("log_est_format_v2", 'innovation', 'gps_hpos', True),
    ("log_est_format_v2", 'innovation', 'gps_vpos', True),
    ("log_est_format_v2", 'innovation', 'ev_hvel', True),
    ("log_est_format_v2", 'innovation', 'ev_vvel', True),
    ("log_est_format_v2", 'innovation', 'ev_hpos', True),
    ("log_est_format_v2", 'innovation', 'ev_vpos', True),
    ("log_est_format_v2", 'innovation', 'fake_hvel', True),
    ("log_est_format_v2", 'innovation', 'fake_vvel', True),
    ("log_est_format_v2", 'innovation', 'fake_hpos', True),
    ("log_est_format_v2", 'innovation', 'fake_vpos', True),
    ("log_est_format_v2", 'innovation', 'rng_vpos', True),
    ("log_est_format_v2", 'innovation', 'baro_vpos', True),
    ("log_est_format_v2", 'innovation', 'aux_hvel', True),
    ("log_est_format_v2", 'innovation', 'aux_vvel', True),
    ("log_est_format_v2", 'innovation', 'mag_field', True),
    ("log_est_format_v2", 'innovation', 'heading', True),
    ("log_est_format_v2", 'innovation', 'airspeed', True),
    ("log_est_format_v2", 'innovation', 'beta', True),
    ("log_est_format_v2", 'innovation', 'flow', True),
    ("log_est_format_v2", 'innovation', 'hagl', True),
    ("log_est_format_v2", 'innovation', 'drag', True),
    ("log_est_format_v2", 'innovation_variance', 'vel_pos', False),
    ("log_est_format_v2", 'innovation_variance', 'gps_vvel', True),
    ("log_est_format_v2", 'innovation_variance', 'gps_hvel', True),
    ("log_est_format_v2", 'innovation_variance', 'gps_hpos', True),
    ("log_est_format_v2", 'innovation_variance', 'gps_vpos', True),
    ("log_est_format_v2", 'innovation_variance', 'ev_hvel', True),
    ("log_est_format_v2", 'innovation_variance', 'ev_vvel', True),
    ("log_est_format_v2", 'innovation_variance', 'ev_hpos', True),
    ("log_est_format_v2", 'innovation_variance', 'ev_vpos', True),
    ("log_est_format_v2", 'innovation_variance', 'fake_hvel', True),
    ("log_est_format_v2", 'innovation_variance', 'fake_vvel', True),
    ("log_est_format_v2", 'innovation_variance', 'fake_hpos', True),
    ("log_est_format_v2", 'innovation_variance', 'fake_vpos', True),
    ("log_est_format_v2", 'innovation_variance', 'rng_vpos', True),
    ("log_est_format_v2", 'innovation_variance', 'baro_vpos', True),
    ("log_est_format_v2", 'innovation_variance', 'aux_hvel', True),
    ("log_est_format_v2", 'innovation_variance', 'aux_vvel', True),
    ("log_est_format_v2", 'innovation_variance', 'mag_field', True),
    ("log_est_format_v2", 'innovation_variance', 'heading', True),
    ("log_est_format_v2", 'innovation_variance', 'airspeed', True),
    ("log_est_format_v2", 'innovation_variance', 'beta', True),
    ("log_est_format_v2", 'innovation_variance', 'flow', True),
    ("log_est_format_v2", 'innovation_variance', 'hagl', True),
    ("log_est_format_v2", 'innovation_variance', 'drag', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'hgt', False),
    ("log_est_format_v2", 'innovation_test_ratio', 'vel', False),
    ("log_est_format_v2", 'innovation_test_ratio', 'pos', False),
    ("log_est_format_v2", 'innovation_test_ratio', 'gps_vvel', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'gps_hvel', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'gps_hpos', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'gps_vpos', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'ev_hvel', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'ev_vvel', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'ev_hpos', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'ev_vpos', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'fake_hvel', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'fake_vvel', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'fake_hpos', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'fake_vpos', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'rng_vpos', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'baro_vpos', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'aux_hvel', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'aux_vvel', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'mag_field', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'heading', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'airspeed', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'beta', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'flow', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'hagl', True),
    ("log_est_format_v2", 'innovation_test_ratio', 'drag', True),
]

@pytest.mark.parametrize(
    "est_format_version,topic,field_name_req,should_exist", test_data)

def test_get_field_name_from_message_and_descriptor(
        testing_args, est_format_version, topic, field_name_req, should_exist):
    """
        Test logs of different verison for the existence/inexistence
        of innovation and innovation_variance fields
    """
    log = testing_args[est_format_version]

    message_name, field_name = dvh.get_innovation_message_and_field_name(
        log, field_name_req, topic=topic)
    print(message_name, field_name)
    assert dvh.check_if_field_name_exists_in_message(log, message_name, field_name) == should_exist
