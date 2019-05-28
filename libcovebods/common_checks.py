import json

from libcove.lib.common import common_checks_context
from libcovebods.lib.common_checks import get_statistics, RunAdditionalChecks
from libcovebods.config import LibCoveBODSConfig


def common_checks_bods(context, upload_dir, json_data, schema_obj, lib_cove_bods_config=None):

    if not lib_cove_bods_config:
        lib_cove_bods_config = LibCoveBODSConfig()

    common_checks = common_checks_context(upload_dir, json_data, schema_obj, 'bods-schema.json', context)

    context.update(common_checks['context'])

    additional_checks = RunAdditionalChecks(json_data, lib_cove_bods_config).run()

    context.update({
        'statistics': get_statistics(json_data),
        'additional_checks': additional_checks,
        'additional_checks_count': len(additional_checks),
        'problems': additional_checks.copy(),
    })

    # Rewrite additional fields checks into this
    for data in context['data_only']:
        context['problems'].append({
            'type': 'additional_field',
            'place': data[0],
            'field': data[1],
            'count': data[2],
        })

    # Rewrite Validation errors into this
    for key, value_list in context['validation_errors']:
        key_data = json.loads(key)
        for value in value_list:
            context['problems'].append({
                'type': 'validate_' + key_data['message_type'],
                'path_no_number': key_data['path_no_number'],
                'value': value['value'],
                'path': value['path'],
            })
            
    return context
