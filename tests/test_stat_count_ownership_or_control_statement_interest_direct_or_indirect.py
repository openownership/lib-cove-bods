import os
import tempfile

from tests.api import bods_json_output


def test_schema_0_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.2", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"

    # Schema v0.1 and Schema v0.2 do not have this stat at all.
    assert (
        "count_ownership_or_control_statement_interest_direct_or_indirect"
        not in results["statistics"].keys()
    )


def test_schema_0_3_basic_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.3", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"

    # We want to test the dict has the correct keys!
    # So these tests are deliberately written so they will error if the specified key is not in that dict
    assert (
        1
        == results["statistics"][
            "count_ownership_or_control_statement_interest_direct_or_indirect"
        ]["direct"]
    )
    assert (
        0
        == results["statistics"][
            "count_ownership_or_control_statement_interest_direct_or_indirect"
        ]["indirect"]
    )
    assert (
        0
        == results["statistics"][
            "count_ownership_or_control_statement_interest_direct_or_indirect"
        ]["unknown"]
    )
