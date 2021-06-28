#! /usr/bin/env python3
"""
returns thresholds
"""
#pylint

import os
import configparser

_thresholds = configparser.ConfigParser()
_thresholds.read([os.path.join(os.path.dirname(__file__), 'thresholds.ini')])

def ecl_innovation_failure_pct_exists(innovation_name: str) -> bool:
    return _thresholds.has_option('DEFAULT', '{:s}_innovation_failure_pct'.format(innovation_name))

def ecl_innovation_failure_pct(innovation_name: str) -> float:
    return _thresholds.getfloat('DEFAULT', '{:s}_innovation_failure_pct'.format(innovation_name))

def ecl_short_rolling_innovation_failure_pct_exists(innovation_name: str) -> bool:
    return _thresholds.has_option(
        'DEFAULT',
        '{:s}_short_rolling_innovation_failure_pct'.format(innovation_name)
    )

def ecl_short_rolling_innovation_failure_pct(innovation_name: str) -> float:
    return _thresholds.getfloat(
        'DEFAULT',
        '{:s}_short_rolling_innovation_failure_pct'.format(innovation_name)
    )

def ecl_long_rolling_innovation_warning_pct_exists(innovation_name: str) -> bool:
    return _thresholds.has_option(
        'DEFAULT', '{:s}_long_rolling_innovation_warning_pct'.format(innovation_name)
    )

def ecl_long_rolling_innovation_warning_pct(innovation_name: str) -> float:
    return _thresholds.getfloat(
        'DEFAULT',
        '{:s}_long_rolling_innovation_warning_pct'.format(innovation_name)
    )

def ecl_amber_warning_pct(innovation_name: str) -> float:
    return _thresholds.getfloat('DEFAULT', '{:s}_amber_warning_pct'.format(innovation_name))

def ecl_amber_warning_pct_exists(innovation_name: str) -> bool:
    return _thresholds.has_option('DEFAULT', '{:s}_amber_warning_pct'.format(innovation_name))

def ecl_amber_failure_pct(innovation_name: str) -> float:
    return _thresholds.getfloat('DEFAULT', '{:s}_amber_failure_pct'.format(innovation_name))

def ecl_amber_failure_pct_exists(innovation_name: str) -> bool:
    return _thresholds.has_option('DEFAULT', '{:s}_amber_failure_pct'.format(innovation_name))

def ecl_amber_warning_windowed_pct(innovation_name: str) -> float:
    return _thresholds.getfloat(
        'DEFAULT',
        '{:s}_amber_warning_windowed_pct'.format(innovation_name)
    )

def ecl_amber_warning_windowed_pct_exists(innovation_name: str) -> bool:
    return _thresholds.has_option(
        'DEFAULT',
        '{:s}_amber_warning_windowed_pct'.format(innovation_name)
    )

def ecl_amber_failure_windowed_pct(innovation_name: str) -> float:
    return _thresholds.getfloat(
        'DEFAULT',
        '{:s}_amber_failure_windowed_pct'.format(innovation_name)
    )

def ecl_amber_failure_windowed_pct_exists(innovation_name: str) -> bool:
    return _thresholds.has_option(
        'DEFAULT',
        '{:s}_amber_failure_windowed_pct'.format(innovation_name)
    )

def ecl_filter_fault_flag_failure() -> float:
    return _thresholds.getfloat('DEFAULT', 'filter_fault_flag_failure')

def imu_coning_warning_max() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_coning_warning_max')

def imu_coning_warning_rolling_avg() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_coning_warning_rolling_avg')

def imu_high_freq_delta_angle_warning_max() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_high_freq_delta_angle_warning_max')

def imu_high_freq_delta_angle_warning_rolling_avg() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_high_freq_delta_angle_warning_rolling_avg')

def imu_high_freq_delta_velocity_warning_max() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_high_freq_delta_velocity_warning_max')

def imu_high_freq_delta_velocity_warning_rolling_avg() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_high_freq_delta_velocity_warning_rolling_avg')

def imu_observed_angle_error_warning_avg() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_observed_angle_error_warning_avg')

def imu_observed_velocity_error_warning_avg() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_observed_velocity_error_warning_avg')

def imu_observed_position_error_warning_avg() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_observed_position_error_warning_avg')

def imu_delta_angle_bias_warning_avg() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_delta_angle_bias_warning_avg')

def imu_delta_velocity_bias_warning_avg() -> float:
    return _thresholds.getfloat('DEFAULT', 'imu_delta_velocity_bias_warning_avg')