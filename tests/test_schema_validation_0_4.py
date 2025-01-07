import csv
import os
import pathlib
import tempfile

import pytest

from tests.api import bods_json_output


@pytest.fixture
def expected_errors():
    expected = []
    with open(
        "tests/fixtures/0.4/invalid-schema/expected_errors.csv", newline=""
    ) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            expected.append(row)
    return expected


@pytest.fixture
def valid_statements():
    return pathlib.Path("tests/fixtures/0.4/valid-schema").glob("*.json")


def extract_elements(element_path):
    elems = [0 if elem == "$[0]" else elem for elem in element_path.split(".")]
    out = []
    for elem in elems:
        if isinstance(elem, str) and "[0]" in elem:
            out.append(elem.split("[0]")[0])
            out.append(0)
        else:
            out.append(elem)
    if len(out) == 1 and out[0] == "$":
        out = []
    return out


def test_all_schema_validation_invalid(expected_errors):

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )

    for expected in expected_errors:

        json_filename = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "0.4",
            "invalid-schema",
            expected[0],
        )

        results = bods_json_output(cove_temp_folder, json_filename)

        assert results["schema_version"] == "0.4"
        if expected[1] in ("enum", "type"):
            assert results["validation_errors_count"] > 0
        else:
            assert results["validation_errors_count"] == 1
        assert results["validation_errors"][0]["validator"] == expected[1]
        assert results["validation_errors"][0]["path"] == extract_elements(expected[2])
        if expected[1] == "required":
            assert (
                results["validation_errors"][0]["extra"][
                    "required_key_which_is_missing"
                ]
                == expected[3]
            )
        elif expected[1] in (
            "enum",
            "anyOf",
            "type",
            "maxLength",
            "minLength",
            "format",
            "minimum",
            "maximum",
            "pattern",
            "oneOf",
            "const",
        ):
            pass
        else:
            pass


def test_all_schema_validation_valid(valid_statements):

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-bods-tests-", dir=tempfile.gettempdir()
    )

    for valid_statement in valid_statements:

        results = bods_json_output(cove_temp_folder, valid_statement)

        assert results["schema_version"] == "0.4"
        assert results["validation_errors_count"] == 0
