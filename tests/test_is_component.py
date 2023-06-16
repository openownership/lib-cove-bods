import os
import tempfile

from tests.api import bods_json_output


def test_iscomponent_true_but_has_component_statement_ids_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "iscomponent_true_but_has_component_statement_ids_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["additional_checks_count"] == 1

    assert (
        results["additional_checks"][0]["type"]
        == "ownership_or_control_statement_has_is_compontent_and_component_statement_ids"
    )  # noqa
    assert (
        results["additional_checks"][0]["statement"]
        == "12340547-d0c6-4a00-b559-5c5e91c34f5d"
    )


def test_component_statement_ids_not_in_package_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "component_statement_ids_not_in_package_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["additional_checks_count"] == 1

    assert (
        results["additional_checks"][0]["type"]
        == "component_statement_id_not_in_package"
    )
    assert (
        results["additional_checks"][0]["seen_in_ownership_or_control_statement"]
        == "fbfd0547-d0c6-4a00-b559-5c5e91c34f5c"
    )  # noqa
    assert (
        results["additional_checks"][0]["component_statement_id"]
        == "000a00a0-a000-00a0-000a-00000000a0a0"
    )


def test_statement_is_component_but_is_not_used_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "statement_is_component_but_is_not_used_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["additional_checks_count"] == 1

    assert (
        results["additional_checks"][0]["type"]
        == "statement_is_component_but_not_used_in_component_statement_ids"
    )
    assert (
        results["additional_checks"][0]["statement"]
        == "426b7dc8-8b7a-4d50-93de-8e200a4aedf5"
    )
    assert results["additional_checks"][0]["statement_type"] == "ownership_or_control"


def test_statement_is_component_but_is_used_in_the_wrong_order_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "statement_is_component_but_is_used_in_the_wrong_order_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["additional_checks_count"] == 1

    assert (
        results["additional_checks"][0]["type"]
        == "statement_is_component_but_is_after_use_in_component_statement_id"
    )  # noqa
    assert (
        results["additional_checks"][0]["statement"]
        == "24e604f2-790f-4600-8ff2-7fd8e46f047e"
    )
    assert results["additional_checks"][0]["statement_type"] == "ownership_or_control"
