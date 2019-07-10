#! /usr/bin/env python3
"""
Performs a health assessment on the ecl EKF navigation estimator data contained in a an ULog file
Outputs a health assessment summary in a csv file named <inputfilename>.mdat.csv
Outputs summary plots in a pdf file named <inputfilename>.pdf
"""

from __future__ import print_function

import argparse
import sys
from typing import Dict, Tuple, Optional

from pyulog import ULog

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


def analyse_logdata_ekf(ulog: ULog) -> Dict[str, tuple]:
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
    ecl_check_runner = EclCheckRunner(ulog, innov_flags)
    ecl_check_runner.run_checks()
    test_results = ecl_check_runner.results_table

    return test_results


def get_master_status_from_test_results(
            test_results: Dict[str, tuple]) -> Tuple[str, str, Optional[str]]:
    """
    :param test_results:
    :return:
    """
    master_status = 'Pass'
    for _, entry in test_results.items():
        if entry[0] == 'Warning' and master_status == 'Pass':
            master_status = 'Warning'
        elif entry[0] == 'Fail':
            master_status = 'Fail'
            break
    return (master_status, '', None)


def write_test_results_to_csv(filename: str, test_results: Dict[str, tuple]) -> None:
    """
    :param filename:
    :param test_results:
    :return:
    """
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


def process_logdata_ekf(filename: str, plot: bool = False) -> Dict[str, tuple]:
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

    test_results['master_status'] = get_master_status_from_test_results(test_results)

    write_test_results_to_csv(filename, test_results)

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
