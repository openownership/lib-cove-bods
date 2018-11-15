# Lib Cove BODS


## Command line

Call `libcovebods` and pass the filename of some JSON data.

    libcovebods tests/fixtures/api/basic_1.json

## Code for use by external users

The only code that should be used directly by users is the `libcovebods.config` and `libcovebods.api` modules.

Other code ( Code in `lib`, etc) 
should not be used by external users of this library directly, as the structure and use of these may change more frequently.
