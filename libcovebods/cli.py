import argparse
import json

import libcovebods.additionalfields
import libcovebods.config
import libcovebods.jsonschemavalidate
import libcovebods.lib.common_checks
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

    statistics_parser = subparsers.add_parser(
        "statistics",
        aliases=["s"],
        help="",
    )
    statistics_parser.add_argument(
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

        with open(args.inputfilename) as fp:
            input_data = json.load(fp)

        config = libcovebods.config.LibCoveBODSConfig()
        schema = libcovebods.schema.SchemaBODS(input_data, config)
        output_data = libcovebods.lib.common_checks.process_additional_checks(
            input_data, config, schema
        )

        print(json.dumps(output_data["additional_checks"], indent=4))

    elif args.subparser_name == "statistics" or args.subparser_name == "s":

        with open(args.inputfilename) as fp:
            input_data = json.load(fp)

        config = libcovebods.config.LibCoveBODSConfig()
        schema = libcovebods.schema.SchemaBODS(input_data, config)
        output_data = libcovebods.lib.common_checks.process_additional_checks(
            input_data, config, schema
        )

        print(json.dumps(output_data["statistics"], indent=4))

    elif args.subparser_name == "additionalfields" or args.subparser_name == "af":

        with open(args.inputfilename) as fp:
            input_data = json.load(fp)

        config = libcovebods.config.LibCoveBODSConfig()
        schema = libcovebods.schema.SchemaBODS(input_data, config)
        validator = libcovebods.additionalfields.AdditionalFields(schema)

        output = validator.process(input_data)

        print(json.dumps(output, indent=4))

    elif args.subparser_name == "jsonschemavalidate" or args.subparser_name == "jsv":

        with open(args.inputfilename) as fp:
            input_data = json.load(fp)

        config = libcovebods.config.LibCoveBODSConfig()
        schema = libcovebods.schema.SchemaBODS(input_data, config)
        validator = libcovebods.jsonschemavalidate.JSONSchemaValidator(schema)

        output = validator.validate(input_data)

        output_json = [o.json() for o in output]

        print(json.dumps(output_json, indent=4))


if __name__ == "__main__":
    main()
