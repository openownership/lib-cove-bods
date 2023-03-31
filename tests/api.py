import libcovebods.config
import libcovebods.schema
import libcovebods.lib.common_checks
import libcovebods.additionalfields
import libcovebods.jsonschemavalidate
import json


def bods_json_output(temp_folder, input_file_name, file_type=None, json_data=None, lib_cove_bods_config=None ):
    # Data
    with open(input_file_name) as fp:
        input_data = json.load(fp)

    # classes
    if not lib_cove_bods_config:
        lib_cove_bods_config = libcovebods.config.LibCoveBODSConfig()
    schema = libcovebods.schema.SchemaBODS(input_data, lib_cove_bods_config)

    # Additional checks and stats
    output_data = libcovebods.lib.common_checks.process_additional_checks(input_data, lib_cove_bods_config, schema)

    # Additional fields
    additionalfields_validator = libcovebods.additionalfields.AdditionalFields(schema)
    additionalfields_output = additionalfields_validator.process(input_data)

    # JSON Schema
    jsonschemavalidate_validator = libcovebods.jsonschemavalidate.JSONSchemaValidator(schema)
    jsonschemavalidate_output = jsonschemavalidate_validator.validate(input_data)

    # Put it all together ...
    return {
        "schema_version": schema.schema_version,
        "additional_checks": output_data['additional_checks'],
        "additional_checks_count": len(output_data['additional_checks']),
        "statistics": output_data['statistics'],
        "validation_errors_count": len(jsonschemavalidate_output),
        "validation_errors": [o.json() for o in jsonschemavalidate_output],
        "additional_fields_count": len(additionalfields_output),
        "additional_fields": len(additionalfields_output),
        "file_type": "json",
    }
