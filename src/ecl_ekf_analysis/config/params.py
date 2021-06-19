#! /usr/bin/env python3
"""
returns environment parameters
"""
import configparser
import os

_params = configparser.ConfigParser()
_params.read([os.path.join(os.path.dirname(__file__), "params.ini")])


def iad_min_flight_duration_seconds() -> float:
    return _params.getfloat("in-air-detector", "min_flight_duration_seconds")


def iad_in_air_margin_seconds() -> float:
    return _params.getfloat("in-air-detector", "in_air_margin_seconds")


def warn_altitude() -> float:
    return _params.getfloat("log-processing", "warn_altitude")


def warn_duration_s() -> int:
    return _params.getint("log-processing", "warn_duration_s")


def gps_ts_rejection_h() -> int:
    return _params.getint("log-processing", "gps_timestamp_rejection_hours")


def ecl_red_thresh() -> float:
    return _params.getfloat("ecl-analysis", "red_thresh")


def ecl_amb_thresh() -> float:
    return _params.getfloat("ecl-analysis", "amb_thresh")


def ecl_pos_checks_when_sensors_not_fused() -> bool:
    return _params.getboolean("ecl-analysis", "ecl_pos_checks_when_sensors_not_fused")


def ecl_window_len_s() -> float:
    return _params.getfloat("ecl-analysis", "window_len_s")


def of_min_ground_distance_meters() -> float:
    return _params.getfloat("optical-flow", "min_ground_distance_meters")


def of_min_flight_phase_duration_seconds() -> float:
    return _params.getfloat("optical-flow", "min_flight_phase_duration_seconds")
