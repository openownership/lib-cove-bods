import json
from libcove.lib.tools import get_file_type
from libcovebods.common_checks import common_checks_bods
from libcovebods.lib.api import context_api_transform
from libcovebods.config import LibCoveBODSConfig
from libcovebods.schema import SchemaBODS


class APIException(Exception):
    pass


def bods_json_output(output_dir, file, file_type=None, json_data=None,
                     lib_cove_bods_config=None):

    if not lib_cove_bods_config:
        lib_cove_bods_config = LibCoveBODSConfig()

    if not file_type:
        file_type = get_file_type(file)
    context = {"file_type": file_type}

    if file_type == 'json':
        if not json_data:
            with open(file, encoding='utf-8') as fp:
                try:
                    json_data = json.load(fp)
                except ValueError:
                    raise APIException('The file looks like invalid json')

        schema_bods = SchemaBODS(json_data=json_data, lib_cove_bods_config=lib_cove_bods_config)

    else:

        raise Exception("JSON only for now, sorry!")

    context['schema_version'] = schema_bods.schema_version

    context = context_api_transform(
        common_checks_bods(context, output_dir, json_data, schema_bods, lib_cove_bods_config=lib_cove_bods_config)
    )

    return context
