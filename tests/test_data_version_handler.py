#! /usr/bin/env python3
"""
Testing the data version handler.
"""
import os
import pytest
from pyulog import ULog

import ecl_ekf_analysis.log_processing.data_version_handler as dvh

@pytest.fixture(scope="module")
def testing_args():
    """
    arguments for testing.
    :return: test arguments
    """
    flight_logs_path = os.path.join(os.path.dirname(__file__), 'flight_logs')
    log_est_format_v1 = ULog(os.path.join(flight_logs_path, 'short_f450_log.ulg'))
    log_est_format_v2 = ULog(os.path.join(flight_logs_path, 'estimator_innovations.ulg'))

    return {'est_format_version_1': log_est_format_v1,
            'est_format_version_2': log_est_format_v2}

def test_get_output_tracking_error_message(testing_args):
    """
        Test if the right message name will be returned for different log file versions
    """

    log_est_format_version_1 = testing_args['est_format_version_1']
    log_est_format_version_2 = testing_args['est_format_version_2']

    assert dvh.get_output_tracking_error_message(log_est_format_version_1) == "ekf2_innovations"
    assert dvh.get_output_tracking_error_message(log_est_format_version_2) == "estimator_status"

def test_get_innovation_message(testing_args):
    """
        Test if the right message name will be returned for different log file versions
    """

    log_est_format_version_1 = testing_args['est_format_version_1']
    log_est_format_version_2 = testing_args['est_format_version_2']

    assert dvh.get_innovation_message(
        log_est_format_version_1, 'innovation') == "ekf2_innovations"
    assert dvh.get_innovation_message(
        log_est_format_version_2, 'innovation') == "estimator_innovations"
    assert dvh.get_innovation_message(
        log_est_format_version_1, 'innovation_variance') == "ekf2_innovations"
    assert dvh.get_innovation_message(
        log_est_format_version_2, 'innovation_variance') == "estimator_innovation_variances"
    assert dvh.get_innovation_message(
        log_est_format_version_1, 'innovation_test_ratio') is None
    assert dvh.get_innovation_message(
        log_est_format_version_2, 'innovation_test_ratio') == "estimator_innovation_test_ratios"


