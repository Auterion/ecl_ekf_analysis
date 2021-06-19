#! /usr/bin/env python3
"""
function collection for handling different versions of log files
"""
from typing import List, Tuple

from pyulog import ULog

from ecl_ekf_analysis.log_processing.custom_exceptions import PreconditionError


def get_output_tracking_error_message(ulog: ULog) -> str:
    """
    return the name of the message containing the output_tracking_error
    :param ulog:
    :return: str
    """
    output_tracking_error_message = ""
    ulog_messages = {elem.name for elem in ulog.data_list}

    if "estimator_innovations" in ulog_messages:
        output_tracking_error_message = "estimator_status"
    elif "ekf2_innovations" in ulog_messages:
        output_tracking_error_message = "ekf2_innovations"
    else:
        raise PreconditionError("Output tracking error message not found in log.")

    return output_tracking_error_message


def get_innovation_message(ulog: ULog, topic: str = "innovation") -> str:
    """
    return the name of the innovation message (old: ekf2_innovations; new: estimator_innovations)
    :param ulog:
    :return: str
    """
    ulog_messages = {elem.name for elem in ulog.data_list}
    message = ""

    if topic == "innovation":
        if "estimator_innovations" in ulog_messages:
            message = "estimator_innovations"
        elif "ekf2_innovations" in ulog_messages:
            message = "ekf2_innovations"
        else:
            raise PreconditionError("innovation message not found.")
    elif topic == "innovation_variance":
        if "estimator_innovation_variances" in ulog_messages:
            message = "estimator_innovation_variances"
        elif "ekf2_innovations" in ulog_messages:
            message = "ekf2_innovations"
        else:
            raise PreconditionError("innovation variances message not found.")
    elif topic == "innovation_test_ratio":
        if "estimator_innovation_test_ratios" in ulog_messages:
            message = "estimator_innovation_test_ratios"
        elif "estimator_status" in ulog_messages:
            message = "estimator_status"
        else:
            raise PreconditionError("estimator innovation test ratios message not found.")
    else:
        raise NotImplementedError("topic {:s} not supported".format(topic))

    return message


def get_field_name_from_message_and_descriptor(
    message: str, field_descriptor: str, topic: str = "innovation"
) -> str:
    """
    return the actual field name for a field descriptor
    e.g. message: ekf2_innovations; field_descriptor: magnetometer_innovations -> mag_innov
    :param ulog:
    :return: str (if field not found, None will be returned)
    """
    field_name = ""
    if message in [
        "estimator_innovations",
        "estimator_innovation_variances",
        "estimator_innovation_test_ratios",
    ]:
        field_name = field_descriptor
    elif message in ["ekf2_innovations", "estimator_status"]:
        if topic == "innovation":
            msg_lookUp_dict = {
                "aux_hvel": "aux_vel_innov",
                "mag_field": "mag_innov",
                "heading": "heading_innov",
                "airspeed": "airspeed_innov",
                "beta": "beta_innov",
                "flow": "flow_innov",
                "hagl": "hagl_innov",
                "drag": "drag_innov",
            }
            field_name = msg_lookUp_dict[field_descriptor]
        elif topic == "innovation_variance":
            msg_lookUp_dict = {
                "aux_hvel": "aux_vel_innov_var",
                "mag_field": "mag_innov_var",
                "heading": "heading_innov_var",
                "airspeed": "airspeed_innov_var",
                "beta": "beta_innov_var",
                "flow": "flow_innov_var",
                "hagl": "hagl_innov_var",
                "drag": "drag_innov_var",
            }
            field_name = msg_lookUp_dict[field_descriptor]
        elif topic == "innovation_test_ratio":
            msg_lookUp_dict = {
                "pos": "pos_test_ratio",
                "vel": "vel_test_ratio",
                "hgt": "hgt_test_ratio",
                "mag_field": "mag_test_ratio",
                "airspeed": "tas_test_ratio",
                "beta": "beta_test_ratio",
                "hagl": "hagl_test_ratio",
            }
            field_name = msg_lookUp_dict[field_descriptor]
        else:
            raise NotImplementedError("topic {:s} not supported".format(topic))
    else:
        raise NotImplementedError("message {:s} not supported".format(message))

    return field_name


def get_innovation_message_and_field_names(
    ulog: ULog, field_descriptor: str, topic: str = "innovation"
) -> Tuple[str, List[str]]:
    """
    :param ulog:
    :param field_descriptor:
    :param topic: one of (innovation | innovation_variance | innovation_test_ratio)
    :return:
    """
    field_names = []
    message = get_innovation_message(ulog, topic=topic)

    field_name = get_field_name_from_message_and_descriptor(message, field_descriptor, topic=topic)

    innov_data = ulog.get_dataset(message).data

    if field_name in innov_data:
        field_names.append(field_name)
    else:
        i = 0
        while "{:s}[{:d}]".format(field_name, i) in innov_data:
            field_names.append("{:s}[{:d}]".format(field_name, i))
            i += 1

        if field_name.endswith("_vel"):
            field_names.append("{:s}_h{:s}[0]".format(field_name[:3], field_name[-3:]))
            field_names.append("{:s}_h{:s}[1]".format(field_name[:3], field_name[-3:]))
            field_names.append("{:s}_v{:s}".format(field_name[:3], field_name[-3:]))

    return message, field_names


def get_field_names_for_innovation_messages(ulog: ULog, field_descriptors: List[str]) -> List[str]:
    """
    :param ulog:
    :param field_descriptors:
    :return:
    """
    return [
        get_field_name_from_message_and_descriptor(get_innovation_message(ulog), field_descriptor)
        for field_descriptor in field_descriptors
    ]


def check_if_field_name_exists_in_message(ulog: ULog, message: str, field_name: str) -> bool:
    """
    Check if a field is part of a message in a certain log
    """
    exists = True

    if message not in [elem.name for elem in ulog.data_list]:
        exists = False
    elif field_name not in ulog.get_dataset(message).data.keys():
        exists = False

    return exists


def check_if_field_name_exists_in_message_escape_axis(
    ulog: ULog, message: str, field_name: str
) -> bool:
    """
    Check if a field is part of a message in a certain log
    """
    exists = True

    if message not in [elem.name for elem in ulog.data_list]:
        exists = False
    elif field_name not in [
        str(key).split("[")[0] for key in ulog.get_dataset(message).data.keys()
    ]:
        exists = False

    return exists
