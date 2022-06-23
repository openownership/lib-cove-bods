import os
import tempfile

from libcovebods.api import bods_json_output


def test_not_in_old_schema():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.1", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.1"
    assert "count_person_statements_have_pep_status" not in results["statistics"]


def test_schema_0_2_basic_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "pep_status_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["statistics"]["count_person_statements_have_pep_status"] == 1
    # We want to test the dict has the correct keys!
    # So these tests are deliberately written so they will error if the specified key is not in that dict
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isPep"
        ]
        == 1
    )
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isNotPep"
        ]
        == 0
    )


def test_schema_0_2_missing_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "pep_status_missing_info_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["statistics"]["count_person_statements_have_pep_status"] == 1
    # We want to test the dict has the correct keys!
    # So these tests are deliberately written so they will error if the specified key is not in that dict
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isPep"
        ]
        == 1
    )
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isNotPep"
        ]
        == 0
    )


def test_schema_0_3_basic_1():
    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.3",
        "basic_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"
    assert results["statistics"]["count_person_statements_have_pep_status"] == 0
    # We want to test the dict has the correct keys!
    # So these tests are deliberately written so they will error if the specified key is not in that dict
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isPep"
        ]
        == 0
    )
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isNotPep"
        ]
        == 0
    )


def test_schema_0_3_pep_status_1():
    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.3",
        "pep_status_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"
    assert results["statistics"]["count_person_statements_have_pep_status"] == 1
    # We want to test the dict has the correct keys!
    # So these tests are deliberately written so they will error if the specified key is not in that dict
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isPep"
        ]
        == 1
    )
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isNotPep"
        ]
        == 0
    )
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "unknown"
        ]
        == 0
    )
