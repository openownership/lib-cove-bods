#!/bin/bash
# This follows broadly the approach from
# http://www.kennethreitz.org/essays/a-better-pip-workflow but with the
# addition of requirements_dev

# Delete and recreate a virtualenv to ensure that we don't have any extra
# packages installed in it
rm -rf .ve
virtualenv --python=python3 .ve
source .ve/bin/activate

pip install -e .
pip install -r requirements_dev.in
pip freeze > requirements_dev.txt

sed -i 's/pkg-resources==0.0.0//' requirements_dev.txt
sed -i 's/^-e.*//' requirements_dev.txt