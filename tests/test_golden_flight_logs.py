#! /usr/bin/env python3
"""
Running the analysis over a couple of golden flight logs.
"""

import os
import csv
from tempfile import TemporaryDirectory

import simplejson as json
import pytest

from process_logdata_ekf import process_logdata_ekf

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
        log_file_path, '{:s}_golden.json'.format(os.path.splitext(log_filename)[0]))

    with TemporaryDirectory() as tmp_dir:

        tmp_log_filename = os.path.join(tmp_dir, os.path.basename(log_filename))

        os.system('cp {:s} {:s}'.format(log_filename, tmp_log_filename))

        assert os.path.exists(tmp_log_filename), '{:s} does not exist.'.format(tmp_log_filename)

        process_logdata_ekf(tmp_log_filename, plot=False)

        analysis_result_filename = os.path.join(tmp_dir, '{:s}.json'.format(tmp_log_filename))

        assert os.path.exists(analysis_result_filename), '{:s} does not exist.'.format(
            analysis_result_filename)

        with open(analysis_result_filename, 'r') as file:
            analysis_results = json.load(file)

        with open(golden_result_filename, 'r') as file:
            golden_results = json.load(file)

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
