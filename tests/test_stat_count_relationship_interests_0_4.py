import os
import tempfile

from tests.api import bods_json_output


def test_stat_count_relationship_interests_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.4",
        "basic_1.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"

    assert (
        results["statistics"][
            "count_ownership_or_control_statement_with_at_least_one_interest_beneficial"
        ]
        == 1
    )
