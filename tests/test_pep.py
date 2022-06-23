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
    assert results["additional_checks_count"] == 0


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

    assert results["additional_checks_count"] == 0


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
        == 0
    )
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isNotPep"
        ]
        == 1
    )

    assert results["additional_checks_count"] == 0


def test_schema_0_2_pep_details_no_missing_info_but_incorrect_status_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "pep_details_no_missing_info_but_incorrect_status_1.json",
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
        == 0
    )
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isNotPep"
        ]
        == 1
    )

    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "has_pep_details_without_missing_info_but_incorrect_pep_status"
    )
    assert results["additional_checks"][0]["statement_type"] == "person"
    assert (
        results["additional_checks"][0]["statement"]
        == "a5680770-899f-4f7a-b795-e266f1ce8668"
    )


def test_schema_0_2_pep_details_missing_info_but_incorrect_status_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "pep_details_missing_info_but_incorrect_status_1.json",
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

    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "has_pep_details_with_missing_info_but_incorrect_pep_status"
    )
    assert results["additional_checks"][0]["statement_type"] == "person"
    assert (
        results["additional_checks"][0]["statement"]
        == "a5680770-899f-4f7a-b795-e266f1ce8668"
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

    assert results["additional_checks_count"] == 0


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

    assert results["additional_checks_count"] == 0


def test_schema_0_3_pep_details_but_incorrect_status_1():
    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.3",
        "pep_details_but_incorrect_status_1.json",
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
        == 0
    )
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isNotPep"
        ]
        == 1
    )
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "unknown"
        ]
        == 0
    )

    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "has_pep_details_but_incorrect_pep_status"
    )
    assert results["additional_checks"][0]["statement_type"] == "person"
    assert (
        results["additional_checks"][0]["statement"]
        == "019a93f1-e470-42e9-957b-03559861b2e2"
    )


def test_schema_0_3_pep_details_missing_info_but_incorrect_status_1():
    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.3",
        "pep_details_missing_info_but_incorrect_status_1.json",
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

    assert results["additional_checks_count"] == 1
    assert (
        results["additional_checks"][0]["type"]
        == "has_pep_details_with_missing_info_but_incorrect_pep_status"
    )
    assert results["additional_checks"][0]["statement_type"] == "person"
    assert (
        results["additional_checks"][0]["statement"]
        == "019a93f1-e470-42e9-957b-03559861b2e2"
    )
