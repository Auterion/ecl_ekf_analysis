#! /usr/bin/env python3
"""
Runs process_logdata_ekf.py on the .ulg files in the supplied directory. ulog files are
skipped from the analysis, if a
 corresponding .pdf file already exists (unless the overwrite flag was set).
"""
# -*- coding: utf-8 -*-

from ecl_ekf_analysis.process_logdata_ekf import process_logdata_ekf
import argparse
import sys
import os
import glob

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


def get_arguments():
    """
    parses the command line arguments.
    :return:
    """
    parser = argparse.ArgumentParser(
        description='Analyse the estimator_status and ekf2_innovation message data for the '
                    '.ulg files in the specified directory')
    parser.add_argument("directory_path")
    parser.add_argument(
        '-o', '--overwrite', action='store_true',
        help='Whether to overwrite an already analysed file. If a file with .pdf extension exists '
             'for a .ulg file, the log file will be skipped from analysis unless this flag has '
             'been set.')
    parser.add_argument(
        '--plots',
        action='store_true',
        help='Whether to plot an innovation summary for developers (only available '
        'for old estimator innovation messages).')
    return parser.parse_args()


def main() -> None:
    """
    the main entry point
    :return:
    """

    args = get_arguments()

    ulog_directory = args.directory_path

    # get all the ulog files found in the specified directory and in
    # subdirectories
    ulog_files = glob.glob(
        os.path.join(
            ulog_directory,
            '**/*.ulg'),
        recursive=True)
    print(f"found {len(ulog_files):d} .ulg files in {ulog_directory:s}")

    # remove the files already analysed unless the overwrite flag was specified. A
    # ulog file is consired to be analysed if # a corresponding .pdf file
    # exists.'
    if not args.overwrite:
        print("skipping already analysed ulg files.")
        ulog_files = [ulog_file for ulog_file in ulog_files if not os.path.exists(
            f'{os.path.splitext(ulog_file)[0]:s}.json')]

    n_files = len(ulog_files)

    print(f"analysing the {n_files:d} .ulg files")

    i = 1
    n_skipped = 0
    # analyse all ulog files
    for ulog_file in ulog_files:
        print(f'analysing file {i:d}/{n_files:d}: {ulog_file:s}')

        try:
            _ = process_logdata_ekf(ulog_file, plot=args.plots)

        except Exception as e:
            print(str(e))
            print(f'an exception occurred, skipping file {ulog_file:s}')
            n_skipped = n_skipped + 1

        i = i + 1

    print(f'{n_files - n_skipped:d}/{n_files:d} files analysed, {n_skipped:d} skipped.')


if __name__ == '__main__':
    main()
