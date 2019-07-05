#! /usr/bin/env python3
"""
Performs a health assessment on the ecl EKF navigation estimator data contained in a an ULog file
Outputs a health assessment summary in a csv file named <inputfilename>.mdat.csv
Outputs summary plots in a pdf file named <inputfilename>.pdf
"""

from __future__ import print_function

import argparse
import os
import sys
import csv
from typing import Dict, Optional

from pyulog import ULog

from analyse_logdata_ekf import analyse_ekf
from plotting.pdf_report import create_pdf_report
from analysis.custom_exceptions import PreconditionError


def get_arguments():
    """
    parses the command line arguments
    :return:
    """
    parser = argparse.ArgumentParser(
        description='Analyse the estimator_status and ekf2_innovation message data for a single'
                    'ulog file.')
    parser.add_argument('filename', metavar='file.ulg', help='ULog input file')
    parser.add_argument('--no-plots', action='store_true',
                        help='Whether to only analyse and not plot the summaries for developers.')
    parser.add_argument('--check-level-thresholds', type=str, default=None,
                        help='The csv file of fail and warning test thresholds for analysis.')
    parser.add_argument('--check-table', type=str, default=None,
                        help='The csv file with descriptions of the checks.')
    parser.add_argument(
        '--no-sensor-safety-margin', action='store_true',
        help='Whether to not cut-off 5s after take-off and 5s before landing '
             '(for certain sensors that might be influence by proximity to ground).')
    return parser.parse_args()


def create_results_table(
        check_table_filename: str, master_status: str, check_status: Dict[str, str],
        metrics: Dict[str, float], airtime_info: Dict[str, float]) -> Dict[str, list]:
    """
    creates the output results table
    :param check_table_filename:
    :param master_status:
    :param check_status:
    :param metrics:
    :param airtime_info:
    :return:
    """

    try:
        with open(check_table_filename, 'r') as file:
            reader = csv.DictReader(file)
            test_results_table = {
                row['check_id']: [float('NaN'), row['check_description']] for row in reader}
        print('Using test description loaded from {:s}'.format(check_table_filename))
    except:
        raise PreconditionError('could not find {:s}'.format(check_table_filename))

    # store metrics
    for key, value in metrics.items():
        test_results_table[key][0] = value

    # store check results
    for key, value in check_status.items():
        test_results_table[key][0] = value

    # store check results
    for key, value in test_results_table.items():
        if key.endswith('_status'):
            test_results_table[key][0] = str(value[0])

    # store master status
    test_results_table['master_status'][0] = master_status

    # store take_off and landing information
    test_results_table['in_air_transition_time'][0] = airtime_info['in_air_transition_time']
    test_results_table['on_ground_transition_time'][0] = airtime_info['on_ground_transition_time']

    return test_results_table


def process_logdata_ekf(
        filename: str, check_level_dict_filename: str, check_table_filename: str,
        plot: bool = True, sensor_safety_margins: bool = True):
    """
    main function for processing the logdata for ekf analysis.
    :param filename:
    :param check_level_dict_filename:
    :param check_table_filename:
    :param plot:
    :param sensor_safety_margins:
    :return:
    """

    ## load the log and extract the necessary data for the analyses
    try:
        ulog = ULog(filename)
    except:
        raise PreconditionError('could not open {:s}'.format(filename))

    try:
        # get the dictionary of fail and warning test thresholds from a csv file
        with open(check_level_dict_filename, 'r') as file:
            reader = csv.DictReader(file)
            check_levels = {row['check_id']: float(row['threshold']) for row in reader}
        print('Using test criteria loaded from {:s}'.format(check_level_dict_filename))
    except:
        raise PreconditionError('could not find {:s}'.format(check_level_dict_filename))

    in_air_margin = 5.0 if sensor_safety_margins else 0.0
    # perform the ekf analysis
    master_status, check_status, metrics, airtime_info = analyse_ekf(
        ulog, check_levels, red_thresh=1.0, amb_thresh=0.5, min_flight_duration_seconds=5.0,
        in_air_margin_seconds=in_air_margin)

    test_results = create_results_table(
        check_table_filename, master_status, check_status, metrics, airtime_info)

    # write metadata to a .csv file
    with open('{:s}.mdat.csv'.format(filename), "w") as file:

        file.write("name,value,description\n")

        # loop through the test results dictionary and write each entry on a separate row,
        # with data comma separated save data in alphabetical order
        key_list = list(test_results.keys())
        key_list.sort()
        for key in key_list:
            file.write(key + "," + str(test_results[key][0]) + "," + test_results[key][1] + "\n")
    print('Test results written to {:s}.mdat.csv'.format(filename))

    if plot:
        create_pdf_report(ulog, '{:s}.pdf'.format(filename))
        print('Plots saved to {:s}.pdf'.format(filename))

    return test_results


def process_logdata_ekf_configured(
        log_filename: str, check_level_thresholds: Optional[str] = None,
        check_table: Optional[str] = None, plot: bool = True,
        sensor_safety_margins: bool = True):
    """
    process the logdate without specifying the csv parameter files.
    :param log_filename:
    :param check_level_thresholds:
    :param check_table:
    :param plot:
    :param sensor_safety_margins:
    :return:
    """

    if check_level_thresholds is not None:
        check_level_dict_filename = check_level_thresholds
    else:
        file_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        check_level_dict_filename = os.path.join(file_dir, "check_level_dict.csv")

    if check_table is not None:
        check_table_filename = check_table
    else:
        file_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        check_table_filename = os.path.join(file_dir, "check_table.csv")

    test_results = process_logdata_ekf(
        log_filename, check_level_dict_filename, check_table_filename,
        plot=plot, sensor_safety_margins=sensor_safety_margins)

    return test_results


def main() -> None:
    """
    main entry point
    :return:
    """

    args = get_arguments()

    try:
        test_results = process_logdata_ekf_configured(
            args.filename, check_level_thresholds=args.check_level_thresholds,
            check_table=args.check_table, plot=not args.no_plots,
            sensor_safety_margins=not args.no_sensor_safety_margin)
    except Exception as e:
        print(str(e))
        sys.exit(-1)

    # print master test status to console
    if test_results['master_status'][0] == 'Pass':
        print('No anomalies detected')
    elif test_results['master_status'][0] == 'Warning':
        print('Minor anomalies detected')
    elif test_results['master_status'][0] == 'Fail':
        print('Major anomalies detected')
        sys.exit(-1)


if __name__ == '__main__':
    main()
