import json
import os
import tempfile

from tests.api import bods_json_output


def test_basic_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.2", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_iscompontent_os_03_dr_03():
    """This is a piece of sample data direct from the schema with iscomponent / componentStatementIDs data.
    Make sure it passes all our tests"""

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "iscompontent-os-03-dr-03.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_bad_statement_id_type():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "bad_statement_id_type.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["validation_errors_count"] == 1
    validation_error = json.loads(results["validation_errors"][0][0])
    assert validation_error["message"].startswith("'statementID' should be a string.")
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0
