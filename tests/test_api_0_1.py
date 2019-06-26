import tempfile
import os
import json
import pytest
from libcovebods.api import bods_json_output
from libcovebods.config import LibCoveBODSConfig


BADFILE_RESULTS = [
    ({'message': "'entityType' is missing but required. Check that the field is included and correctly spelled.", 'message_safe': '<code>entityType</code> is missing but required. Check that the field is included and correctly spelled.', 'message_type': 'required', 'path_no_number': ''}, [{'path': '21'}]), # noqa
    ({'message': "'exact' should be a number. Check that the value is not null, and doesn’t contain any characters other than 0-9 and dot ('.'). Number values should not be in quotes. ", 'message_safe': '<code>exact</code> should be a number. Check that the value is not null, and doesn’t contain any characters other than 0-9 and dot (<code>.</code>). Number values should not be in quotes. ', 'message_type': 'number', 'path_no_number': 'interests/share/exact'}, [{'path': '16/interests/0/share/exact', 'value': 'not a number'}]), # noqa
    ({'message': "'exclusiveMinimum' should be a JSON boolean, 'true' or 'false'.", 'message_safe': '<code>exclusiveMinimum</code> should be a JSON boolean, <code>true</code> or <code>false</code>.', 'message_type': 'boolean', 'path_no_number': 'interests/share/exclusiveMinimum'}, [{'path': '19/interests/0/share/exclusiveMinimum', 'value': 'not a bool'}]), # noqa
    ({'message': "'interestedParty' is missing but required. Check that the field is included and correctly spelled.", 'message_safe': '<code>interestedParty</code> is missing but required. Check that the field is included and correctly spelled.', 'message_type': 'required', 'path_no_number': ''}, [{'path': '16'}, {'path': '17'}, {'path': '18'}, {'path': '19'}, {'path': '20'}]), # noqa
    ({'message': "'interests' should be a JSON array. Check that value(s) appear within square brackets, [...]", 'message_safe': '<code>interests</code> should be a JSON array. Check that value(s) appear within square brackets, [...]', 'message_type': 'array', 'path_no_number': 'interests'}, [{'path': '17/interests'}]), # noqa
    ({'message': "'interests/0' should be a JSON object", 'message_safe': '<code>interests/0</code> should be a JSON object', 'message_type': 'object', 'path_no_number': 'interests'}, [{'path': '18/interests/0', 'value': 'not an object'}]), # noqa
    ({'message': "'missingPersonType' is a dependency of 'missingPersonReason'", 'message_safe': '&#39;missingPersonType&#39; is a dependency of &#39;missingPersonReason&#39;', 'message_type': 'dependencies', 'path_no_number': ''}, [{'path': '14'}]), # noqa
    ({'message': "'motivation' contains an unrecognised value. Check the related codelist for allowed code values.", 'message_safe': '<code>motivation</code> contains an unrecognised value. Check the related codelist for allowed code values.', 'message_type': 'enum', 'path_no_number': 'annotations/motivation'}, [{'path': '20/annotations/0/motivation', 'value': 'not on open list'}]), # noqa
    ({'message': "'not a date' does not match '^([\\\\+-]?\\\\d{4}(?!\\\\d{2}\\x08))((-?)((0[1-9]|1[0-2])(\\\\3([12]\\\\d|0[1-9]|3[01]))?|W([0-4]\\\\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\\\\d|[12]\\\\d{2}|3([0-5]\\\\d|6[1-6])))([T\\\\s]((([01]\\\\d|2[0-3])((:?)[0-5]\\\\d)?|24\\\\:?00)([\\\\.,]\\\\d+(?!:))?)?(\\\\17[0-5]\\\\d([\\\\.,]\\\\d+)?)?([zZ]|([\\\\+-])([01]\\\\d|2[0-3]):?([0-5]\\\\d)?)?)?)?$'", 'message_safe': '<code>birthDate</code> does not match the regex <code>^([\\+-]?\\d{4}(?!\\d{2}\x08))((-?)((0[1-9]|1[0-2])(\\3([12]\\d|0[1-9]|3[01]))?|W([0-4]\\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\\d|[12]\\d{2}|3([0-5]\\d|6[1-6])))([T\\s]((([01]\\d|2[0-3])((:?)[0-5]\\d)?|24\\:?00)([\\.,]\\d+(?!:))?)?(\\17[0-5]\\d([\\.,]\\d+)?)?([zZ]|([\\+-])([01]\\d|2[0-3]):?([0-5]\\d)?)?)?)?$</code>', 'message_type': 'pattern', 'path_no_number': 'birthDate'}, [{'path': '12/birthDate', 'value': 'not a date'}]), # noqa
    ({'message': "'personType' contains an unrecognised value. Check the related codelist for allowed code values.", 'message_safe': '<code>personType</code> contains an unrecognised value. Check the related codelist for allowed code values.', 'message_type': 'enum', 'path_no_number': 'personType'}, [{'path': '11/personType', 'value': 'bad person type'}]), # noqa
    ({'message': "'replacesStatements' should be a JSON array. Check that value(s) appear within square brackets, [...]", 'message_safe': '<code>replacesStatements</code> should be a JSON array. Check that value(s) appear within square brackets, [...]', 'message_type': 'array', 'path_no_number': 'replacesStatements'}, [{'path': '9/replacesStatements', 'value': 'not an array'}]), # noqa
    ({'message': "'statementID' is missing but required. Check that the field is included and correctly spelled.", 'message_safe': '<code>statementID</code> is missing but required. Check that the field is included and correctly spelled.', 'message_type': 'required', 'path_no_number': ''}, [{'path': '2'}, {'path': '7'}, {'path': '8'}, {'path': '9'}, {'path': '10'}]), # noqa
    ({'message': "'statementID' should be a string. Check that the value is not null, and has quotes at the start and end. Escape any quotes in the value with '\\'", 'message_safe': '<code>statementID</code> should be a string. Check that the value is not null, and has quotes at the start and end. Escape any quotes in the value with <code>\\</code>', 'message_type': 'string', 'path_no_number': 'statementID'}, [{'path': '4/statementID', 'value': 100}]), # noqa
    ({'message': "'statementType' contains an unrecognised value. Check the related codelist for allowed code values.", 'message_safe': '<code>statementType</code> contains an unrecognised value. Check the related codelist for allowed code values.', 'message_type': 'enum', 'path_no_number': 'statementType'}, [{'path': '1/statementType', 'value': 'bad statement type'}, {'path': '3/statementType'}]), # noqa
    ({'message': "'statementType' is missing but required. Check that the field is included and correctly spelled.", 'message_safe': '<code>statementType</code> is missing but required. Check that the field is included and correctly spelled.', 'message_type': 'required', 'path_no_number': ''}, [{'path': '0'}]), # noqa
    ({'message': "'subject' is missing but required. Check that the field is included and correctly spelled.", 'message_safe': '<code>subject</code> is missing but required. Check that the field is included and correctly spelled.', 'message_type': 'required', 'path_no_number': ''}, [{'path': '16'}, {'path': '17'}, {'path': '18'}, {'path': '19'}, {'path': '20'}]), # noqa
    ({'message': "'too long long long long long long long long long long long long long long long long' is too long", 'message_safe': '<code>replacesStatements/0</code> is too long. It should not exceed 64 characters.', 'message_type': 'maxLength', 'path_no_number': 'replacesStatements'}, [{'path': '8/replacesStatements/0', 'value': 'too long long long long long long long long long long long long long long long long'}]), # noqa
    ({'message': "'tooshort' is too short", 'message_safe': '<code>replacesStatements/0</code> is too short. It should be at least 32 characters.', 'message_type': 'minLength', 'path_no_number': 'replacesStatements'}, [{'path': '7/replacesStatements/0', 'value': 'tooshort'}]), # noqa
    ({'message': "'tooshort' is too short", 'message_safe': '<code>statementID</code> is too short. It should be at least 32 characters.', 'message_type': 'minLength', 'path_no_number': 'statementID'}, [{'path': '5/statementID', 'value': 'tooshort'}]), # noqa
    ({'message': '-1 is less than the minimum of 0', 'message_safe': '<code>minimum</code> is too small. The minimum allowed value is 0.', 'message_type': 'minimum', 'path_no_number': 'interests/share/minimum'}, [{'path': '16/interests/0/share/minimum', 'value': -1}]), # noqa
    ({'message': '101 is greater than the maximum of 100', 'message_safe': '<code>maximum</code> is too large. The maximum allowed value is 100.', 'message_type': 'maximum', 'path_no_number': 'interests/share/maximum'}, [{'path': '16/interests/0/share/maximum', 'value': 101}]), # noqa
    ({'message': 'Date is not in the correct format. The correct format is YYYY-MM-DD.', 'message_safe': 'Date is not in the correct format. The correct format is YYYY-MM-DD.', 'message_type': 'date', 'path_no_number': 'statementDate'}, [{'path': '10/statementDate', 'value': 'not a date'}]), # noqa
    ({'message': 'Date is not in the correct format. The correct format is YYYY-MM-DDThh:mm:ssZ.', 'message_safe': 'Date is not in the correct format. The correct format is YYYY-MM-DDT00:00:00Z.', 'message_type': 'date-time', 'path_no_number': 'source/retrievedAt'}, [{'path': '13/source/retrievedAt', 'value': 'not a date-time'}]), # noqa
    ({'message': 'Invalid uri found', 'message_safe': 'Invalid uri found', 'message_type': 'uri', 'path_no_number': 'uri'}, [{'path': '21/uri', 'value': 'not a uri'}]), # noqa
    ({'message': "{'motivation': 'not on open list'} is not valid under any of the given schemas", 'message_safe': '{&#39;motivation&#39;: &#39;not on open list&#39;} is not valid under any of the given schemas', 'message_type': 'anyOf', 'path_no_number': 'annotations'}, [{'path': '20/annotations/0'}]), # noqa
    ({'message': '{} is not valid under any of the given schemas', 'message_safe': '{} is not valid under any of the given schemas', 'message_type': 'anyOf', 'path_no_number': 'identifiers'}, [{'path': '15/identifiers/0'}]), # noqa
]


