import tempfile
import os
from libcovebods.api import bods_json_output


def test_basic_1():

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-tests-', dir=tempfile.gettempdir())
    json_filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'fixtures', 'api', 'basic_1.json'
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results['file_type'] == 'json'
