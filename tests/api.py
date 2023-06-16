import libcovebods.additionalfields
import libcovebods.config
import libcovebods.data_reader
import libcovebods.jsonschemavalidate
import libcovebods.run_tasks
import libcovebods.schema


def bods_json_output(
    temp_folder,
    input_file_name,
    file_type=None,
    json_data=None,
    lib_cove_bods_config=None,
):
    # Data Reader
    data_reader = libcovebods.data_reader.DataReader(input_file_name)

    # classes
    if not lib_cove_bods_config:
        lib_cove_bods_config = libcovebods.config.LibCoveBODSConfig()
    schema = libcovebods.schema.SchemaBODS(data_reader, lib_cove_bods_config)

    # Additional checks and stats
    output_data = libcovebods.run_tasks.process_additional_checks(
        data_reader, lib_cove_bods_config, schema
    )

    # Additional fields
    additionalfields_validator = libcovebods.additionalfields.AdditionalFields(schema)
    additionalfields_output = additionalfields_validator.process(data_reader)

    # JSON Schema
    jsonschemavalidate_validator = libcovebods.jsonschemavalidate.JSONSchemaValidator(
        schema
    )
    jsonschemavalidate_output = jsonschemavalidate_validator.validate(data_reader)

    # Put it all together ...
    return {
        "schema_version": schema.schema_version,
        "additional_checks": output_data["additional_checks"],
        "additional_checks_count": len(output_data["additional_checks"]),
        "statistics": output_data["statistics"],
        "validation_errors_count": len(jsonschemavalidate_output),
        "validation_errors": [o.json() for o in jsonschemavalidate_output],
        "additional_fields_count": len(additionalfields_output),
        "additional_fields": additionalfields_output,
        "file_type": "json",
    }
