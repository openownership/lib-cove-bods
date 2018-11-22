from libcove.lib.common import common_checks_context
from libcovebods.lib.common_checks import get_statistics


def common_checks_bods(context, upload_dir, json_data, schema_obj):

    common_checks = common_checks_context(upload_dir, json_data, schema_obj, 'bods-schema.json', context)

    context.update(common_checks['context'])

    context.update({
      'statistics': get_statistics(json_data)
    })

    return context
