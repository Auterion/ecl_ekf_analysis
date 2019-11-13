#! /usr/bin/env python3
"""
function collection for handling different versions of log files
"""
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

def get_innovation_message(ulog: ULog) -> str:
    """
    return the name of the innovation message (old: ekf2_innovations; new: estimator_innovations)
    :param ulog:
    :return: str
    """
    for elem in  ulog.data_list:
        if elem.name == "ekf2_innovations":
            return "ekf2_innovations"
        if elem.name == "estimator_innovations":
            return "estimator_innovations"

    raise PreconditionError("Could not detect any known innovation message")

def get_innovation_variance_message(ulog: ULog) -> str:
    """
    return the name of the innovation variance message
    :param ulog:
    :return: str
    """
    for elem in  ulog.data_list:
        if elem.name == "ekf2_innovations":
            return "ekf2_innovations"
        if elem.name == "estimator_innovations":
            return "estimator_innovation_variances"

    raise PreconditionError("Could not detect any known innovation message")

def get_field_name_from_message_and_descriptor(message: str, field_descriptor: str) -> str:
    """
    return the actual field name for a field descriptor
    e.g. message: ekf2_innovations; field_descriptor: magnetometer_innovations -> mag_innov
    :param ulog:
    :return: str (if field not found, None will be returned)
    """
    msg_lookUp_dict = {
        'ekf2_innovations' :
            {
                'vel_pos_innovation' : 'vel_pos_innov',
                'aux_hvel_innovation' : 'aux_vel_innov',
                'mag_field_innovation' : 'mag_innov',
                'heading_innovation' : 'heading_innov',
                'airspeed_innovation' : 'airspeed_innov',
                'sideslip_innovation' : 'beta_innov',
                'flow_innovation' : 'flow_innov',
                'hagl_innovation' : 'hagl_innov',
                'drag_innovation' : 'drag_innov',
                'vel_pos_innovation_variance' : 'vel_pos_innov_var',
                'mag_field_innovation_variance' : 'mag_innov_var',
                'heading_innovation_variance' : 'heading_innov_var',
                'airspeed_innovation_variance' : 'airspeed_innov_var',
                'sideslip_innovation_variance' : 'beta_innov_var',
                'flow_innovation_variance' : 'flow_innov_var',
                'hagl_innovation_variance' : 'hagl_innov_var',
                'drag_innovation_variance' : 'drag_innov_var'
            },
        'estimator_innovations' :
            {
                'gps_hvel_innovation' : 'gps_hvel',
                'gps_vvel_innovation' : 'gps_vvel',
                'gps_hpos_innovation' : 'gps_hpos',
                'gps_vpos_innovation' : 'gps_vpos',
                'vision_hvel_innovation' : 'ev_hvel',
                'vision_vvel_innovation' : 'ev_vvel',
                'vision_hpos_innovation' : 'ev_hpos',
                'vision_vpos_innovation' : 'ev_vpos',
                'fake_hvel_innovation' : 'fake_hvel',
                'fake_vvel_innovation' : 'fake_vvel',
                'fake_hpos_innovation' : 'fake_hpos',
                'fake_vpos_innovation' : 'fake_vpos',
                'rng_vpos_innovation' : 'rng_vpos',
                'baro_vpos_innovation' : 'baro_vpos',
                'aux_hvel_innovation' : 'aux_hvel',
                'aux_vvel_innovation' : 'aux_vvel',
                'mag_field_innovation' : 'mag_field',
                'heading_innovation' : 'heading',
                'airspeed_innovation' : 'airspeed',
                'sideslip_innovation' : 'beta',
                'flow_innovation' : 'flow',
                'hagl_innovation' : 'hagl',
                'drag_innovation' : 'drag',
            },
        'estimator_innovation_variances' :
            {
                'gps_hvel_innovation_variance' : 'gps_hvel',
                'gps_vvel_innovation_variance' : 'gps_vvel',
                'gps_hpos_innovation_variance' : 'gps_hpos',
                'gps_vpos_innovation_variance' : 'gps_vpos',
                'vision_hvel_innovation_variance' : 'ev_hvel',
                'vision_vvel_innovation_variance' : 'ev_vvel',
                'vision_hpos_innovation_variance' : 'ev_hpos',
                'vision_vpos_innovation_variance' : 'ev_vpos',
                'fake_hvel_innovation_variance' : 'fake_hvel',
                'fake_vvel_innovation_variance' : 'fake_vvel',
                'fake_hpos_innovation_variance' : 'fake_hpos',
                'fake_vpos_innovation_variance' : 'fake_vpos',
                'rng_vpos_innovation_variance' : 'rng_vpos',
                'baro_vpos_innovation_variance' : 'baro_vpos',
                'aux_hvel_innovation_variance' : 'aux_hvel',
                'aux_vvel_innovation_variance' : 'aux_vvel',
                'mag_field_innovation_variance' : 'mag_field',
                'heading_innovation_variance' : 'heading',
                'airspeed_innovation_variance' : 'airspeed',
                'sideslip_innovation_variance' : 'beta',
                'flow_innovation_variance' : 'flow',
                'hagl_innovation_variance' : 'hagl',
                'drag_innovation_variance' : 'drag'
            }
    }

    field = msg_lookUp_dict[message].get(field_descriptor, None)

    return field


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