def unpack_validation_error(validation_error_result):
    validation_error, data = validation_error_result
    validation_error_data = json.loads(validation_error)
    return validation_error_data, data


def test_basic_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_1.json'
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
    assert results['statistics']['count_ownership_or_control_statement_current'] == 1
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename, lib_cove_bods_config=config)

    assert results['additional_checks_count'] == 1

    assert results['additional_checks'][0]['type'] == 'person_birth_year_too_late'
    assert results['additional_checks'][0]['person_statement'] == '019a93f1-e470-42e9-957b-03559861b2e2'
    assert results['additional_checks'][0]['year'] == 1964


def test_basic_2():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_2.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_extra_entity_statement_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_extra_person_statement_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_extra_ownership_or_control_statements_1.json'
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
    assert results['statistics']['count_ownership_or_control_statement_subject_by_year'] == {
        2017: 1,
        2018: 1
    }


def test_basic_missing_statement_ids():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_missing_statement_ids.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_statement_id_and_type_errors.json'
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

    validation_error_data, data = unpack_validation_error(results['validation_errors'][3])
    assert "'statementType' is missing but required" in validation_error_data['message']
    assert data[0]['path'] == '3'

    validation_error_data, data = unpack_validation_error(results['validation_errors'][2])
    assert "'statementType' contains an unrecognised value. Check the related codelist for allowed code values." in validation_error_data['message'] # noqa
    assert data[0]['path'] == '4/statementType'
    assert data[0]['value'] == 'test'

    assert results['additional_checks'][0]['type'] == 'person_statement_not_used_in_ownership_or_control_statement'
    assert results['additional_checks'][0]['person_statement'] == 'shortID'