test_data = [
    ("est_format_version_1", 'innovation', 'vel_pos', True),
    ("est_format_version_1", 'innovation', 'gps_vvel', False),
    ("est_format_version_1", 'innovation', 'gps_hvel', False),
    ("est_format_version_1", 'innovation', 'gps_hpos', False),
    ("est_format_version_1", 'innovation', 'gps_vpos', False),
    ("est_format_version_1", 'innovation', 'ev_hvel', False),
    ("est_format_version_1", 'innovation', 'ev_vvel', False),
    ("est_format_version_1", 'innovation', 'ev_hpos', False),
    ("est_format_version_1", 'innovation', 'ev_vpos', False),
    ("est_format_version_1", 'innovation', 'fake_hvel', False),
    ("est_format_version_1", 'innovation', 'fake_vvel', False),
    ("est_format_version_1", 'innovation', 'fake_hpos', False),
    ("est_format_version_1", 'innovation', 'fake_vpos', False),
    ("est_format_version_1", 'innovation', 'rng_vpos', False),
    ("est_format_version_1", 'innovation', 'baro_vpos', False),
    ("est_format_version_1", 'innovation', 'aux_hvel', True),
    ("est_format_version_1", 'innovation', 'aux_vvel', False),
    ("est_format_version_1", 'innovation', 'mag_field', True),
    ("est_format_version_1", 'innovation', 'heading', True),
    ("est_format_version_1", 'innovation', 'airspeed', True),
    ("est_format_version_1", 'innovation', 'beta', True),
    ("est_format_version_1", 'innovation', 'flow', True),
    ("est_format_version_1", 'innovation', 'hagl', True),
    ("est_format_version_1", 'innovation', 'drag', True),
    ("est_format_version_1", 'innovation_variance', 'vel_pos', True),
    ("est_format_version_1", 'innovation_variance', 'gps_vvel', False),
    ("est_format_version_1", 'innovation_variance', 'gps_hvel', False),
    ("est_format_version_1", 'innovation_variance', 'gps_hpos', False),
    ("est_format_version_1", 'innovation_variance', 'gps_vpos', False),
    ("est_format_version_1", 'innovation_variance', 'ev_hvel', False),
    ("est_format_version_1", 'innovation_variance', 'ev_vvel', False),
    ("est_format_version_1", 'innovation_variance', 'ev_hpos', False),
    ("est_format_version_1", 'innovation_variance', 'ev_vpos', False),
    ("est_format_version_1", 'innovation_variance', 'fake_hvel', False),
    ("est_format_version_1", 'innovation_variance', 'fake_vvel', False),
    ("est_format_version_1", 'innovation_variance', 'fake_hpos', False),
    ("est_format_version_1", 'innovation_variance', 'fake_vpos', False),
    ("est_format_version_1", 'innovation_variance', 'rng_vpos', False),
    ("est_format_version_1", 'innovation_variance', 'baro_vpos', False),
    ("est_format_version_1", 'innovation_variance', 'aux_hvel', False),
    ("est_format_version_1", 'innovation_variance', 'aux_vvel', False),
    ("est_format_version_1", 'innovation_variance', 'mag_field', True),
    ("est_format_version_1", 'innovation_variance', 'heading', True),
    ("est_format_version_1", 'innovation_variance', 'airspeed', True),
    ("est_format_version_1", 'innovation_variance', 'beta', True),
    ("est_format_version_1", 'innovation_variance', 'flow', True),
    ("est_format_version_1", 'innovation_variance', 'hagl', True),
    ("est_format_version_1", 'innovation_variance', 'drag', True),
    ("est_format_version_1", 'innovation_test_ratio', 'hgt', True),
    ("est_format_version_1", 'innovation_test_ratio', 'vel', True),
    ("est_format_version_1", 'innovation_test_ratio', 'pos', True),
    ("est_format_version_1", 'innovation_test_ratio', 'gps_vvel', False),
    ("est_format_version_1", 'innovation_test_ratio', 'gps_hvel', False),
    ("est_format_version_1", 'innovation_test_ratio', 'gps_hpos', False),
    ("est_format_version_1", 'innovation_test_ratio', 'gps_vpos', False),
    ("est_format_version_1", 'innovation_test_ratio', 'ev_hvel', False),
    ("est_format_version_1", 'innovation_test_ratio', 'ev_vvel', False),
    ("est_format_version_1", 'innovation_test_ratio', 'ev_hpos', False),
    ("est_format_version_1", 'innovation_test_ratio', 'ev_vpos', False),
    ("est_format_version_1", 'innovation_test_ratio', 'fake_hvel', False),
    ("est_format_version_1", 'innovation_test_ratio', 'fake_vvel', False),
    ("est_format_version_1", 'innovation_test_ratio', 'fake_hpos', False),
    ("est_format_version_1", 'innovation_test_ratio', 'fake_vpos', False),
    ("est_format_version_1", 'innovation_test_ratio', 'rng_vpos', False),
    ("est_format_version_1", 'innovation_test_ratio', 'baro_vpos', False),
    ("est_format_version_1", 'innovation_test_ratio', 'aux_hvel', False),
    ("est_format_version_1", 'innovation_test_ratio', 'aux_vvel', False),
    ("est_format_version_1", 'innovation_test_ratio', 'mag_field', True),
    ("est_format_version_1", 'innovation_test_ratio', 'heading', False),
    ("est_format_version_1", 'innovation_test_ratio', 'airspeed', True),
    ("est_format_version_1", 'innovation_test_ratio', 'beta', True),
    ("est_format_version_1", 'innovation_test_ratio', 'flow', False),
    ("est_format_version_1", 'innovation_test_ratio', 'hagl', True),
    ("est_format_version_1", 'innovation_test_ratio', 'drag', False),
    ("est_format_version_2", 'innovation', 'vel_pos', False),
    ("est_format_version_2", 'innovation', 'gps_vvel', True),
    ("est_format_version_2", 'innovation', 'gps_hvel', True),
    ("est_format_version_2", 'innovation', 'gps_hpos', True),
    ("est_format_version_2", 'innovation', 'gps_vpos', True),
    ("est_format_version_2", 'innovation', 'ev_hvel', True),
    ("est_format_version_2", 'innovation', 'ev_vvel', True),
    ("est_format_version_2", 'innovation', 'ev_hpos', True),
    ("est_format_version_2", 'innovation', 'ev_vpos', True),
    ("est_format_version_2", 'innovation', 'fake_hvel', True),
    ("est_format_version_2", 'innovation', 'fake_vvel', True),
    ("est_format_version_2", 'innovation', 'fake_hpos', True),
    ("est_format_version_2", 'innovation', 'fake_vpos', True),
    ("est_format_version_2", 'innovation', 'rng_vpos', True),
    ("est_format_version_2", 'innovation', 'baro_vpos', True),
    ("est_format_version_2", 'innovation', 'aux_hvel', True),
    ("est_format_version_2", 'innovation', 'aux_vvel', True),
    ("est_format_version_2", 'innovation', 'mag_field', True),
    ("est_format_version_2", 'innovation', 'heading', True),
    ("est_format_version_2", 'innovation', 'airspeed', True),
    ("est_format_version_2", 'innovation', 'beta', True),
    ("est_format_version_2", 'innovation', 'flow', True),
    ("est_format_version_2", 'innovation', 'hagl', True),
    ("est_format_version_2", 'innovation', 'drag', True),
    ("est_format_version_2", 'innovation_variance', 'vel_pos', False),
    ("est_format_version_2", 'innovation_variance', 'gps_vvel', True),
    ("est_format_version_2", 'innovation_variance', 'gps_hvel', True),
    ("est_format_version_2", 'innovation_variance', 'gps_hpos', True),
    ("est_format_version_2", 'innovation_variance', 'gps_vpos', True),
    ("est_format_version_2", 'innovation_variance', 'ev_hvel', True),
    ("est_format_version_2", 'innovation_variance', 'ev_vvel', True),
    ("est_format_version_2", 'innovation_variance', 'ev_hpos', True),
    ("est_format_version_2", 'innovation_variance', 'ev_vpos', True),
    ("est_format_version_2", 'innovation_variance', 'fake_hvel', True),
    ("est_format_version_2", 'innovation_variance', 'fake_vvel', True),
    ("est_format_version_2", 'innovation_variance', 'fake_hpos', True),
    ("est_format_version_2", 'innovation_variance', 'fake_vpos', True),
    ("est_format_version_2", 'innovation_variance', 'rng_vpos', True),
    ("est_format_version_2", 'innovation_variance', 'baro_vpos', True),
    ("est_format_version_2", 'innovation_variance', 'aux_hvel', True),
    ("est_format_version_2", 'innovation_variance', 'aux_vvel', True),
    ("est_format_version_2", 'innovation_variance', 'mag_field', True),
    ("est_format_version_2", 'innovation_variance', 'heading', True),
    ("est_format_version_2", 'innovation_variance', 'airspeed', True),
    ("est_format_version_2", 'innovation_variance', 'beta', True),
    ("est_format_version_2", 'innovation_variance', 'flow', True),
    ("est_format_version_2", 'innovation_variance', 'hagl', True),
    ("est_format_version_2", 'innovation_variance', 'drag', True),
    ("est_format_version_2", 'innovation_test_ratio', 'hgt', False),
    ("est_format_version_2", 'innovation_test_ratio', 'vel', False),
    ("est_format_version_2", 'innovation_test_ratio', 'pos', False),
    ("est_format_version_2", 'innovation_test_ratio', 'gps_vvel', True),
    ("est_format_version_2", 'innovation_test_ratio', 'gps_hvel', True),
    ("est_format_version_2", 'innovation_test_ratio', 'gps_hpos', True),
    ("est_format_version_2", 'innovation_test_ratio', 'gps_vpos', True),
    ("est_format_version_2", 'innovation_test_ratio', 'ev_hvel', True),
    ("est_format_version_2", 'innovation_test_ratio', 'ev_vvel', True),
    ("est_format_version_2", 'innovation_test_ratio', 'ev_hpos', True),
    ("est_format_version_2", 'innovation_test_ratio', 'ev_vpos', True),
    ("est_format_version_2", 'innovation_test_ratio', 'fake_hvel', True),
    ("est_format_version_2", 'innovation_test_ratio', 'fake_vvel', True),
    ("est_format_version_2", 'innovation_test_ratio', 'fake_hpos', True),
    ("est_format_version_2", 'innovation_test_ratio', 'fake_vpos', True),
    ("est_format_version_2", 'innovation_test_ratio', 'rng_vpos', True),
    ("est_format_version_2", 'innovation_test_ratio', 'baro_vpos', True),
    ("est_format_version_2", 'innovation_test_ratio', 'aux_hvel', True),
    ("est_format_version_2", 'innovation_test_ratio', 'aux_vvel', True),
    ("est_format_version_2", 'innovation_test_ratio', 'mag_field', True),
    ("est_format_version_2", 'innovation_test_ratio', 'heading', True),
    ("est_format_version_2", 'innovation_test_ratio', 'airspeed', True),
    ("est_format_version_2", 'innovation_test_ratio', 'beta', True),
    ("est_format_version_2", 'innovation_test_ratio', 'flow', True),
    ("est_format_version_2", 'innovation_test_ratio', 'hagl', True),
    ("est_format_version_2", 'innovation_test_ratio', 'drag', True),
]

@pytest.mark.parametrize(
    "est_format_version,message_descriptor,field_name_req,should_exist", test_data)

def test_get_field_name_from_message_and_descriptor(
        testing_args, est_format_version, message_descriptor, field_name_req, should_exist):
    """
        Test logs of different verison for the existence/inexistence
        of innovation and innovation_variance fields
    """
    log = testing_args[est_format_version]

    message_name, field_name = dvh.get_innovation_message_and_field_name(
        log, field_name_req, message_descriptor)
    print(message_name, field_name)
    assert dvh.check_if_field_name_exists_in_message(log, message_name, field_name) == should_exist
