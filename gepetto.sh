#!/bin/bash
############################
# Gepetto can be used inside a Docker container; it installs your package, 
# executes any bash command given as an argument and gets rid of the py* overhead 
# in your containers file system. 
#
# Use e.g.:
# docker-compose run --rm -w /code container_name bash -c "./gepetto.sh 'pytest -vv tests/*'"
############################

COMMAND="$1"

set -e .
python setup.py develop 
$COMMAND
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf