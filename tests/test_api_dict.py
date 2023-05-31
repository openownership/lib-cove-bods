import os
import tempfile

from tests.api import bods_json_output

# Schema version of a dict is not allowed - it must be a string!
# This file has tests to make sure that this mistake is picked up and reported by this library.


def test_basic_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "dict", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"
    assert results["validation_errors_count"] == 3
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1
    assert results["additional_checks"][0]["type"] == "unknown_schema_version_used"
    assert results["additional_checks"][0]["schema_version"] == "{}"
