import tempfile
import os
import json
from libcovebods.api import bods_json_output
from libcovebods.config import LibCoveBODSConfig


def unpack_validation_error(validation_error_result):
    validation_error, data = validation_error_result
    validation_error_data = json.loads(validation_error)
    return validation_error_data, data


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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    for k in results['statistics']['count_entity_statements_types_with_any_identifier']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types_with_any_identifier'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types_with_any_identifier'][k] == 0
    for k in results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme'][k] == 1 # noqa
        else:
            assert results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme'][k] == 0 # noqa

    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0
    assert results['statistics']['count_replaces_statements_missing'] == 0


def test_basic_1_with_birth_year_to_early():

    config = LibCoveBODSConfig()
    config.config['bods_additional_checks_person_birthdate_min_year'] = 1970
    config.config['bods_additional_checks_person_birthdate_max_year'] = 2000

    # we reuse the basic1.json file here.
    # So we don't bother testing anything not related to year, as the normal 'basic_1.json' test will do that.
    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename, lib_cove_bods_config=config)

    assert results['additional_checks_count'] == 1

    assert results['additional_checks'][0]['type'] == 'person_birth_year_too_early'
    assert results['additional_checks'][0]['person_statement'] == '019a93f1-e470-42e9-957b-03559861b2e2'
    assert results['additional_checks'][0]['year'] == 1964


def test_basic_1_with_birth_year_to_late():

    config = LibCoveBODSConfig()
    config.config['bods_additional_checks_person_birthdate_min_year'] = 1900
    config.config['bods_additional_checks_person_birthdate_max_year'] = 1950

    # we reuse the basic1.json file here.
    # So we don't bother testing anything not related to year, as the normal 'basic_1.json' test will do that.
    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename, lib_cove_bods_config=config)

    assert results['additional_checks_count'] == 1

    assert results['additional_checks'][0]['type'] == 'person_birth_year_too_late'
    assert results['additional_checks'][0]['person_statement'] == '019a93f1-e470-42e9-957b-03559861b2e2'
    assert results['additional_checks'][0]['year'] == 1964


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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'legalEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        elif k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 0
    for k in results['statistics']['count_person_statements_types']:
        assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'influence-or-control':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement_by_year'] == {
        2017: 1
    }


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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 2
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 2
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 2
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

    assert results['additional_checks'][0]['type'] == 'person_statement_not_used_in_ownership_or_control_statement'
    assert results['additional_checks'][0]['person_statement'] == '891298d0-9b97-4d46-b776-d98927d72580'


def test_basic_extra_ownership_or_control_statement_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_extra_ownership_or_control_statements_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 3
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 3
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 3
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement_by_year'] == {
        2017: 1,
        2018: 2
    }


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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

    for validation_error, data in results['validation_errors']:
        validation_error_data = json.loads(validation_error)
        assert "'statementID' is missing but required" in validation_error_data['message']


def test_basic_statement_id_and_type_errors():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_statement_id_and_type_errors.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['file_type'] == 'json'
    assert results['validation_errors_count'] == 5
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0

    validation_error_data, data = unpack_validation_error(results['validation_errors'][0])
    assert "'shortID' is too short" in validation_error_data['message']
    assert data[0]['path'] == '1/statementID'
    assert data[0]['value'] == 'shortID'

    validation_error_data, data = unpack_validation_error(results['validation_errors'][1])
    assert "'statementID' is missing but required" in validation_error_data['message']
    assert data[0]['path'] == '0'
    assert data[1]['path'] == '2'

    validation_error_data, data = unpack_validation_error(results['validation_errors'][2])
    assert "'statementType' is missing but required" in validation_error_data['message']
    assert data[0]['path'] == '3'

    validation_error_data, data = unpack_validation_error(results['validation_errors'][3])
    assert "Invalid code found in 'statementType'" in validation_error_data['message']
    assert data[0]['path'] == '4/statementType'
    assert data[0]['value'] == 'test'

    assert results['additional_checks'][0]['type'] == 'person_statement_not_used_in_ownership_or_control_statement'
    assert results['additional_checks'][0]['person_statement'] == 'shortID'


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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0


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
    for k in results['statistics']['count_entity_statements_types']:
        assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 0
    for k in results['statistics']['count_person_statements_types']:
        assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 0
    for k in results['statistics']['count_person_statements_types']:
        assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 2
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 0
    for k in results['statistics']['count_person_statements_types']:
        assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

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
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

    assert results['additional_checks'][0]['type'] == 'entity_identifier_scheme_not_known'
    assert results['additional_checks'][0]['scheme'] == 'GB-COH-THIS-SCHEME-IS-NOT-REAL-I-JUST-MADE-IT-UP-MWAHAHAHAHA'
    assert results['additional_checks'][0]['entity_statement'] == '1dc0e987-5c57-4a1c-b3ad-61353b66a9b7'


def test_basic_anonymous_person_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_anonymous_person_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'anonymousPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0


def test_unknown_basic_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_unknown_person_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'unknownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0


def test_basic_unknown_owner_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_unknown_owner_1.json'
    )
    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 0
    for k in results['statistics']['count_person_statements_types']:
        assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 1
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0


def test_basic_duplicate_statement_id_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_duplicate_statement_id_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 1

    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0

    assert results['additional_checks'][0]['type'] == 'duplicate_statement_id'
    assert results['additional_checks'][0]['id'] == '019a93f1-e470-42e9-957b-03559861b2e2'
    assert results['additional_checks'][0]['count'] == 2


def test_basic_entity_with_no_ids_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_entity_with_no_ids_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    for k in results['statistics']['count_entity_statements_types_with_any_identifier']:
        assert results['statistics']['count_entity_statements_types_with_any_identifier'][k] == 0
    for k in results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme']:
        assert results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme'][k] == 0

    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0


def test_basic_basic_entity_with_id_with_scheme_name_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_entity_with_id_with_scheme_name_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    for k in results['statistics']['count_entity_statements_types_with_any_identifier']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types_with_any_identifier'][k] == 1
        else:
            assert results['statistics']['count_entity_statements_types_with_any_identifier'][k] == 0
    for k in results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme']:
        assert results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme'][k] == 0

    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 1
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0


def test_replaces_statements():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_replaces_statements.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['additional_checks_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 2
    for k in results['statistics']['count_entity_statements_types']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types'][k] == 2
        else:
            assert results['statistics']['count_entity_statements_types'][k] == 0
    for k in results['statistics']['count_entity_statements_types_with_any_identifier']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types_with_any_identifier'][k] == 2
        else:
            assert results['statistics']['count_entity_statements_types_with_any_identifier'][k] == 0
    for k in results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme']:
        if k == 'registeredEntity':
            assert results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme'][k] == 2 # noqa
        else:
            assert results['statistics']['count_entity_statements_types_with_any_identifier_with_id_and_scheme'][k] == 0 # noqa

    assert results['statistics']['count_person_statements'] == 1
    for k in results['statistics']['count_person_statements_types']:
        if k == 'knownPerson':
            assert results['statistics']['count_person_statements_types'][k] == 1
        else:
            assert results['statistics']['count_person_statements_types'][k] == 0
    assert results['statistics']['count_ownership_or_control_statement'] == 2
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 2
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 2
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0
    assert results['statistics']['count_replaces_statements_missing'] == 3
    assert results['statistics']['count_ownership_or_control_statement_by_year'] == {
        2017: 1,
        2018: 1
    }


def test_bad_statement_date():
    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'bad_statement_date.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)
    assert results['statistics']['count_ownership_or_control_statement_by_year'] == {2011: 1}
