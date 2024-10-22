import json
import os
import tempfile

from tests.api import bods_json_output


def test_additional_fields_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.4", "additional_fields_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    print(results)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 2
    assert results["additional_checks_count"] == 0

    assert False
