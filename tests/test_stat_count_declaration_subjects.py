import os
import tempfile

from tests.api import bods_json_output


def test_schema_0_4_count():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "statistic_count_declaration_subjects.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"

    assert results["statistics"]["count_declaration_subjects"] == 2
