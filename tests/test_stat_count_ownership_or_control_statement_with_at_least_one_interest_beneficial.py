import os
import tempfile

from libcovebods.api import bods_json_output


def test_schema_0_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.2", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"

    assert (
        1
        == results["statistics"][
            "count_ownership_or_control_statement_with_at_least_one_interest_beneficial"
        ]
    )


def test_schema_0_2_statement_is_component_but_is_not_used_1():

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

    assert (
        2
        == results["statistics"][
            "count_ownership_or_control_statement_with_at_least_one_interest_beneficial"
        ]
    )


def test_schema_0_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.3", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"

    assert (
        1
        == results["statistics"][
            "count_ownership_or_control_statement_with_at_least_one_interest_beneficial"
        ]
    )
