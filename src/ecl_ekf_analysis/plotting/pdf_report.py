#! /usr/bin/env python3
"""
function collection for plotting
"""

# matplotlib don't use Xwindows backend (must be before pyplot import)
from typing import Tuple

import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from pyulog import ULog

from ecl_ekf_analysis.analysis.post_processing import magnetic_field_estimates_from_status, \
    get_estimator_check_flags
from ecl_ekf_analysis.log_processing.data_version_handling import get_innovation_message, \
    get_field_name_from_message_and_descriptor, get_innovation_message_and_field_name
from ecl_ekf_analysis.log_processing.custom_exceptions import PreconditionError
from ecl_ekf_analysis.plotting.data_plots import TimeSeriesPlot, InnovationPlot, \
    ControlModeSummaryPlot, CheckFlagsPlot


#pylint: disable=too-many-statements
def create_pdf_report(ulog: ULog, output_plot_filename: str) -> None:
    """
    create a pdf analysis report.
    :param ulog:
    :param output_plot_filename:
    :return:
    """

    # create summary plots
    # save the plots to PDF

    messages = {elem.name for elem in ulog.data_list}
    new_log_format = 'estimator_innovations' in messages

    test_ratio_msg = get_innovation_message(ulog, topic='innovation_test_ratio')
    if test_ratio_msg not in messages:
        raise PreconditionError('could not find {:s} data'.format(test_ratio_msg))
    test_ratio_data = ulog.get_dataset(test_ratio_msg).data

    innovation_message = get_innovation_message(ulog, topic='innovation')
    innovation_data = ulog.get_dataset(innovation_message).data

    innovation_variance_message = get_innovation_message(ulog, topic='innovation_variance')
    innovation_variance_data = ulog.get_dataset(innovation_variance_message).data

    if 'sensor_preflight' not in messages:
        raise PreconditionError('could not find sensor_preflight data')
    sensor_preflight = ulog.get_dataset('sensor_preflight').data

    control_mode, innov_flags, gps_fail_flags = get_estimator_check_flags(estimator_status)

    status_time = 1e-6 * test_ratio_data['timestamp']

    b_finishes_in_air, b_starts_in_air, in_air_duration, in_air_transition_time, \
    on_ground_transition_time = detect_airtime(control_mode, status_time)

    with PdfPages(output_plot_filename) as pdf_pages:

        # plot IMU consistency data
        if ('accel_inconsistency_m_s_s' in sensor_preflight.keys()) and (
                'gyro_inconsistency_rad_s' in sensor_preflight.keys()):
            data_plot = TimeSeriesPlot(
                sensor_preflight, [['accel_inconsistency_m_s_s'], ['gyro_inconsistency_rad_s']],
                x_labels=['data index', 'data index'],
                y_labels=['acceleration (m/s/s)', 'angular rate (rad/s)'],
                plot_title='IMU Consistency Check Levels', pdf_handle=pdf_pages)
            data_plot.save()
            data_plot.close()

        if not new_log_format:
            # vertical velocity and position innovations
            data_plot = InnovationPlot(
                innovation_data, [('vel_pos_innov[2]', 'vel_pos_innov_var[2]'),
                                  ('vel_pos_innov[5]', 'vel_pos_innov_var[5]')],
                x_labels=['time (sec)', 'time (sec)'],
                y_labels=['Down Vel (m/s)', 'Down Pos (m)'], plot_title='Vertical Innovations',
                pdf_handle=pdf_pages)
            data_plot.save()
            data_plot.close()

            # horizontal velocity innovations
            data_plot = InnovationPlot(
                innovation_data, [('vel_pos_innov[0]', 'vel_pos_innov_var[0]'),
                                  ('vel_pos_innov[1]', 'vel_pos_innov_var[1]')],
                x_labels=['time (sec)', 'time (sec)'],
                y_labels=['North Vel (m/s)', 'East Vel (m/s)'],
                plot_title='Horizontal Velocity  Innovations', pdf_handle=pdf_pages)
            data_plot.save()
            data_plot.close()

            # horizontal position innovations
            data_plot = InnovationPlot(
                innovation_data, [('vel_pos_innov[3]', 'vel_pos_innov_var[3]'),
                                  ('vel_pos_innov[4]', 'vel_pos_innov_var[4]')],
                x_labels=['time (sec)', 'time (sec)'],
                y_labels=['North Pos (m)', 'East Pos (m)'],
                plot_title='Horizontal Position Innovations', pdf_handle=pdf_pages)
            data_plot.save()
            data_plot.close()

        mag_innov_field, plot_data = get_plot_data_field_name_from_ulog(ulog, 'mag_field')
        # magnetometer innovations
        data_plot = InnovationPlot(
            plot_data, [('{:s}[0]'.format(mag_innov_field), '{:s}_var[0]'.format(mag_innov_field)),
                        ('{:s}[1]'.format(mag_innov_field), '{:s}_var[1]'.format(mag_innov_field)),
                        ('{:s}[2]'.format(mag_innov_field), '{:s}_var[2]'.format(mag_innov_field))],
            x_labels=['time (sec)', 'time (sec)', 'time (sec)'],
            y_labels=['X (Gauss)', 'Y (Gauss)', 'Z (Gauss)'], plot_title='Magnetometer Innovations',
            pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        heading_field, plot_data = get_plot_data_field_name_from_ulog(ulog, 'heading')
        # magnetic heading innovations
        data_plot = InnovationPlot(
            plot_data, [(heading_field, '{:s}_var'.format(heading_field))],
            x_labels=['time (sec)'], y_labels=['Heading (rad)'],
            plot_title='Magnetic Heading Innovations', pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        airspeed_field, plot_data = get_plot_data_field_name_from_ulog(ulog, 'airspeed')
        beta_field, beta_plot_data = get_plot_data_field_name_from_ulog(ulog, 'beta')
        plot_data.update(beta_plot_data)
        # air data innovations
        data_plot = InnovationPlot(
            plot_data, [(airspeed_field, '{:s}_var'.format(airspeed_field)),
                        (beta_field, '{:s}_var'.format(beta_field))],
            x_labels=['time (sec)', 'time (sec)'],
            y_labels=['innovation (m/sec)', 'innovation (rad)'],
            sub_titles=['True Airspeed Innovations', 'Synthetic Sideslip Innovations'],
            pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        flow_field, plot_data = get_plot_data_field_name_from_ulog(ulog, 'flow')
        # optical flow innovations
        data_plot = InnovationPlot(
            plot_data, [('{:s}[0]'.format(flow_field), '{:s}_var[0]'.format(flow_field)),
                        ('{:s}[1]'.format(flow_field), '{:s}_var[1]'.format(flow_field))],
            x_labels=['time (sec)', 'time (sec)'],
            y_labels=['X (rad/sec)', 'Y (rad/sec)'],
            plot_title='Optical Flow Innovations', pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        test_ratio_message, mag_field = get_innovation_message_and_field_name(
            ulog, 'mag_field', topic='innovation_test_ratio')
        # plot normalised innovation test levels
        # define variables to plot
        field_descriptors = [['mag_field'], ['vel', 'pos'], ['hgt']]
        variables = [
            [get_innovation_message_and_field_name(
                ulog, var, topic='innovation_test_ratio')[1] for var in field_descriptor]
            for field_descriptor in field_descriptors
        ]

        y_labels = ['mag', 'vel, pos', 'hgt']
        legend = [['mag'], ['vel', 'pos'], ['hgt']]
        _, hagl_field_name = get_innovation_message_and_field_name(
            ulog, 'hagl', topic='innovation_test_ratio')
        if np.amax(test_ratio_data[hagl_field_name]) > 0.0:  # plot hagl ratio, if applicable
            variables[-1].append(hagl_field_name)
            y_labels[-1] += ', hagl'
            legend[-1].append('hagl')

        _, airspeed_field_name = get_innovation_message_and_field_name(
            ulog, 'airspeed', topic='innovation_test_ratio')
        if np.amax(test_ratio_data[airspeed_field_name]) > 0.0:  # plot airspeed sensor test ratio
            variables.append([airspeed_field_name])
            y_labels.append('TAS')
            legend.append(['airspeed'])

        data_plot = CheckFlagsPlot(
            status_time, test_ratio_data, variables, x_label='time (sec)', y_labels=y_labels,
            plot_title='Normalised Innovation Test Levels', pdf_handle=pdf_pages, annotate=True,
            legend=legend
        )
        data_plot.save()
        data_plot.close()

        # plot control mode summary A
        data_plot = ControlModeSummaryPlot(
            status_time, control_mode,
            [['tilt_aligned', 'yaw_aligned'], ['using_gps', 'using_optflow', 'using_evpos'],
             ['using_barohgt', 'using_gpshgt', 'using_rnghgt', 'using_evhgt'],
             ['using_magyaw', 'using_mag3d', 'using_magdecl']],
            x_label='time (sec)', y_labels=['aligned', 'pos aiding', 'hgt aiding', 'mag aiding'],
            annotation_text=[
                ['tilt alignment', 'yaw alignment'],
                ['GPS aiding', 'optical flow aiding', 'external vision aiding'],
                ['Baro aiding', 'GPS aiding', 'rangefinder aiding', 'external vision aiding'],
                ['magnetic yaw aiding', '3D magnetoemter aiding', 'magnetic declination aiding']],
            plot_title='EKF Control Status - Figure A', pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        # plot control mode summary B
        # construct additional annotations for the airborne plot
        airborne_annotations = list()
        if np.amin(np.diff(control_mode['airborne'])) > -0.5:
            airborne_annotations.append(
                (on_ground_transition_time, 'air to ground transition not detected'))
        else:
            airborne_annotations.append(
                (on_ground_transition_time, 'on-ground at {:.1f} sec'.format(
                    on_ground_transition_time)))
        if in_air_duration > 0.0:
            airborne_annotations.append(((in_air_transition_time + on_ground_transition_time) / 2,
                                         'duration = {:.1f} sec'.format(in_air_duration)))
        if np.amax(np.diff(control_mode['airborne'])) < 0.5:
            airborne_annotations.append(
                (in_air_transition_time, 'ground to air transition not detected'))
        else:
            airborne_annotations.append(
                (in_air_transition_time, 'in-air at {:.1f} sec'.format(in_air_transition_time)))

        data_plot = ControlModeSummaryPlot(
            status_time, control_mode, [['airborne'], ['estimating_wind']],
            x_label='time (sec)', y_labels=['airborne', 'estimating wind'],
            annotation_text=[[], []], additional_annotation=[airborne_annotations, []],
            plot_title='EKF Control Status - Figure B', pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        # plot innovation_check_flags summary
        data_plot = CheckFlagsPlot(
            status_time, innov_flags, [['vel_innov_fail', 'posh_innov_fail'], ['posv_innov_fail',
                                                                               'hagl_innov_fail'],
                                       ['magx_innov_fail', 'magy_innov_fail', 'magz_innov_fail',
                                        'yaw_innov_fail'], ['tas_innov_fail'], ['sli_innov_fail'],
                                       ['ofx_innov_fail',
                                        'ofy_innov_fail']], x_label='time (sec)',
            y_labels=['failed', 'failed', 'failed', 'failed', 'failed', 'failed'],
            y_lim=(-0.1, 1.1),
            legend=[['vel NED', 'pos NE'], ['hgt absolute', 'hgt above ground'],
                    ['mag_x', 'mag_y', 'mag_z', 'yaw'], ['airspeed'], ['sideslip'],
                    ['flow X', 'flow Y']],
            plot_title='EKF Innovation Test Fails', annotate=False, pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        # gps_check_fail_flags summary
        data_plot = CheckFlagsPlot(
            status_time, gps_fail_flags,
            [['nsat_fail', 'gdop_fail', 'herr_fail', 'verr_fail', 'gfix_fail', 'serr_fail'],
             ['hdrift_fail', 'vdrift_fail', 'hspd_fail', 'veld_diff_fail']],
            x_label='time (sec)', y_lim=(-0.1, 1.1), y_labels=['failed', 'failed'],
            sub_titles=['GPS Direct Output Check Failures', 'GPS Derived Output Check Failures'],
            legend=[
                ['N sats', 'GDOP', 'horiz pos error', 'vert pos error', 'fix type', 'speed error'],
                ['horiz drift', 'vert drift', 'horiz speed', 'vert vel inconsistent']],
            annotate=False, pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        # filter reported accuracy
        data_plot = CheckFlagsPlot(
            status_time, estimator_status, [['pos_horiz_accuracy', 'pos_vert_accuracy']],
            x_label='time (sec)', y_labels=['accuracy (m)'], plot_title='Reported Accuracy',
            legend=[['horizontal', 'vertical']], annotate=False, pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        # Plot the EKF IMU vibration metrics
        scaled_estimator_status = {'vibe[0]': 1000. * estimator_status['vibe[0]'],
                                   'vibe[1]': 1000. * estimator_status['vibe[1]'],
                                   'vibe[2]': estimator_status['vibe[2]']
                                   }
        data_plot = CheckFlagsPlot(
            status_time, scaled_estimator_status, [['vibe[0]'], ['vibe[1]'], ['vibe[2]']],
            x_label='time (sec)', y_labels=['Del Ang Coning (mrad)', 'HF Del Ang (mrad)',
                                            'HF Del Vel (m/s)'], plot_title='IMU Vibration Metrics',
            pdf_handle=pdf_pages, annotate=True)
        data_plot.save()
        data_plot.close()

        # Plot the EKF output observer tracking errors
        scaled_innovations = {
            'output_tracking_error[0]': 1000. * ekf2_innovations['output_tracking_error[0]'],
            'output_tracking_error[1]': ekf2_innovations['output_tracking_error[1]'],
            'output_tracking_error[2]': ekf2_innovations['output_tracking_error[2]']
            }
        data_plot = CheckFlagsPlot(
            1e-6 * ekf2_innovations['timestamp'], scaled_innovations,
            [['output_tracking_error[0]'], ['output_tracking_error[1]'],
             ['output_tracking_error[2]']], x_label='time (sec)',
            y_labels=['angles (mrad)', 'velocity (m/s)', 'position (m)'],
            plot_title='Output Observer Tracking Error Magnitudes',
            pdf_handle=pdf_pages, annotate=True)
        data_plot.save()
        data_plot.close()

        # Plot the delta angle bias estimates
        data_plot = CheckFlagsPlot(
            1e-6 * estimator_status['timestamp'], estimator_status,
            [['states[10]'], ['states[11]'], ['states[12]']],
            x_label='time (sec)', y_labels=['X (rad)', 'Y (rad)', 'Z (rad)'],
            plot_title='Delta Angle Bias Estimates', annotate=False, pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        # Plot the delta velocity bias estimates
        data_plot = CheckFlagsPlot(
            1e-6 * estimator_status['timestamp'], estimator_status,
            [['states[13]'], ['states[14]'], ['states[15]']],
            x_label='time (sec)', y_labels=['X (m/s)', 'Y (m/s)', 'Z (m/s)'],
            plot_title='Delta Velocity Bias Estimates', annotate=False, pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        # Plot the earth frame magnetic field estimates
        declination, field_strength, inclination = magnetic_field_estimates_from_status(
            estimator_status)
        data_plot = CheckFlagsPlot(
            1e-6 * estimator_status['timestamp'],
            {'strength': field_strength, 'declination': declination, 'inclination': inclination},
            [['declination'], ['inclination'], ['strength']],
            x_label='time (sec)', y_labels=['declination (deg)', 'inclination (deg)',
                                            'strength (Gauss)'],
            plot_title='Earth Magnetic Field Estimates', annotate=False,
            pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        # Plot the body frame magnetic field estimates
        data_plot = CheckFlagsPlot(
            1e-6 * estimator_status['timestamp'], estimator_status,
            [['states[19]'], ['states[20]'], ['states[21]']],
            x_label='time (sec)', y_labels=['X (Gauss)', 'Y (Gauss)', 'Z (Gauss)'],
            plot_title='Magnetometer Bias Estimates', annotate=False, pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()

        # Plot the EKF wind estimates
        data_plot = CheckFlagsPlot(
            1e-6 * estimator_status['timestamp'], estimator_status,
            [['states[22]'], ['states[23]']], x_label='time (sec)',
            y_labels=['North (m/s)', 'East (m/s)'], plot_title='Wind Velocity Estimates',
            annotate=False, pdf_handle=pdf_pages)
        data_plot.save()
        data_plot.close()


def get_plot_data_field_name_from_ulog(ulog, field_descriptor: str) -> Tuple[str, dict]:
    """
    :param ulog:
    :param field_descriptor:
    :return:
    """

    messages = {elem.name for elem in ulog.data_list}
    new_log_format = 'estimator_innovations' in messages

    innovation_message, field_name = get_innovation_message_and_field_name(
        ulog, field_descriptor, topic='innovation')
    innovation_variance_message, field_name_var = get_innovation_message_and_field_name(
        ulog, field_descriptor, topic='innovation_variance')

    innovation_data = ulog.get_dataset(innovation_message).data
    innovation_variance_data = ulog.get_dataset(innovation_variance_message).data

    if new_log_format:
        plot_data = {
            innovation_data['{:s}[{:d}]'.format(field_name, axis)] for axis in [0, 1, 2]}
        plot_data.update({
            innovation_variance_data['{:s}_var[{:d}]'.format(
                field_name_var, axis)] for axis in [0, 1, 2]})
    else:
        plot_data = innovation_data

    return field_name, plot_data


def detect_airtime(control_mode, status_time):
    """
    detect airtime. Warning: this function is deprecated and only used for the pdf report.
    :param control_mode:
    :param status_time:
    :return:
    """

    # define flags for starting and finishing in air
    b_starts_in_air = False
    b_finishes_in_air = False
    # calculate in-air transition time
    if np.amax(np.abs(np.diff(control_mode['airborne']))) > 0.5:
        in_air_transtion_time_arg = np.argmax(np.diff(control_mode['airborne']))
        in_air_transition_time = status_time[in_air_transtion_time_arg]
    elif np.amax(control_mode['airborne']) > 0.5:
        in_air_transition_time = np.amin(status_time)
        print('log starts while in-air at ' + str(round(in_air_transition_time, 1)) + ' sec')
        b_starts_in_air = True
    else:
        in_air_transition_time = float('NaN')
        print('always on ground')
    # calculate on-ground transition time
    if np.amin(np.diff(control_mode['airborne'])) < 0.0:
        on_ground_transition_time_arg = np.argmin(np.diff(control_mode['airborne']))
        on_ground_transition_time = status_time[on_ground_transition_time_arg]
    elif np.amax(control_mode['airborne']) > 0.5:
        on_ground_transition_time = np.amax(status_time)
        print('log finishes while in-air at ' + str(round(on_ground_transition_time, 1)) + ' sec')
        b_finishes_in_air = True
    else:
        on_ground_transition_time = float('NaN')
        print('always on ground')
    if np.amax(np.diff(control_mode['airborne'])) > 0.5 and \
            np.amin(np.diff(control_mode['airborne'])) < -0.5:
        if (on_ground_transition_time - in_air_transition_time) > 0.0:
            in_air_duration = on_ground_transition_time - in_air_transition_time
        else:
            in_air_duration = float('NaN')
    else:
        in_air_duration = float('NaN')
    return b_finishes_in_air, b_starts_in_air, in_air_duration, in_air_transition_time, \
           on_ground_transition_time
