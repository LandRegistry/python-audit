#!/usr/bin/env bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $dir
source ./environment-test.sh

py.test  --junitxml=python_logging.xml  --cov setup_logging --cov-report term-missing -v tests "$@"
