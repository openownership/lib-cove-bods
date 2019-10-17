#!/bin/bash

virtualenv .travis.upgrade.needed.ve -p python3
source .travis.upgrade.needed.ve/bin/activate

pip install -e .
pip install -r requirements_dev.in
pip freeze > requirements_dev_new.txt
sed -i 's/pkg-resources==0.0.0//' requirements_dev_new.txt
sed -i 's/^-e.*//' requirements_dev_new.txt
diff -B -b -w requirements_dev.txt requirements_dev_new.txt >  requirements_dev_new.diff


if [ -s requirements_dev_new.diff ]
then
     echo "LOCKED DEPENDENCIES ARE NOT THE LATEST POSSIBLE"
     cat requirements_dev_new.diff
     exit 1
else
     echo "The locked dependencies are already the latest version - cool"
     exit 0
fi