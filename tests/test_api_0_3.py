import os
import tempfile

from libcovebods.api import bods_json_output


def test_basic_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.3", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_has_public_listing_information_but_has_public_listing_is_false_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.3",
        "has_public_listing_information_but_has_public_listing_is_false_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0

    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "has_public_listing_information_but_has_public_listing_is_false"
    )
    assert (
        results["additional_checks"][0]["statement"]
        == "1dc0e987-5c57-4a1c-b3ad-61353b66a9b7"
    )


def test_entity_sub_type_does_not_align_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.3",
        "entity_sub_type_does_not_align_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0

    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "statement_entity_type_and_entity_sub_type_do_not_align"
    )
    assert (
        results["additional_checks"][0]["statement"]
        == "1dc0e987-5c57-4a1c-b3ad-61353b66a9b7"
    )


def test_entity_sub_type_does_align_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.3",
        "entity_sub_type_does_align_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_basic_with_correct_mic_codes_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.3",
        "basic_with_correct_mic_codes_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_basic_with_operating_mic_code_missing_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.3",
        "basic_with_operating_mic_code_missing_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0

    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "entity_security_listing_market_identifier_code_set_but_not_operating_market_identifier_code"
    )
    assert results["additional_checks"][0]["statement_type"] == "entity"
    assert (
        results["additional_checks"][0]["statement"]
        == "1dc0e987-5c57-4a1c-b3ad-61353b66a9b7"
    )
