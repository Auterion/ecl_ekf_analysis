#! /usr/bin/env python3
"""
Running the analysis over a couple of golden flight logs.
"""

import os
import csv
from tempfile import TemporaryDirectory

import pytest

from ecl_ekf_analysis.process_logdata_ekf import process_logdata_ekf_configured

@pytest.fixture(scope="module")
def testing_args():
    """
    arguments for testing.
    :return: test arguments
    """
    return {'golden_flight_logs_path': os.path.join(os.path.dirname(__file__), 'flight_logs'),
            'golden_flight_logs': ['short_f450_log.ulg']}


def compare_analysis_to_golden(log_filename: str, log_file_path: str) -> None:
    """
    runs an analysis and compares the result file to the golden result (uses approximate value
    for floating points)
    :param log_filename:
    :param log_file_path:
    :return:
    """

    golden_result_filename = os.path.join(
        log_file_path, '{:s}_golden.mdat.csv'.format(os.path.splitext(log_filename)[0]))

    with TemporaryDirectory() as tmp_dir:

        tmp_log_filename = os.path.join(tmp_dir, os.path.basename(log_filename))

        os.system('cp {:s} {:s}'.format(log_filename, tmp_log_filename))

        assert os.path.exists(tmp_log_filename)

        process_logdata_ekf_configured(tmp_log_filename, plot=False)

        analysis_result_filename = os.path.join(tmp_dir, '{:s}.mdat.csv'.format(tmp_log_filename))

        assert os.path.exists(analysis_result_filename)

        with open(analysis_result_filename, 'r') as file:
            reader = csv.DictReader(file)
            analysis_results = {row['name']: row['value'] for row in reader}


        with open(golden_result_filename, 'r') as file:
            reader = csv.DictReader(file)
            golden_results = {row['name']: row['value'] for row in reader}

        print('comparing analysis to golden results')
        print('result_name; value; golden_value')
        for result_name, golden_value in golden_results.items():
            print('{:s}; {:s}; {:s}'.format(
                result_name, str(analysis_results[result_name]), str(golden_value)))
            if isinstance(golden_value, float):
                assert golden_value == pytest.approx(analysis_results[result_name])
            else:
                assert golden_value == analysis_results[result_name]

def test_golden_flight_logs(testing_args):
    """
    tests the basics of the in air detector on a dummy log file.
    :param testing_args:
    :return:
    """

    for golden_flight_log in testing_args['golden_flight_logs']:
        log_filename = os.path.join(
            testing_args['golden_flight_logs_path'], golden_flight_log)

        compare_analysis_to_golden(log_filename, testing_args['golden_flight_logs_path'])
