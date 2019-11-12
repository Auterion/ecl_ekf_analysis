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

def test_get_field_name_from_message_and_descriptor():
    """
     Test if the return field name for different messages is correct
    """

    assert dvh.get_field_name_from_message_and_descriptor(
        'ekf2_innovations', 'magnetometer_innovation') == 'mag_innov'
    assert dvh.get_field_name_from_message_and_descriptor(
        'ekf2_innovations', 'magnetometer_innovation_variance') == 'mag_innov_var'

    assert dvh.get_field_name_from_message_and_descriptor(
        'estimator_innovations', 'magnetometer_innovation') == 'mag'
    assert dvh.get_field_name_from_message_and_descriptor(
        'estimator_innovation_variances', 'magnetometer_innovation_variance') == 'mag'
