# Lib Cove BODS


## Command line

Call `libcovebods` and pass the filename of some JSON data.

    libcovebods tests/fixtures/0.1/basic_1.json

You can also pass the raw option to see the JSON as it originally came out of the library.

    libcovebods --raw tests/fixtures/0.1/basic_1.json

## Code for use by external users

The only code that should be used directly by users is the `libcovebods.config` and `libcovebods.api` modules.

Other code ( Code in `lib`, etc)
should not be used by external users of this library directly, as the structure and use of these may change more frequently.

## FAQ: libcovebods: command not found ?

If installed via

    virtualenv .ve -p python3
    source .ve/bin/activate
    pip3 install -r requirements.txt

You may get

    libcovebods tests/fixtures/0.1/basic_1.json
    libcovebods: command not found

To fix, run

    pip3 install -e .

We are looking at a proper fix for this problem in https://github.com/openownership/lib-cove-bods/issues/19

## Running tests

In an activated virtualenv, with requirements_dev.txt installed:

    python -m pytest
