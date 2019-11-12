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
    :return: str
    """
    msg_lookUp_dict = {
        'ekf2_innovations' :
            {
                'magnetometer_innovation' : 'mag_innov',
                'heading_innovation' : 'heading_innov',
                'airspeed_innovation' : 'airspeed_innov',
                'sideslip_innovation' : 'beta_innov',
                'flow_innovation' : 'flow_innov',
                'hagl_innovation' : 'hagl_innov',
                'drag_innovation' : 'drag_innov',
                'magnetometer_innovation_variance' : 'mag_innov_var',
                'heading_innovation_variance' : 'heading_innov_var',
                'airspeed_innovation_variance' : 'airspeed_innov_var',
                'sideslip_innovation_variance' : 'beta_innov_var',
                'flow_innovation_variance' : 'flow_innov_var',
                'hagl_innovation_variance' : 'hagl_innov_var',
                'drag_innovation_variance' : 'drag_innov_var'
            },
        'estimator_innovations' :
            {
                'magnetometer_innovation' : 'mag',
                'heading_innovation' : 'heading',
                'airspeed_innovation' : 'airspeed',
                'sideslip_innovation' : 'beta',
                'flow_innovation' : 'flow',
                'hagl_innovation' : 'hagl',
                'drag_innovation' : 'drag',
            },
        'estimator_innovation_variances' :
            {
                'magnetometer_innovation_variance' : 'mag',
                'heading_innovation_variance' : 'heading',
                'airspeed_innovation_variance' : 'airspeed',
                'sideslip_innovation_variance' : 'beta',
                'flow_innovation_variance' : 'flow',
                'hagl_innovation_variance' : 'hagl',
                'drag_innovation_variance' : 'drag'
            }
    }

    field = msg_lookUp_dict[message].get(field_descriptor, None)

    if field is None:
        raise PreconditionError("Could not find field in lookup table")

    return field
