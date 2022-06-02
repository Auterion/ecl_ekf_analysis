#! /usr/bin/env python3
"""
Performs a health assessment on the ecl EKF navigation estimator data contained in a an ULog file
Outputs a health assessment summary in a csv file named <inputfilename>.mdat.csv
Outputs summary plots in a pdf file named <inputfilename>.pdf
"""

from __future__ import print_function
from ecl_ekf_analysis.checks.ecl_check_runner import EclCheckRunner
from ecl_ekf_analysis.log_processing.custom_exceptions import PreconditionError
from ecl_ekf_analysis.plotting.pdf_report import create_pdf_report

import argparse
import os
import sys
from typing import List

from pyulog import ULog
import simplejson as json

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


def get_arguments():
    """
    parses the command line arguments
    :return:
    """
    parser = argparse.ArgumentParser(
        description='Analyse the estimator_status and ekf2_innovation message data for a single'
                    'ulog file.')
    parser.add_argument('filename', metavar='file.ulg', help='ULog input file')
    parser.add_argument(
        '--plots',
        action='store_true',
        help='Whether to plot an innovation summary for developers (only available '
        'for old estimator innovation messages).')
    return parser.parse_args()


def analyse_logdata_ekf(ulog: ULog) -> List[dict]:
    """
    perform the analysis
    :param ulog:
    :return:
    """

    ecl_check_runner = EclCheckRunner(ulog)
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
        if test_result['status'] == 'WARNING' and master_status == 'Pass':
            master_status = 'Warning'
        elif test_result['status'] == 'FAIL':
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
    except Exception as e:
        raise PreconditionError(f'could not open {filename:s}') from e

    test_results = analyse_logdata_ekf(ulog)

    with open(f'{os.path.splitext(filename)[0]:s}.json', 'w') as file:
        json.dump(test_results, file, indent=2)

    if plot:
        create_pdf_report(ulog, f'{filename:s}.pdf')
        print(f'Plots saved to {filename:s}.pdf')

    return test_results


def main() -> None:
    """
    main entry point
    :return:
    """

    args = get_arguments()

    try:
        test_results = process_logdata_ekf(args.filename, plot=args.plots)
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