def test_additional_fields_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_additional_fields_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_missing_entity_statement_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_missing_entity_statement_2.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_missing_person_statement_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_1_wrong_order_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_1_wrong_order_2.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_2_wrong_order_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_bad_identifier_scheme.json'
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


def test_badfile_all_validation_errors():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.1', 'badfile_all_validation_errors.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 39
    assert results['additional_fields_count'] == 1
    assert results['additional_checks_count'] == 11
    assert results['file_type'] == 'json'

    for (i, (expected_error, expected_values)) in enumerate(BADFILE_RESULTS):
        error, values = unpack_validation_error(results['validation_errors'][i])
        assert error['message'] == expected_error['message']
        assert error['message_safe'] == expected_error['message_safe']
        assert error['message_type'] == expected_error['message_type']
        assert error['path_no_number'] == expected_error['path_no_number']

        for j, value in enumerate(expected_values):
            assert value['path'] == expected_values[j]['path']


def test_basic_anonymous_person_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_anonymous_person_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_unknown_person_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_unknown_owner_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_duplicate_statement_id_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_entity_with_no_ids_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_entity_with_id_with_scheme_name_1.json'
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
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_replaces_statements.json'
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
    assert results['statistics']['count_ownership_or_control_statement_current'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 1
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
    assert results['statistics']['count_ownership_or_control_statement_subject_by_year'] == {
        2017: 1,
        2018: 1
    }
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person_by_year'] == {
        2018: 1
    }
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity_by_year'] == {
    }
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified_by_year'] == {
        2017: 1
    }


def test_bad_statement_date():
    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.1', 'bad_statement_date.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)
    assert results['statistics']['count_ownership_or_control_statement_by_year'] == {
        None: 1,
        2011: 1
    }
    assert results['statistics']['count_ownership_or_control_statement_subject_by_year'] == {
        None: 1,
        2011: 1
    }
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person_by_year'] == {
        None: 1,
        2011: 1
    }
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity_by_year'] == {
    }
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified_by_year'] == {
    }


@pytest.mark.parametrize(('filename', 'interests_shareholding', 'current_statements'), [
    ('basic_end_date.json', 1, 0),
    ('basic_end_date_2_interests.json', 2, 1),
])
def test_basic_end_date(filename, interests_shareholding, current_statements):
    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.1', filename
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
    assert results['statistics']['count_ownership_or_control_statement_current'] == current_statements
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_person'] == 1
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_entity'] == 0
    assert results['statistics']['count_ownership_or_control_statement_interested_party_with_unspecified'] == 0
    for k in results['statistics']['count_ownership_or_control_statement_interest_statement_types']:
        if k == 'shareholding':
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == interests_shareholding # noqa
        else:
            assert results['statistics']['count_ownership_or_control_statement_interest_statement_types'][k] == 0
    assert results['statistics']['count_replaces_statements_missing'] == 0
