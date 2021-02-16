# /usr/bin/env/ python3
"""
an estimator check runner class
"""
from pyulog import ULog

from ecl_ekf_analysis.checks.base_runner import CheckRunner, AnalysisStatus
from ecl_ekf_analysis.checks.estimator_analysis import MagnetometerCheck, MagneticHeadingCheck, \
    VelocityCheck, PositionCheck, HeightCheck, HeightAboveGroundCheck, AirspeedCheck, \
    SideSlipCheck, OpticalFlowCheck, GPSVelocityCheck, GPSPositionCheck, EVVelocityCheck, \
    EVPositionCheck, GPSHeightCheck, EVHeightCheck, BarometerHeightCheck, RangeSensorHeightCheck
from ecl_ekf_analysis.checks.imu_analysis import IMU_Vibration_Check, IMU_Bias_Check, \
    IMU_Output_Predictor_Check
from ecl_ekf_analysis.checks.numerical_analysis import NumericalCheck
from ecl_ekf_analysis.log_processing.custom_exceptions import capture_message
from ecl_ekf_analysis.analysis.post_processing import get_estimator_check_flags


class EclCheckRunner(CheckRunner):
    """
    a runner for performing the load analyses.

    """
    def __init__(self, ulog: ULog):
        """
        :param ulog:
        """
        super().__init__()

        try:
            estimator_status_data = ulog.get_dataset('estimator_status').data
            print('found estimator_status data')

            control_mode_flags, innov_flags, _ = get_estimator_check_flags(estimator_status_data)

            self.append(MagnetometerCheck(ulog, innov_flags, control_mode_flags))
            self.append(MagneticHeadingCheck(ulog, innov_flags, control_mode_flags))
            self.append(VelocityCheck(ulog, innov_flags, control_mode_flags))
            self.append(PositionCheck(ulog, innov_flags, control_mode_flags))
            self.append(HeightCheck(ulog, innov_flags, control_mode_flags))
            self.append(HeightAboveGroundCheck(ulog, innov_flags, control_mode_flags))
            self.append(AirspeedCheck(ulog, innov_flags, control_mode_flags))
            self.append(SideSlipCheck(ulog, innov_flags, control_mode_flags))
            self.append(OpticalFlowCheck(ulog, innov_flags, control_mode_flags))
            self.append(IMU_Vibration_Check(ulog))
            self.append(IMU_Bias_Check(ulog))
            self.append(IMU_Output_Predictor_Check(ulog))
            self.append(NumericalCheck(ulog))
            self.append(GPSVelocityCheck(ulog, innov_flags, control_mode_flags))
            self.append(EVVelocityCheck(ulog, innov_flags, control_mode_flags))
            self.append(GPSPositionCheck(ulog, innov_flags, control_mode_flags))
            self.append(EVPositionCheck(ulog, innov_flags, control_mode_flags))
            self.append(GPSHeightCheck(ulog, innov_flags, control_mode_flags))
            self.append(EVHeightCheck(ulog, innov_flags, control_mode_flags))
            self.append(BarometerHeightCheck(ulog, innov_flags, control_mode_flags))
            self.append(RangeSensorHeightCheck(ulog, innov_flags, control_mode_flags))
        except Exception as e:
            capture_message(str(e))
            self.error_message = str(e)
            self.analysis_status = AnalysisStatus.PRECONDITION_ERROR
