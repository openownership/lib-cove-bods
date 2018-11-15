from libcove.lib.tools import get_file_type
from libcovebods.common_checks import common_checks_bods
from libcovebods.lib.api import context_api_transform
from libcovebods.config import LibCoveBODSConfig


class APIException(Exception):
    pass


def bods_json_output(output_dir, file, file_type=None, json_data=None,
                     lib_cove_bods_config=None):

    if not lib_cove_bods_config:
        lib_cove_bods_config = LibCoveBODSConfig()

    if not file_type:
        file_type = get_file_type(file)
    context = {"file_type": file_type}

    context = context_api_transform(
        common_checks_bods(context)
    )

    return context
