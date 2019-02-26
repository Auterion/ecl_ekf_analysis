# ecl_ekf_analysis

This repository contains a python package for ekf analysis on PX4 ULog files ([pyulog](https://github.com/PX4/pyulog)). The analysis checks the innovations of the ekf for irregularities and this package provides convenient command line for performing the analysis.

The provided command line scripts are:

```
- process_logdata_ekf: analyse a single PX4 ULog file.
- batch_process_logdata_ekf: run `process_logdata_ekf` on multiple PX4 ULog files in a directory.
- batch_process_metadata_ekf: perform a population analysis on already analysed PX4 ULog files.
```
