# ecl_ekf_analysis

This repository contains a python package for ekf related analysis on PX4 ULog files ([pyulog](https://github.com/PX4/pyulog)). The command line scripts of this package analyse the ekf innovations and the internal ekf test metrics for irregularities.

The provided command line scripts are:

- `process_logdata_ekf`: analyse a single PX4 ULog file.
- `batch_process_logdata_ekf`: run `process_logdata_ekf` on multiple PX4 ULog files in a directory.

## Installation

Installation with package manager via ssh:
```bash
pip install git+ssh://git@github.com/Auterion/ecl_ekf_analysis.git#egg=ecl_ekf_analysis
```
or using https:
```bash
pip install git+https://github.com/Auterion/ecl_ekf_analysis.git#egg=ecl_ekf_analysis
```

Check the official pip [documentation](https://pip.pypa.io/en/stable/reference/pip_install/) for installing particular branches or commits using git hashes.

Installation from source:
```bash
python setup.py build install
```

## Development 

For development it might be useful to install the package as a link to the repo so that the requirements are always updated when the repo changes:

```bash
pip install -e .
```

## Linting & Testing

This repository includes a Makefile and dockerfiles for conveniently running the linter ([pylint](https://www.pylint.org/)) and the unit tests ([pytest](https://docs.pytest.org/en/latest/)).
Recent versions of `docker` and `docker-compose` are required to run the following make targets.  

run the linter:
```bash
make lint
```
run the unit tests:
```bash
make test
```

the unit tests run the analysis over a set of golden log files and compare the current analysis results to stored ground truth results. The golden log files are described in the [README](https://github.com/Auterion/ecl_ekf_analysis/blob/master/tests/flight_logs/README.md) file.

## Usage 

The analysis can also be run using the provided docker file. Recent versions of `docker` and `docker-compose` are required to run the following make targets.

#### analyse a single ulog file
run `make analyse-file file=PATH/TO/THE/ULOG-FILE`. This should create a new `.json` file `ulog_filename.json` in the folder of the `.ulg` file containing the analysis results. 

#### analyse a directory of ulog files

run `make analyse-dir dir=PATH/TO/THE/LOG-FOLDER/` to create a new `.json` analytics result file for every `.ulg` file in the log folder.  

