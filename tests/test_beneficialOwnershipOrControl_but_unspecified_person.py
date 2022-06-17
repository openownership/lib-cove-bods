import os
import tempfile

from libcovebods.api import bods_json_output


def test_schema_0_1_file_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.1",
        "beneficialOwnershipOrControl_but_unspecified_person_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.1"

    assert results["validation_errors_count"] == 0
    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "statement_is_beneficialOwnershipOrControl_but_no_person_specified"
    )


def test_schema_0_1_file_2():
    """In this case, the interested party is another entity - it should be a person."""

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.1",
        "beneficialOwnershipOrControl_but_unspecified_person_2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.1"

    assert results["validation_errors_count"] == 0
    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "statement_is_beneficialOwnershipOrControl_but_no_person_specified"
    )


def test_schema_0_2_file_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "beneficialOwnershipOrControl_but_unspecified_person_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"

    assert results["validation_errors_count"] == 0
    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "statement_is_beneficialOwnershipOrControl_but_no_person_specified"
    )
