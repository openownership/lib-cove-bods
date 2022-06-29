# Lib Cove BODS

## Command line

### Installation

Installation from this git repo:

```bash
git clone https://github.com/openownership/lib-cove-bods.git
cd lib-cove-bods
python3 -m venv .ve
source .ve/bin/activate
pip install -e .
```

### Running the command line tool

Call `libcovebods` and pass the filename of some JSON data.

    libcovebods tests/fixtures/0.1/basic_1.json
    
You can also pass the raw option to see the JSON as it originally came out of the library.

    libcovebods --raw tests/fixtures/0.1/basic_1.json

### Running tests

    python -m pytest

### Code linting

Make sure dev dependencies are installed in your virtual environment:

    pip install -e .[dev]

Then run:

    isort libcovebods/ tests/ setup.py
    black libcovebods/ tests/ setup.py
    flake8 libcovebods/ tests/ setup.py

### Updating schema files in data

This library contains the actual data files for different versions of the schema, in the `libcovebods/data` directory.

To update them, you need:
 * a install of the Compile To JSON Schema Tool. https://compiletojsonschema.readthedocs.io/en/latest/index.html
 * a checkout of the data standard repository. https://github.com/openownership/data-standard

To update a file:

First go to your checkout of the data standard repository and make sure you have checked out the correct tag or branch.
ie. To update the `libcovebods/data/schema-0-2-0.json` file, check out `0.2.0`

Run the compile tool, telling it where the codelists directory is and pipe the output to the file for the version 
you have checked out:

    compiletojsonschema -c openownership-data-standard/schema/codelists/ openownership-data-standard/schema/bods-package.json > openownership-lib-cove-bods/libcovebods/data/schema-0-2-0.json  

Due to https://github.com/openownership/data-standard/issues/375 you may have to do some editing by hand when using early versions of the schema, pre 0.3. Open the files in `libcovebods/data`. At the top level there is an `oneOf` with 3 statement types - people, entity, and ownershipOrControl. In each of these statement types, there is an enum for the `statementType` field. This enum should have one option only - the value for whatever type of statement it is. (ie The person statement should only have the `personStatement` value). This tool may have added extra options - if so, remove them by hand.

## Code for use by external users

The only code that should be used directly by users is the `libcovebods.config` and `libcovebods.api` modules.

Other code ( Code in `lib`, etc) 
should not be used by external users of this library directly, as the structure and use of these may change more frequently.
