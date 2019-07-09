# /usr/bin/env/ python3
"""
an estimator check runner class
"""
from typing import Dict
from pyulog import ULog

from checks.base_runner import CheckRunner
from checks.estimator_analysis import MagnetometerCheck, MagneticHeadingCheck, VelocityCheck, \
    PositionCheck, HeightCheck, HeightAboveGroundCheck, AirspeedCheck, SideSlipCheck, \
    OpticalFlowCheck
from checks.imu_analysis import IMU_Vibration_Check, IMU_Bias_Check, IMU_Output_Predictor_Check


class EclCheckRunner(CheckRunner):
    """
    a runner for performing the load analyses.

    """
    def __init__(self, ulog: ULog, innov_flags: Dict[str, float]):
        """
        :param ulog:
        :param check_levels_dict:
        """
        super(EclCheckRunner, self).__init__()
        self.append(MagnetometerCheck(ulog, innov_flags))
        self.append(MagneticHeadingCheck(ulog, innov_flags))
        self.append(VelocityCheck(ulog, innov_flags))
        self.append(PositionCheck(ulog, innov_flags))
        self.append(HeightCheck(ulog, innov_flags))
        self.append(HeightAboveGroundCheck(ulog, innov_flags))
        self.append(AirspeedCheck(ulog, innov_flags))
        self.append(SideSlipCheck(ulog, innov_flags))
        self.append(OpticalFlowCheck(ulog, innov_flags))
        self.append(IMU_Vibration_Check(ulog))
        self.append(IMU_Bias_Check(ulog))
        self.append(IMU_Output_Predictor_Check(ulog))
