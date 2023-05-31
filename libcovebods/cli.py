import argparse
import json

import libcovebods.additionalfields
import libcovebods.config
import libcovebods.data_reader
import libcovebods.jsonschemavalidate
import libcovebods.run_tasks
import libcovebods.schema


def main():
    parser = argparse.ArgumentParser(description="Lib Cove BODS CLI")
    subparsers = parser.add_subparsers(dest="subparser_name")

    python_validate_parser = subparsers.add_parser(
        "pythonvalidate",
        aliases=["pv"],
        help="Check that data conforms to normative rules specified in BODS",
    )
    python_validate_parser.add_argument(
        "inputfilename", help="File name of an input JSON data file"
    )

    additional_fields_parser = subparsers.add_parser(
        "additionalfields",
        aliases=["af"],
        help="Report additional fields not specified in the schema",
    )
    additional_fields_parser.add_argument(
        "inputfilename", help="File name of an input JSON data file"
    )

    json_schema_validate_parser = subparsers.add_parser(
        "jsonschemavalidate", aliases=["jsv"], help="Validate data against the schema"
    )
    json_schema_validate_parser.add_argument(
        "inputfilename", help="File name of an input JSON data file"
    )

    args = parser.parse_args()

    if args.subparser_name == "pythonvalidate" or args.subparser_name == "pv":

        data_reader = libcovebods.data_reader.DataReader(args.inputfilename)
        config = libcovebods.config.LibCoveBODSConfig()
        schema = libcovebods.schema.SchemaBODS(data_reader, config)
        output_data = libcovebods.run_tasks.process_additional_checks(
            data_reader, config, schema, libcovebods.run_tasks.TASK_CLASSES
        )

        print(json.dumps(output_data, indent=4))

    elif args.subparser_name == "additionalfields" or args.subparser_name == "af":

        data_reader = libcovebods.data_reader.DataReader(args.inputfilename)
        config = libcovebods.config.LibCoveBODSConfig()
        schema = libcovebods.schema.SchemaBODS(data_reader, config)
        validator = libcovebods.additionalfields.AdditionalFields(schema)

        output = validator.process(data_reader)

        print(json.dumps(output, indent=4))

    elif args.subparser_name == "jsonschemavalidate" or args.subparser_name == "jsv":

        data_reader = libcovebods.data_reader.DataReader(args.inputfilename)
        config = libcovebods.config.LibCoveBODSConfig()
        schema = libcovebods.schema.SchemaBODS(data_reader, config)
        validator = libcovebods.jsonschemavalidate.JSONSchemaValidator(schema)

        output = validator.validate(data_reader)

        output_json = [o.json() for o in output]

        print(json.dumps(output_json, indent=4))


if __name__ == "__main__":
    main()
