import tempfile
import os
import json
from libcovebods.api import bods_json_output


def test_basic_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0


def test_basic_2():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_2.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 2
    assert results['statistics']['count_person_statements'] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 1


def test_basic_extra_entity_statement_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_extra_entity_statement_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 2
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0

    assert results['additional_checks'][0]['type'] == 'entity_statement_not_used_in_ownership_or_control_statement'
    assert results['additional_checks'][0]['entity_statement'] == '9bf27aa7-f372-41d7-9429-1bcd8b0f475d'


def test_basic_extra_person_statement_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_extra_person_statement_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 2
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0

    assert results['additional_checks'][0]['type'] == 'person_statement_not_used_in_ownership_or_control_statement'
    assert results['additional_checks'][0]['person_statement'] == '891298d0-9b97-4d46-b776-d98927d72580'


def test_basic_extra_ownership_or_control_statement_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_extra_ownership_or_control_statement_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 2
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 2
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0


def test_basic_missing_statement_ids():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_missing_statement_ids.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['file_type'] == 'json'
    assert results['validation_errors_count'] == 3
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0

    for validation_error, data in results['validation_errors']:
        validation_error_data = json.loads(validation_error)
        assert "'statementID' is missing but required" in validation_error_data['message']


def test_additional_fields_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_additional_fields_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 2
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['data_only'] == [('', 'cats', 1), ('', 'dogs', 1)]
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0


def test_basic_missing_entity_statement_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_missing_entity_statement_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 0
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0

    assert results['additional_checks'][0]['type'] == 'entity_statement_missing'
    assert results['additional_checks'][0]['missing_from'] == 'subject'
    assert results['additional_checks'][0]['entity_statement_missing'] == '1dc0e987-5c57-4a1c-b3ad-61353b66a9b7'
    assert results['additional_checks'][0]['seen_in_ownership_or_control_statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c' # noqa


def test_basic_missing_entity_statement_2():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_missing_entity_statement_2.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 1

    assert results['additional_checks'][0]['type'] == 'entity_statement_missing'
    assert results['additional_checks'][0]['missing_from'] == 'interestedParty'
    assert results['additional_checks'][0]['entity_statement_missing'] == '019a93f1-e420-42e9-957b-03559861b2e2'
    assert results['additional_checks'][0]['seen_in_ownership_or_control_statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c' # noqa


def test_basic_missing_person_statement_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_missing_person_statement_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0

    assert results['additional_checks'][0]['type'] == 'person_statement_missing'
    assert results['additional_checks'][0]['missing_from'] == 'interestedParty'
    assert results['additional_checks'][0]['person_statement_missing'] == '019a93f1-e470-42e9-957b-03559861b2e2'
    assert results['additional_checks'][0]['seen_in_ownership_or_control_statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c' # noqa


def test_basic_1_wrong_order_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_1_wrong_order_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0

    assert results['additional_checks'][0]['type'] == 'entity_statement_out_of_order'
    assert results['additional_checks'][0]['referenced_from'] == 'subject'
    assert results['additional_checks'][0]['entity_statement_out_of_order'] == '1dc0e987-5c57-4a1c-b3ad-61353b66a9b7'
    assert results['additional_checks'][0]['seen_in_ownership_or_control_statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c' # noqa


def test_basic_1_wrong_order_2():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_1_wrong_order_2.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0

    assert results['additional_checks'][0]['type'] == 'person_statement_out_of_order'
    assert results['additional_checks'][0]['referenced_from'] == 'interestedParty'
    assert results['additional_checks'][0]['person_statement_out_of_order'] == '019a93f1-e470-42e9-957b-03559861b2e2'
    assert results['additional_checks'][0]['seen_in_ownership_or_control_statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c' # noqa


def test_basic_2_wrong_order_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_2_wrong_order_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 2
    assert results['statistics']['count_person_statements'] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 1

    assert results['additional_checks'][0]['type'] == 'entity_statement_out_of_order'
    assert results['additional_checks'][0]['referenced_from'] == 'interestedParty'
    assert results['additional_checks'][0]['entity_statement_out_of_order'] == '9bf27aa7-f372-41d7-9429-1bcd8b0f475d'
    assert results['additional_checks'][0]['seen_in_ownership_or_control_statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c' # noqa


def test_basic_bad_identifier_scheme():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_bad_identifier_scheme.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0

    assert results['additional_checks'][0]['type'] == 'entity_identifier_scheme_not_known'
    assert results['additional_checks'][0]['scheme'] == 'GB-COH-THIS-SCHEME-IS-NOT-REAL-I-JUST-MADE-IT-UP-MWAHAHAHAHA'
    assert results['additional_checks'][0]['entity_statement'] == '1dc0e987-5c57-4a1c-b3ad-61353b66a9b7'
