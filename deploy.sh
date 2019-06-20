#!/bin/bash




# REMOTE_LOC_IP=
# REMOTE_NET_IP=

# ssh and run remote.sh

# MAYBE automatic version handling

# nao deploy script
DIR=`dirname "$0"`

echo "$DIR"
cd "$DIR"

echo "----creating dist----"
python setup.py sdist bdist_wheel

echo "----uploading to PYPI TEST----"
read -n 1
# python3 setup.py register -r pypitest
# python3 setup.py sdist upload -r pypitest
twine upload --repository pypitest dist/*


echo "----uploading to PYPI----"
read -n 1
# python3 setup.py register -r pypi
# python3 setup.py sdist upload -r pypi
twine upload --repository pypi dist/* 


# add repository (git push)