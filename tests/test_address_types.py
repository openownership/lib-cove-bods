import tempfile
import os
from libcovebods.api import bods_json_output


def test_entity_address_wrong_type_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.2', 'entity_address_wrong_type_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['schema_version'] == '0.2'
    assert results['additional_checks_count'] == 1

    assert results['additional_checks'][0]['type'] == 'wrong_address_type_used'
    assert results['additional_checks'][0]['statement'] == '1dc0e987-5c57-4a1c-b3ad-61353b66a9b7'
    assert results['additional_checks'][0]['statement_type'] == 'entity'
    assert results['additional_checks'][0]['address_type'] == 'placeOfBirth'
