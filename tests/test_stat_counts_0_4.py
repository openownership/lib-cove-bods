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
        "sample_300_statements.json",
    )

    results = bods_json_output(cove_temp_folder, json_filename, sample_mode=True)

    assert results["schema_version"] == "0.4"

    assert results["statistics"]["count_entity_statements"] == 50
    assert (
        results["statistics"]["count_entity_statements_types"]["registeredEntity"] == 50
    )
    assert (
        results["statistics"]["count_entity_statements_types_with_any_identifier"][
            "registeredEntity"
        ]
        == 50
    )
    assert (
        results["statistics"][
            "count_entity_statements_types_with_any_identifier_with_id_and_scheme"
        ]["registeredEntity"]
        == 50
    )
    assert results["statistics"]["count_person_statements"] == 50
    assert results["statistics"]["count_person_statements_types"]["knownPerson"] == 50
    assert results["statistics"]["count_ownership_or_control_statement"] == 50
    assert (
        results["statistics"][
            "count_ownership_or_control_statement_interested_party_with_person"
        ]
        == 50
    )
    assert (
        results["statistics"][
            "count_ownership_or_control_statement_interested_party_with_entity"
        ]
        == 0
    )
    assert (
        results["statistics"][
            "count_ownership_or_control_statement_interested_party_with_unspecified"
        ]
        == 0
    )
    assert (
        results["statistics"]["count_ownership_or_control_statement_interested_party"]
        == 50
    )
    assert (
        results["statistics"][
            "count_ownership_or_control_statement_interest_statement_types"
        ]["shareholding"]
        == 50
    )
    assert (
        results["statistics"]["count_ownership_or_control_statement_by_year"][2020]
        == 50
    )
    assert (
        results["statistics"]["count_ownership_or_control_statement_subject_by_year"][
            2020
        ]
        == 50
    )
    assert (
        results["statistics"][
            "count_ownership_or_control_statement_interested_party_by_year"
        ][2020]
        == 50
    )
