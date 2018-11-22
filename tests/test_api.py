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
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1


def test_basic_extra_entity_statement_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_extra_entity_statement_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 2
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1


def test_basic_extra_person_statement_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_extra_person_statement_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 2
    assert results['statistics']['count_ownership_or_control_statement'] == 1


def test_basic_extra_ownership_or_control_statement_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_extra_ownership_or_control_statement_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 0
    assert results['file_type'] == 'json'
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 2


def test_basic_missing_statement_ids():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_missing_statement_ids.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['file_type'] == 'json'
    assert results['validation_errors_count'] == 3
    assert results['additional_fields_count'] == 0
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1

    for validation_error, data in results['validation_errors']:
        validation_error_data = json.loads(validation_error)
        assert 'is not valid under any of the given schemas' in validation_error_data['message']


def test_additional_fields_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_additional_fields_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['validation_errors_count'] == 0
    assert results['additional_fields_count'] == 2
    assert results['file_type'] == 'json'
    assert results['data_only'] == [('', 'cats', 1), ('', 'dogs', 1)]
    assert results['statistics']['count_entity_statements'] == 1
    assert results['statistics']['count_person_statements'] == 1
    assert results['statistics']['count_ownership_or_control_statement'] == 1
