import json
from decimal import Decimal

from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft4Validator

import libcovebods.data_reader
from libcovebods.schema import SchemaBODS


class NumberStr(float):
    def __init__(self, o):
        # We don't call the parent here, since we're deliberately altering it's functionality
        # pylint: disable=W0231
        self.o = o

    def __repr__(self):
        return str(self.o)

    # This is needed for this trick to work in python 3.4
    def __float__(self):
        return self


def decimal_default(o):
    if isinstance(o, Decimal):
        if int(o) == o:
            return int(o)
        else:
            return NumberStr(o)
    raise TypeError(f"{repr(o)} is not JSON serializable")


def oneOf_draft4(validator, oneOf, instance, schema):
    """
    oneOf_draft4 validator from
    https://github.com/Julian/jsonschema/blob/d16713a4296663f3d62c50b9f9a2893cb380b7af/jsonschema/_validators.py#L337
    Modified to:
    - sort the instance JSON, so we get a reproducible output that we
      can can test more easily
    - If `statementType` is available, use that pick the correct
      sub-schema, and to yield those ValidationErrors. (Only
      applicable for BODS).
    """
    subschemas = enumerate(oneOf)
    all_errors = []
    validStatementTypes = []
    for index, subschema in subschemas:
        errs = list(validator.descend(instance, subschema, schema_path=index))
        if not errs:
            first_valid = subschema
            break
        properties = subschema.get("properties", {})
        if "statementType" in properties:
            if "statementType" in instance:
                try:
                    validStatementType = properties["statementType"].get("enum", [])[0]
                except IndexError:
                    continue
                if instance["statementType"] == validStatementType:
                    for err in errs:
                        yield err
                    return
                else:
                    validStatementTypes.append(validStatementType)
            else:
                yield ValidationError(
                    "statementType",
                    validator="required",
                )
                break
        all_errors.extend(errs)
    else:
        if validStatementTypes:
            yield ValidationError(
                "Invalid code found in statementType",
                instance=instance["statementType"],
                path=("statementType",),
                validator="enum",
            )
        else:
            yield ValidationError(
                "%s is not valid under any of the given schemas"
                % (json.dumps(instance, sort_keys=True, default=decimal_default),),
                context=all_errors,
            )

    more_valid = [s for i, s in subschemas if validator.is_valid(instance, s)]
    if more_valid:
        more_valid.append(first_valid)
        reprs = ", ".join(repr(schema) for schema in more_valid)
        yield ValidationError("%r is valid under each of %s" % (instance, reprs))


class JSONSchemaValidator:
    """Validates data using the JSON Schema method"""

    def __init__(self, schema: SchemaBODS):
        self._schema = schema

    def validate(self, data_reader: libcovebods.data_reader.DataReader) -> list:
        """Call with data. Results are returned."""
        validator = Draft4Validator(
            schema=self._schema._pkg_schema_obj, format_checker=FormatChecker()
        )
        validator.VALIDATORS["oneOf"] = oneOf_draft4
        output = []
        all_data = data_reader.get_all_data()
        for e in validator.iter_errors(all_data):
            output.append(BODSValidationError(e, all_data, self._schema))
        return output


class BODSValidationError:
    """Any problems found in data are returned as an instance of this class."""

    def __init__(
        self,
        json_schema_exceptions_validation_error: ValidationError,
        json_data: dict,
        schema: SchemaBODS,
    ):
        self._message = json_schema_exceptions_validation_error.message
        self._path = json_schema_exceptions_validation_error.path
        self._schema_path = json_schema_exceptions_validation_error.schema_path
        self._validator = json_schema_exceptions_validation_error.validator
        self._validator_value = json_schema_exceptions_validation_error.validator_value
        self._context = json_schema_exceptions_validation_error.context
        self._instance = json_schema_exceptions_validation_error.instance
        self._extra = {}

        if self._validator == "required":
            if "'" in self._message:
                self._extra["required_key_which_is_missing"] = self._message.split("'")[
                    1
                ]
            else:
                self._extra["required_key_which_is_missing"] = self._message

    def json(self):
        """Return representation of this error in JSON."""

        path_ending = self._path[-1]
        if isinstance(self._path[-1], int) and len(self._path) >= 2:
            # We're dealing with elements in an array of items at this point
            path_ending = "{}/[number]".format(self._path[-2])
        elif isinstance(self._path[0], int) and len(self._path) == 1:
            path_ending = "[number]"

        return {
            "message": self._message,
            "path": list(self._path),
            "path_ending": path_ending,
            "schema_path": list(self._schema_path),
            "validator": self._validator,
            "validator_value": self._validator_value,
            # "context": self._context,
            "instance": self._instance,
            "extra": self._extra,
        }
