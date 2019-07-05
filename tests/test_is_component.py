import tempfile
import os
from libcovebods.api import bods_json_output


def test_iscomponent_true_but_has_component_statement_ids_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.2', 'iscomponent_true_but_has_component_statement_ids_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['schema_version'] == '0.2'
    assert results['additional_checks_count'] == 1

    assert results['additional_checks'][0]['type'] == 'ownership_or_control_statement_has_is_compontent_and_component_statement_ids'  # noqa
    assert results['additional_checks'][0]['statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c'


def test_component_statement_ids_not_in_package_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.2', 'component_statement_ids_not_in_package_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['schema_version'] == '0.2'
    assert results['additional_checks_count'] == 1

    assert results['additional_checks'][0]['type'] == 'component_statement_id_not_in_package'
    assert results['additional_checks'][0]['seen_in_ownership_or_control_statement'] == 'fbfd0547-d0c6-4a00-b559-5c5e91c34f5c'  # noqa
    assert results['additional_checks'][0]['component_statement_id'] == '000a00a0-a000-00a0-000a-00000000a0a0'
