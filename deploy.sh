#!/bin/bash




# REMOTE_LOC_IP=
# REMOTE_NET_IP=

# ssh and run remote.sh

# MAYBE automatic version handling

# nao deploy script
DIR=`dirname "$0"`

echo "$DIR"
cd "$DIR"

echo "PYPI TEST"
python3 setup.py register -r pypitest
python3 setup.py sdist upload -r pypitest

read -n 1

echo "PYPI"
python3 setup.py register -r pypi
python3 setup.py sdist upload -r pypi


# add repository (git push)