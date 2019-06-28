import tempfile
import os
from libcovebods.api import bods_json_output


def test_schema_0_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.1', 'basic_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['schema_version'] == '0.1'

    # Schema v0.1 and Schema v0.2 have different enum options, make sure that is reflected in data
    keys = results['statistics']['count_ownership_or_control_statement_interest_statement_types'].keys()
    assert 12 == len(keys)

    # We want to test the dict has the correct keys!
    # So these tests are deliberately written so they will error if the specified key is not in that dict
    assert 1 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['shareholding']
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['voting-rights']
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['appointment-of-board']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['influence-or-control']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['senior-managing-official']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['settlor-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['trustee-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['protector-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['beneficiary-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['other-influence-or-control-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['rights-to-surplus-assets']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['rights-to-profit-or-income']  # noqa


def test_schema_0_2():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', '0.2', 'basic_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['schema_version'] == '0.2'

    # Schema v0.1 and Schema v0.2 have different enum options, make sure that is reflected in data
    keys = results['statistics']['count_ownership_or_control_statement_interest_statement_types'].keys()
    assert 14 == len(keys)

    # We want to test the dict has the correct keys!
    # So these tests are deliberately written so they will error if the specified key is not in that dict
    assert 1 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['shareholding']
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['voting-rights']
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['appointment-of-board']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['other-influence-or-control']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['senior-managing-official']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['settlor-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['trustee-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['protector-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['beneficiary-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['other-influence-or-control-of-trust']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['rights-to-surplus-assets-on-dissolution']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['rights-to-profit-or-income']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['rights-granted-by-contract']  # noqa
    assert 0 == results['statistics']['count_ownership_or_control_statement_interest_statement_types']['conditional-rights-granted-by-contract']  # noqa
