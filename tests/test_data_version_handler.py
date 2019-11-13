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

    assert dvh.get_innovation_message(log_est_format_version_1) == "ekf2_innovations"
    assert dvh.get_innovation_message(log_est_format_version_2) == "estimator_innovations"

def test_get_innovation_variance_message(testing_args):
    """
        Test if the right message name will be returned for different log file versions
    """

    log_est_format_version_1 = testing_args['est_format_version_1']
    log_est_format_version_2 = testing_args['est_format_version_2']

    assert dvh.get_innovation_variance_message(
        log_est_format_version_1) == "ekf2_innovations"
    assert dvh.get_innovation_variance_message(
        log_est_format_version_2) == "estimator_innovation_variances"


test_data = [
    ("est_format_version_1", 'innovation', 'vel_pos_innovation', True),
    ("est_format_version_1", 'innovation', 'gps_vvel_innovation', False),
    ("est_format_version_1", 'innovation', 'gps_hvel_innovation', False),
    ("est_format_version_1", 'innovation', 'gps_hpos_innovation', False),
    ("est_format_version_1", 'innovation', 'gps_vpos_innovation', False),
    ("est_format_version_1", 'innovation', 'vision_hvel_innovation', False),
    ("est_format_version_1", 'innovation', 'vision_vvel_innovation', False),
    ("est_format_version_1", 'innovation', 'vision_hpos_innovation', False),
    ("est_format_version_1", 'innovation', 'vision_vpos_innovation', False),
    ("est_format_version_1", 'innovation', 'fake_hvel_innovation', False),
    ("est_format_version_1", 'innovation', 'fake_vvel_innovation', False),
    ("est_format_version_1", 'innovation', 'fake_hpos_innovation', False),
    ("est_format_version_1", 'innovation', 'fake_vpos_innovation', False),
    ("est_format_version_1", 'innovation', 'rng_vpos_innovation', False),
    ("est_format_version_1", 'innovation', 'baro_vpos_innovation', False),
    ("est_format_version_1", 'innovation', 'aux_hvel_innovation', True),
    ("est_format_version_1", 'innovation', 'aux_vvel_innovation', False),
    ("est_format_version_1", 'innovation', 'mag_field_innovation', True),
    ("est_format_version_1", 'innovation', 'heading_innovation', True),
    ("est_format_version_1", 'innovation', 'airspeed_innovation', True),
    ("est_format_version_1", 'innovation', 'sideslip_innovation', True),
    ("est_format_version_1", 'innovation', 'flow_innovation', True),
    ("est_format_version_1", 'innovation', 'hagl_innovation', True),
    ("est_format_version_1", 'innovation', 'drag_innovation', True),
    ("est_format_version_1", 'innovation_variance', 'vel_pos_innovation_variance', True),
    ("est_format_version_1", 'innovation_variance', 'gps_vvel_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'gps_hvel_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'gps_hpos_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'gps_vpos_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'vision_hvel_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'vision_vvel_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'vision_hpos_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'vision_vpos_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'fake_hvel_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'fake_vvel_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'fake_hpos_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'fake_vpos_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'rng_vpos_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'baro_vpos_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'aux_hvel_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'aux_vvel_innovation_variance', False),
    ("est_format_version_1", 'innovation_variance', 'mag_field_innovation_variance', True),
    ("est_format_version_1", 'innovation_variance', 'heading_innovation_variance', True),
    ("est_format_version_1", 'innovation_variance', 'airspeed_innovation_variance', True),
    ("est_format_version_1", 'innovation_variance', 'sideslip_innovation_variance', True),
    ("est_format_version_1", 'innovation_variance', 'flow_innovation_variance', True),
    ("est_format_version_1", 'innovation_variance', 'hagl_innovation_variance', True),
    ("est_format_version_1", 'innovation_variance', 'drag_innovation_variance', True),
    ("est_format_version_2", 'innovation', 'vel_pos_innovation', False),
    ("est_format_version_2", 'innovation', 'gps_vvel_innovation', True),
    ("est_format_version_2", 'innovation', 'gps_hvel_innovation', True),
    ("est_format_version_2", 'innovation', 'gps_hpos_innovation', True),
    ("est_format_version_2", 'innovation', 'gps_vpos_innovation', True),
    ("est_format_version_2", 'innovation', 'vision_hvel_innovation', True),
    ("est_format_version_2", 'innovation', 'vision_vvel_innovation', True),
    ("est_format_version_2", 'innovation', 'vision_hpos_innovation', True),
    ("est_format_version_2", 'innovation', 'vision_vpos_innovation', True),
    ("est_format_version_2", 'innovation', 'fake_hvel_innovation', True),
    ("est_format_version_2", 'innovation', 'fake_vvel_innovation', True),
    ("est_format_version_2", 'innovation', 'fake_hpos_innovation', True),
    ("est_format_version_2", 'innovation', 'fake_vpos_innovation', True),
    ("est_format_version_2", 'innovation', 'rng_vpos_innovation', True),
    ("est_format_version_2", 'innovation', 'baro_vpos_innovation', True),
    ("est_format_version_2", 'innovation', 'aux_hvel_innovation', True),
    ("est_format_version_2", 'innovation', 'aux_vvel_innovation', True),
    ("est_format_version_2", 'innovation', 'mag_field_innovation', True),
    ("est_format_version_2", 'innovation', 'heading_innovation', True),
    ("est_format_version_2", 'innovation', 'airspeed_innovation', True),
    ("est_format_version_2", 'innovation', 'sideslip_innovation', True),
    ("est_format_version_2", 'innovation', 'flow_innovation', True),
    ("est_format_version_2", 'innovation', 'hagl_innovation', True),
    ("est_format_version_2", 'innovation', 'drag_innovation', True),
    ("est_format_version_2", 'innovation_variance', 'vel_pos_innovation_variance', False),
    ("est_format_version_2", 'innovation_variance', 'gps_vvel_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'gps_hvel_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'gps_hpos_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'gps_vpos_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'vision_hvel_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'vision_vvel_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'vision_hpos_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'vision_vpos_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'fake_hvel_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'fake_vvel_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'fake_hpos_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'fake_vpos_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'rng_vpos_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'baro_vpos_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'aux_hvel_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'aux_vvel_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'mag_field_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'heading_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'airspeed_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'sideslip_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'flow_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'hagl_innovation_variance', True),
    ("est_format_version_2", 'innovation_variance', 'drag_innovation_variance', True),
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

    message_name = ""
    if message_descriptor == "innovation":
        message_name = dvh.get_innovation_message(log)
    if message_descriptor == "innovation_variance":
        message_name = dvh.get_innovation_variance_message(log)

    field_name = dvh.get_field_name_from_message_and_descriptor(message_name, field_name_req)

    assert dvh.check_if_field_name_exists_in_message(log, message_name, field_name) == should_exist
