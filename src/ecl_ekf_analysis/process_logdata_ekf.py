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
from typing import List

from pyulog import ULog
import simplejson as json

from plotting.pdf_report import create_pdf_report
from log_processing.custom_exceptions import PreconditionError
from analysis.post_processing import get_estimator_check_flags
from checks.ecl_check_runner import EclCheckRunner


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
    return parser.parse_args()


def analyse_logdata_ekf(ulog: ULog) -> List[dict]:
    """
    perform the analysis
    :param ulog:
    :return:
    """
    try:
        estimator_status_data = ulog.get_dataset('estimator_status').data
        print('found estimator_status data')
    except:
        raise PreconditionError('could not find estimator_status data')
    control_mode, innov_flags, gps_fail_flags = get_estimator_check_flags(estimator_status_data)
    ecl_check_runner = EclCheckRunner(ulog, innov_flags, control_mode)
    ecl_check_runner.run_checks()
    test_results = ecl_check_runner.results_deserialized

    return test_results


def get_master_status_from_test_results(test_results: List[dict]) -> str:
    """
    :param test_results:
    :return:
    """
    master_status = 'Pass'
    for test_result in test_results:
        if test_result['status'] == 'CHECK_STATUS_WARNING' and master_status == 'Pass':
            master_status = 'Warning'
        elif test_result['status'] == 'CHECK_STATUS_FAIL':
            master_status = 'Fail'
            break
    return master_status


def process_logdata_ekf(filename: str, plot: bool = False) -> List[dict]:
    """
    main function for processing the logdata for ekf analysis.
    :param filename:
    :param plot:
    :return:
    """
    try:
        ulog = ULog(filename)
    except:
        raise PreconditionError('could not open {:s}'.format(filename))

    test_results = analyse_logdata_ekf(ulog)

    with open('{:s}.json'.format(os.path.splitext(filename)[0]), 'w') as file:
        json.dump(test_results, file, indent=2)

    if plot:
        create_pdf_report(ulog, '{:s}.pdf'.format(filename))
        print('Plots saved to {:s}.pdf'.format(filename))

    return test_results


def main() -> None:
    """
    main entry point
    :return:
    """

    args = get_arguments()

    try:
        test_results = process_logdata_ekf(args.filename, plot=not args.no_plots)
    except Exception as e:
        print(str(e))
        sys.exit(-1)

    master_status = get_master_status_from_test_results(test_results)

    # print master test status to console
    if master_status == 'Pass':
        print('No anomalies detected')
    elif master_status == 'Warning':
        print('Minor anomalies detected')
    elif master_status == 'Fail':
        print('Major anomalies detected')
        sys.exit(-1)


if __name__ == '__main__':
    main()
