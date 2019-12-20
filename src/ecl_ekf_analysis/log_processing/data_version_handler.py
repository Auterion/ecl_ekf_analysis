#! /usr/bin/env python3
"""
function collection for handling different versions of log files
"""
from typing import Tuple

from pyulog import ULog

from ecl_ekf_analysis.log_processing.custom_exceptions import PreconditionError

def get_output_tracking_error_message(ulog: ULog) -> str:
    """
    return the name of the message containing the output_tracking_error
    :param ulog:
    :return: str
    """
    for elem in  ulog.data_list:
        if elem.name == "ekf2_innovations":
            return "ekf2_innovations"
        if elem.name == "estimator_innovations":
            return "estimator_status"

    raise PreconditionError("Could not detect the message containing the output tracking error")

def get_innovation_message(ulog: ULog, topic: str = 'innovation') -> str:
    """
    return the name of the innovation message (old: ekf2_innovations; new: estimator_innovations)
    :param ulog:
    :return: str
    """
    if topic == 'innovation':
        for elem in  ulog.data_list:
            if elem.name == "ekf2_innovations":
                return "ekf2_innovations"
            if elem.name == "estimator_innovations":
                return "estimator_innovations"
    if topic == 'innovation_variance':
        for elem in  ulog.data_list:
            if elem.name == "ekf2_innovations":
                return "ekf2_innovations"
            if elem.name == "estimator_innovations":
                return "estimator_innovation_variances"
    if topic == 'innovation_test_ratio':
        for elem in  ulog.data_list:
            if elem.name == "ekf2_innovations":
                return None
            if elem.name == "estimator_innovations":
                return "estimator_innovation_test_ratios"

    raise PreconditionError("Could not detect the message")

def get_field_name_from_message_and_descriptor(
        message: str, field_descriptor: str, topic: str = 'innovation') -> str:
    """
    return the actual field name for a field descriptor
    e.g. message: ekf2_innovations; field_descriptor: magnetometer_innovations -> mag_innov
    :param ulog:
    :return: str (if field not found, None will be returned)
    """
    if topic == 'innovation':
        msg_lookUp_dict = {
            'ekf2_innovations' :
                {
                    'vel_pos' : 'vel_pos_innov',
                    'aux_hvel' : 'aux_vel_innov',
                    'mag_field' : 'mag_innov',
                    'heading' : 'heading_innov',
                    'airspeed' : 'airspeed_innov',
                    'beta' : 'beta_innov',
                    'flow' : 'flow_innov',
                    'hagl' : 'hagl_innov',
                    'drag' : 'drag_innov'
                },
            'estimator_innovations' :
                {
                    'gps_hvel' : 'gps_hvel',
                    'gps_vvel' : 'gps_vvel',
                    'gps_hpos' : 'gps_hpos',
                    'gps_vpos' : 'gps_vpos',
                    'ev_hvel' : 'ev_hvel',
                    'ev_vvel' : 'ev_vvel',
                    'ev_hpos' : 'ev_hpos',
                    'ev_vpos' : 'ev_vpos',
                    'fake_hvel' : 'fake_hvel',
                    'fake_vvel' : 'fake_vvel',
                    'fake_hpos' : 'fake_hpos',
                    'fake_vpos' : 'fake_vpos',
                    'rng_vpos' : 'rng_vpos',
                    'baro_vpos' : 'baro_vpos',
                    'aux_hvel' : 'aux_hvel',
                    'aux_vvel' : 'aux_vvel',
                    'mag_field' : 'mag_field',
                    'heading' : 'heading',
                    'airspeed' : 'airspeed',
                    'beta' : 'beta',
                    'flow' : 'flow',
                    'hagl' : 'hagl',
                    'drag' : 'drag'
                }
            }
        field = msg_lookUp_dict[message].get(field_descriptor, None)
        return field
    if topic == 'innovation_variance':
        msg_lookUp_dict = {
            'ekf2_innovations' :
                {
                    'vel_pos' : 'vel_pos_innov_var',
                    'aux_hvel' : 'aux_vel_innov_var',
                    'mag_field' : 'mag_innov_var',
                    'heading' : 'heading_innov_var',
                    'airspeed' : 'airspeed_innov_var',
                    'beta' : 'beta_innov_var',
                    'flow' : 'flow_innov_var',
                    'hagl' : 'hagl_innov_var',
                    'drag' : 'drag_innov_var'
                },
            'estimator_innovation_variances' :
                {
                    'gps_hvel' : 'gps_hvel',
                    'gps_vvel' : 'gps_vvel',
                    'gps_hpos' : 'gps_hpos',
                    'gps_vpos' : 'gps_vpos',
                    'ev_hvel' : 'ev_hvel',
                    'ev_vvel' : 'ev_vvel',
                    'ev_hpos' : 'ev_hpos',
                    'ev_vpos' : 'ev_vpos',
                    'fake_hvel' : 'fake_hvel',
                    'fake_vvel' : 'fake_vvel',
                    'fake_hpos' : 'fake_hpos',
                    'fake_vpos' : 'fake_vpos',
                    'rng_vpos' : 'rng_vpos',
                    'baro_vpos' : 'baro_vpos',
                    'aux_hvel' : 'aux_hvel',
                    'aux_vvel' : 'aux_vvel',
                    'mag_field' : 'mag_field',
                    'heading' : 'heading',
                    'airspeed' : 'airspeed',
                    'beta' : 'beta',
                    'flow' : 'flow',
                    'hagl' : 'hagl',
                    'drag' : 'drag'
                }
            }
        field = msg_lookUp_dict[message].get(field_descriptor, None)
        return field
    if topic == 'innovation_test_ratio':
        msg_lookUp_dict = {
            'estimator_status' :
                {
                    'pos' : 'pos_test_ratio',
                    'vel' : 'vel_test_ratio',
                    'hgt' : 'hgt_test_ratio',
                    'mag_field' : 'mag_test_ratio',
                    'airspeed' : 'tas_test_ratio',
                    'beta' : 'beta_test_ratio',
                    'hagl' : 'hagl_test_ratio',

                },
            'estimator_innovation_test_ratios' :
                {
                    'gps_hvel' : 'gps_hvel',
                    'gps_vvel' : 'gps_vvel',
                    'gps_hpos' : 'gps_hpos',
                    'gps_vpos' : 'gps_vpos',
                    'ev_hvel' : 'ev_hvel',
                    'ev_vvel' : 'ev_vvel',
                    'ev_hpos' : 'ev_hpos',
                    'ev_vpos' : 'ev_vpos',
                    'fake_hvel' : 'fake_hvel',
                    'fake_vvel' : 'fake_vvel',
                    'fake_hpos' : 'fake_hpos',
                    'fake_vpos' : 'fake_vpos',
                    'rng_vpos' : 'rng_vpos',
                    'baro_vpos' : 'baro_vpos',
                    'aux_hvel' : 'aux_hvel',
                    'aux_vvel' : 'aux_vvel',
                    'mag_field' : 'mag_field',
                    'heading' : 'heading',
                    'airspeed' : 'airspeed',
                    'beta' : 'beta',
                    'flow' : 'flow',
                    'hagl' : 'hagl',
                    'drag' : 'drag'
                }
        }
        field = msg_lookUp_dict[message].get(field_descriptor, None)
        return field

    return None


