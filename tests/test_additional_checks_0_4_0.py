import os
import tempfile

from tests.api import bods_json_output


def test_retrievedat_not_future_date_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "retrievedat_not_future_date-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_retrievedat_not_future_date_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "retrievedat_not_future_date-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_retrievedat_not_future_date_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "retrievedat_not_future_date-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_retrievedat_not_future_date_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "retrievedat_not_future_date-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_date_not_future_date_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_date_not_future_date-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_date_not_future_date_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_date_not_future_date-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_date_not_future_date_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_date_not_future_date-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_creation_date_not_future_date_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_annotation_creation_date_future_date-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_creation_date_not_future_date_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_annotation_creation_date_future_date-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_creation_date_not_future_date_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_annotation_creation_date_future_date-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_publication_date_future_date_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_publication_date_future_date-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_publication_date_future_date_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_publication_date_future_date-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_publication_date_future_date_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_publication_date_future_date-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_publication_date_future_date_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_publication_date_future_date-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_person_date_of_death_sane_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_date_of_death_sane-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_date_of_death_sane_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_date_of_death_sane-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_date_of_death_sane_invalid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_date_of_death_sane-invalid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_date_of_death_sane_invalid_4():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_date_of_death_sane-invalid-4.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_date_of_death_sane_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_date_of_death_sane-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_person_date_of_death_sane_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_date_of_death_sane-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_entity_foundation_dissolution_dates_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_foundation_dissolution_dates-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_entity_foundation_dissolution_dates_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_foundation_dissolution_dates-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_entity_foundation_dissolution_dates_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_foundation_dissolution_dates-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_person_birth_date_sensible_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_birth_date_sensible-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_birth_date_sensible_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_birth_date_sensible-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_birth_date_sensible_invalid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_birth_date_sensible-invalid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_birth_date_sensible_invalid_4():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_birth_date_sensible-invalid-4.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_birth_date_sensible_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_birth_date_sensible-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_person_birth_date_sensible_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_birth_date_sensible-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_relationship_interests_start_end_dates_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interests_start_end_dates-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_interests_start_end_dates_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interests_start_end_dates-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_relationship_interests_start_end_dates_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interests_start_end_dates-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_entity_securities_listings_haspubliclisting_not_false_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_securities_listings_haspubliclisting_not_false-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_entity_securities_listings_haspubliclisting_not_false_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_securities_listings_haspubliclisting_not_false-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_entity_securities_listings_haspubliclisting_not_false_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_securities_listings_haspubliclisting_not_false-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_relationship_interests_share_values_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interests_share_values-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_interests_share_values_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interests_share_values-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_interests_share_values_invalid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interests_share_values-invalid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_interests_share_values_invalid_4():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interests_share_values-invalid-4.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_interests_share_values_invalid_5():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interests_share_values-invalid-4.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_interests_share_values_invalid_6():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interests_share_values-invalid-6.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_declaration_subject_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_declaration_subject-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_declaration_subject_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_declaration_subject-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_declaration_subject_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_declaration_subject-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_entity_is_component_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_is_component-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_entity_is_component_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_is_component-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 3  # 2 extra ordering errors


def test_statement_entity_is_component_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_is_component-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_person_is_component_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_is_component-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 2  # Extra ordering error


def test_statement_person_is_component_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_is_component-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_is_component_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_is_component-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_relationship_is_component_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_is_component-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_is_component_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_is_component-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_is_component_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_is_component-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_duplicate_statement_id_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_must_have_unique_statement_identifier-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_duplicate_statement_id_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_must_have_unique_statement_identifier-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_duplicate_statement_id_invalid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_must_have_unique_statement_identifier-invalid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_duplicate_statement_id_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_must_have_unique_statement_identifier-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_series_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_series-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_series_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_series-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_series_invalid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_series-invalid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_series_invalid_4():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_series-invalid-4.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_series_invalid_5():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_series-invalid-5.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_series_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_series-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_series_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_series-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_relationship_component_records_are_record_ids_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_component_records_are_record_ids-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_component_records_are_record_ids_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_component_records_are_record_ids-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_relationship_component_records_are_record_ids_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_component_records_are_record_ids-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_relationship_subject_refers_to_entity_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_subject_refers_to_entity_statement-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_relationship_subject_refers_to_entity_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_subject_refers_to_entity_statement-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_relationship_subject_refers_to_entity_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_subject_refers_to_entity_statement-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_relationship_interested_party_entity_or_person_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_relationship_interested_party_entity_or_person-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_annotiation_statement_pointer_target_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "annotiation_statement_pointer_target-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_annotiation_statement_pointer_target_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "annotiation_statement_pointer_target-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_annotiation_statement_pointer_target_invalid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "annotiation_statement_pointer_target-invalid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_annotiation_statement_pointer_target_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "annotiation_statement_pointer_target-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_annotiation_statement_pointer_target_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "annotiation_statement_pointer_target-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_interested_party_person_with_beneficial_ownership_or_control_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "interested_party_person_with_beneficial_ownership_or_control-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_interested_party_person_with_beneficial_ownership_or_control_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "interested_party_person_with_beneficial_ownership_or_control-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_interested_party_person_with_beneficial_ownership_or_control_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "interested_party_person_with_beneficial_ownership_or_control-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_relationship_interest_nominee_or_nominator_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "relationship_interest_nominee_or_nominator-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_relationship_interest_nominee_or_nominator_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "relationship_interest_nominee_or_nominator-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_relationship_interest_nominee_or_nominator_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "relationship_interest_nominee_or_nominator-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_relationship_interest_for_trusts_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "relationship_interest_for_trusts-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_relationship_interest_for_trusts_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "relationship_interest_for_trusts-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_relationship_interest_for_trusts_invalid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "relationship_interest_for_trusts-invalid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_relationship_interest_for_trusts_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "relationship_interest_for_trusts-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_relationship_interest_for_trusts_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "relationship_interest_for_trusts-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_relationship_interest_for_trusts_valid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "relationship_interest_for_trusts-valid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_serialisation_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_serialisation-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_serialisation_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_serialisation-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_serialisation_invalid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_serialisation-invalid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_serialisation_invalid_4():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_serialisation-invalid-4.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_serialisation_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_serialisation-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_person_identifiers_have_correct_scheme_invalid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_identifiers_have_correct_scheme-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_identifiers_have_correct_scheme_invalid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_identifiers_have_correct_scheme-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_identifiers_have_correct_scheme_invalid_3():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_identifiers_have_correct_scheme-invalid-3.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_identifiers_have_correct_scheme_invalid_4():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_identifiers_have_correct_scheme-invalid-4.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_identifiers_have_correct_scheme_invalid_5():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_identifiers_have_correct_scheme-invalid-5.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_identifiers_have_correct_scheme_invalid_6():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_identifiers_have_correct_scheme-invalid-6.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_person_identifiers_have_correct_scheme_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_identifiers_have_correct_scheme-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_person_identifiers_have_correct_scheme_valid_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_person_identifiers_have_correct_scheme-valid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0


def test_statement_entity_identifier_scheme_known_invalid_1():
    # Testing CheckStatementEntityIdentifiersHaveKnownScheme

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_identifier_scheme_known-invalid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_entity_identifier_scheme_known_invalid_2():
    # Testing CheckStatementEntityIdentifiersHaveKnownScheme

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_identifier_scheme_known-invalid-2.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 1


def test_statement_entity_identifier_scheme_known_valid_1():
    # Testing CheckStatementEntityIdentifiersHaveKnownScheme

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "additional-checks",
        "statement_entity_identifier_scheme_known-valid-1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 0
    assert results["additional_checks_count"] == 0
