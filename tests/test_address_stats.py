import os
import tempfile

from tests.api import bods_json_output


def test_basic_address_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.1",
        "basic_address_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.1"

    assert results["statistics"]["count_addresses"] == 1
    assert results["statistics"]["count_addresses_with_postcode"] == 0
    assert results["statistics"]["count_addresses_with_country"] == 0
    assert (
        results["statistics"]["count_addresses_with_postcode_duplicated_in_address"]
        == 0
    )


def test_basic_address_with_country_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.1",
        "basic_address_with_country_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.1"

    assert results["statistics"]["count_addresses"] == 1
    assert results["statistics"]["count_addresses_with_postcode"] == 0
    assert results["statistics"]["count_addresses_with_country"] == 1
    assert (
        results["statistics"]["count_addresses_with_postcode_duplicated_in_address"]
        == 0
    )


def test_basic_address_with_postcode_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.1",
        "basic_address_with_postcode_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.1"

    assert results["statistics"]["count_addresses"] == 1
    assert results["statistics"]["count_addresses_with_postcode"] == 1
    assert results["statistics"]["count_addresses_with_country"] == 0
    assert (
        results["statistics"]["count_addresses_with_postcode_duplicated_in_address"]
        == 0
    )


def test_basic_address_with_postcode_in_address_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.1",
        "basic_address_with_postcode_in_address_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.1"

    assert results["statistics"]["count_addresses"] == 1
    assert results["statistics"]["count_addresses_with_postcode"] == 1
    assert results["statistics"]["count_addresses_with_country"] == 0
    assert (
        results["statistics"]["count_addresses_with_postcode_duplicated_in_address"]
        == 1
    )
