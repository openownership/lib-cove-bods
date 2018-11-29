from libcove.lib.common import common_checks_context
from libcovebods.lib.common_checks import get_statistics, RunAdditionalChecks


def common_checks_bods(context, upload_dir, json_data, schema_obj):

    common_checks = common_checks_context(upload_dir, json_data, schema_obj, 'bods-schema.json', context)

    context.update(common_checks['context'])

    additional_checks = RunAdditionalChecks(json_data).run()

    context.update({
        'statistics': get_statistics(json_data),
        'additional_checks': additional_checks,
        'additional_checks_count': len(additional_checks),
    })

    return context
