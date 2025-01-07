import os
import tempfile

from tests.api import bods_json_output


def test_sample_mode_valid_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "valid-schema",
        "person_politicalExposure_object.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"

    assert results["statistics"]["count_person_statements_have_pep_status"] == 1
    assert (
        results["statistics"]["count_person_statements_have_pep_status_statuses"][
            "isPep"
        ]
        == 1
    )
