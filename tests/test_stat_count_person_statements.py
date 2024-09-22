import os
import tempfile

from tests.api import bods_json_output


def test_schema_0_2():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.2", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"

    assert results["statistics"]["count_person_statements"] == 1
    assert results["statistics"]["count_person_statements_types"]["knownPerson"] == 1


def test_schema_0_3_basic_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.3", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.3"

    assert results["statistics"]["count_person_statements"] == 1
    assert results["statistics"]["count_person_statements_types"]["knownPerson"] == 1


def test_schema_0_4_basic_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.4", "basic_1.json"
    )

    results = bods_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.4"

    assert results["statistics"]["count_person_statements"] == 1
    assert results["statistics"]["count_person_statements_types"]["knownPerson"] == 1
