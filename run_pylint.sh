#! /bin/bash
# execute pylint on the source

set -e

export PYTHONPATH=$PYTHONPATH:src/ecl_ekf_analysis

echo "lint source code"
pylint --rcfile=/app/pylintrc src/

echo "lint unit tests"
pylint --rcfile=/app/pylintrc --disable=redefined-outer-name,import-error tests/

exit 0
