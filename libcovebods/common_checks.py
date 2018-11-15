from libcove.lib.common import common_checks_context


def common_checks_bods(context, upload_dir, json_data, schema_obj):

    common_checks = common_checks_context(upload_dir, json_data, schema_obj, 'bods-schema.json', context)

    context.update(common_checks['context'])

    return context
