import tempfile
import os
from libcovebods.api import bods_json_output


def test_0_1_then_0_2():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'mixed', '0.1_then_0.2.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['schema_version'] == '0.1'
    assert results['additional_checks_count'] == 1

    assert results['additional_checks'][0]['type'] == 'inconsistent_schema_version_used'
    assert results['additional_checks'][0]['statement'] == '019a93f1-e470-42e9-957b-03559861b2e2'
    assert results['additional_checks'][0]['statement_type'] == 'person'
    assert results['additional_checks'][0]['schema_version'] == '0.2'


def test_0_2_then_0_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'mixed', '0.2_then_0.1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['schema_version'] == '0.2'
    assert results['additional_checks_count'] == 1

    assert results['additional_checks'][0]['type'] == 'inconsistent_schema_version_used'
    assert results['additional_checks'][0]['statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c'
    assert results['additional_checks'][0]['statement_type'] == 'ownership_or_control'
    assert results['additional_checks'][0]['schema_version'] == '0.1'


def test_0_2_then_dict():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'mixed', '0.2_then_dict.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['schema_version'] == '0.2'
    assert results['additional_checks_count'] == 1

    assert results['additional_checks'][0]['type'] == 'inconsistent_schema_version_used'
    assert results['additional_checks'][0]['statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c'
    assert results['additional_checks'][0]['statement_type'] == 'ownership_or_control'
    assert results['additional_checks'][0]['schema_version'] == '{}'


def test_dict_then_0_2():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'mixed', 'dict_then_0.2.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['schema_version'] == '0.2'

    assert results['additional_checks_count'] == 2

    assert results['additional_checks'][0]['type'] == 'unknown_schema_version_used'
    assert results['additional_checks'][0]['schema_version'] == '{}'

    assert results['additional_checks'][1]['type'] == 'inconsistent_schema_version_used'
    assert results['additional_checks'][1]['statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c'
    assert results['additional_checks'][1]['statement_type'] == 'ownership_or_control'
    assert results['additional_checks'][1]['schema_version'] == '0.2'
