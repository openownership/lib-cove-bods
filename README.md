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

## Running the command line tool

Call `libcovebods`.

    libcovebods -h

## Running tests

    python -m pytest

## Code linting

Make sure dev dependencies are installed in your virtual environment:

    pip install -e .[dev]

Then run:

    isort libcovebods/ tests/ setup.py
    black libcovebods/ tests/ setup.py
    flake8 libcovebods/ tests/ setup.py

## Changes for BODS 0.4

## Version Identification

The library configuration (`libcovebods/tasks/config.py`) contains various schema versions
which control affect the  These include `schema_version` (e.g. 0.1) which is the default for
older data, the latest schema version `schema_latest_version` ( e.g. 0.4), or latest version
before change to record-based schema `schema_latest_nonrecord_version` (e.g. 0.3). If the data
does not specify a BODS version the library will attempt to identify whether the data is
record-based (0.4 or newer), and use a default version based on this.

### Changes to standard

From BODS version 0.4 onward the data standard is significantly different, record-based and linking components via URNs. The schema
consists of a directory of schema files, rather than a single schema file, and the various [JSON Schema](https://json-schema.org/)
files are linked via URNs, e.g. `"$ref": "urn:person"` in `statement.json` refers to `"$id": "urn:person"` in `person-record.json`.
The library loads the BODS schema files into a JSON Schema registry, so the validator can resolve $refs across all of the schema files.

### Refactoring of checks

The various checks (in `libcovebods/tasks/checks`) have been broken up into legacy_checks, pre_record_checks and record_based_checks.
The legacy_checks and pre_record_checks only apply to pre 0.4 data, whereas the record_based_checks only apply to BODS data with
version 0.4 onwards.

## Updating schema files in data

This library contains the actual data files for different versions of the schema, in the `libcovebods/data` directory.

### BODS Schema from 0.4 onwards

Each version schema (from 0.4 onwards) is contained in a directory containing a number [JSON Schema](https://json-schema.org/) files, e.g. `libcovebods/data/schema-0-4-0`.

To update them, you need:
 * a checkout of the data standard repository. https://github.com/openownership/data-standard

To update a file:

First go to your checkout of the data standard repository and make sure you have checked out the correct tag or branch.
ie. To update the `libcovebods/data/schema-0-4-0` directory, check out `0.4.0`.

Remove any existing directory (e.g. `rm -r openownership-lib-cove-bods/libcovebods/data/schema-0-4-0`) and copy the schema directory over
(e.g. `cp -r openownership-data-standard/schema openownership-lib-cove-bods/libcovebods/data/schema-0-4-0`).
No conversion of the files is needed, unlike for per BODS 0.4 versions.

### BODS Schema before 0.4

Each version schema (before 0.4) is contained in a single file in [JSON Schema](https://json-schema.org/) format, e.g. `libcovebods/data/schema-0-2-0.json`.

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

