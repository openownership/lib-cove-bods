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

## Code for use by external users

The only code that should be used directly by users is the `libcovebods.config` and `libcovebods.api` modules.

Other code ( Code in `lib`, etc) 
should not be used by external users of this library directly, as the structure and use of these may change more frequently.