def check_if_field_name_exists_in_message(ulog: ULog, message_name: str, field_name: str) -> bool:
    """
        Check if a field is part of a message in a certain log
    """
    if field_name is None:
        return False

    msg_data = ulog.get_dataset(message_name).data
    field_name_list = dict.keys(msg_data)

    for elem in field_name_list:
        if field_name == field_name_wo_brackets(elem):
            return True

    return False

def field_name_wo_brackets(field_name: str) -> str:
    """
        Field names in a ulog message can end with [*]. This function removes the [*] at the end
    """
    if field_name.endswith(']'):
        return field_name[:-3]
    return field_name

def get_innovation_message_and_field_name(
        ulog: ULog, field_descriptor: str, topic: str = 'innovation') -> Tuple[str, str]:
    """
    :param ulog:
    :param field_descriptor:
    :param type:
    :return:
    """
    messages = {elem.name for elem in ulog.data_list}
    message = None
    field_name = None
    if 'estimator_innovations' in messages:
        if topic == 'innovation':
            message = 'estimator_innovations'
            field_name = field_descriptor
        elif topic == 'innovation_variance':
            message = 'estimator_innovation_variances'
            field_name = field_descriptor
        elif topic == 'innovation_test_ratio':
            message = 'estimator_innovation_test_ratios'
            field_name = field_descriptor
    else:
        # Old topics
        if topic == 'innovation':
            message = 'ekf2_innovations'
            field_name = get_field_name_from_message_and_descriptor(
                message, field_descriptor, topic)
        elif topic == 'innovation_variance':
            message = 'ekf2_innovations'
            field_name = get_field_name_from_message_and_descriptor(
                message, field_descriptor, topic)
        elif topic == 'innovation_test_ratio':
            message = 'estimator_status'
            field_name = get_field_name_from_message_and_descriptor(
                message, field_descriptor, topic)
    return message, field_name
