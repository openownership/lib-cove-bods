import json
from collections import OrderedDict
from libcove.lib.common import common_checks_context
from libcovebods.lib.common_checks import GetStatistics, RunAdditionalChecks
from django.utils.html import format_html
from libcovebods.config import LibCoveBODSConfig

from cove.html_error_msg import html_error_msg


validation_error_template_lookup = {
    'date': 'Date is not in the correct format. The correct format is YYYY-MM-DD.',
    'date-time': 'Date is not in the correct format. The correct format is YYYY-MM-DDThh:mm:ssZ.',
    'uri': 'Invalid uri found',
    'string': '\'{}\' should be a string. Check that the value {} has quotes at the start and end. Escape any quotes in the value with \'\\\'', # noqa
    'integer': '\'{}\' should be an integer. Check that the value {} doesn’t contain decimal points or any characters other than 0-9. Integer values should not be in quotes. ', # noqa
    'number': '\'{}\' should be a number. Check that the value {} doesn’t contain any characters other than 0-9 and dot (\'.\'). Number values should not be in quotes. ', # noqa
    'boolean': '\'{}\' should be a JSON boolean, \'true\' or \'false\'.', # noqa
    'object': '\'{}\' should be a JSON object',
    'array': '\'{}\' should be a JSON array. Check that value(s) appear within square brackets, [...]'}
# These are "safe" html that we trust
# Don't insert any values into these strings without ensuring escaping
# e.g. using django's format_html function.
validation_error_template_lookup_safe = {
    'date': 'Date is not in the correct format. The correct format is YYYY-MM-DD.',
    'date-time': 'Date is not in the correct format. The correct format is YYYY-MM-DDT00:00:00Z.',
    'uri': 'Invalid uri found',
    'string': '<code>{}</code> should be a string. Check that the value {} has quotes at the start and end. Escape any quotes in the value with <code>\</code>', # noqa
    'integer': '<code>{}</code> should be an integer. Check that the value {} doesn’t contain decimal points or any characters other than 0-9. Integer values should not be in quotes. ', # noqa
    'number': '<code>{}</code> should be a number. Check that the value {} doesn’t contain any characters other than 0-9 and dot (<code>.</code>). Number values should not be in quotes. ', # noqa
    'boolean': '<code>{}</code> should be a JSON boolean, <code>true</code> or <code>false</code>.', # noqa
    'object': '<code>{}</code> should be a JSON object',
    'array': '<code>{}</code> should be a JSON array. Check that value(s) appear within square brackets, [...]'}


def common_checks_bods(context, upload_dir, json_data, schema_obj, lib_cove_bods_config=None):

    if not lib_cove_bods_config:
        lib_cove_bods_config = LibCoveBODSConfig()

    common_checks = common_checks_context(upload_dir, json_data, schema_obj, 'bods-schema.json', context)

    # Rewrite validation errors
    # We do something similar for OCDS
    # https://github.com/open-contracting/lib-cove-ocds/blob/74c459c06136af45db76487f39408664fd2d4854/libcoveocds/common_checks.py#L32
    validation_errors = common_checks['context']['validation_errors']
    new_validation_errors = []
    for (json_key, values) in validation_errors:
        error = json.loads(json_key, object_pairs_hook=OrderedDict)

        assert 'message_safe' not in error
        error['message_safe'] = html_error_msg(error)

        e_validator = error['validator']
        e_validator_value = error['validator_value']
        validator_type = error['message_type']
        null_clause = error['null_clause']
        header = error['header_extra']

        message = None
        message_safe = None

        if e_validator in ('format', 'type'):
            message_template = validation_error_template_lookup.get(validator_type)
            message_safe_template = validation_error_template_lookup_safe.get(validator_type)

            if message_template:
                message = message_template.format(header, null_clause)
            if message_safe_template:
                message_safe = format_html(message_safe_template, header, null_clause)

        if e_validator == 'required':
            extra_message = ". Check that the field is included and correctly spelled."
            error['message'] += extra_message
            error['message_safe'] += extra_message

        if e_validator == 'enum':
            message = "'{}' contains an unrecognised value. Check the related codelist for allowed code values.".format(header) # noqa
            message_safe = format_html("<code>{}</code> contains an unrecognised value. Check the related codelist for allowed code values.", header) # noqa

        if e_validator == 'minItems' and e_validator_value == 1:
            message_safe = format_html('<code>{}</code> is too short. You must supply at least one value, or remove the item entirely (unless it’s required).', header) # noqa

        if e_validator == 'minLength':
            if e_validator_value == 1:
                message_safe = format_html('<code>"{}"</code> is too short. Strings must be at least one character. This error typically indicates a missing value.', header) # noqa
            else:
                message_safe = format_html('<code>{}</code> is too short. It should be at least {} characters.', header, e_validator_value) # noqa 

        if e_validator == 'maxLength':
            message_safe = format_html('<code>{}</code> is too long. It should not exceed {} characters.', header, e_validator_value) # noqa

        if e_validator == 'minimum':
            message_safe = format_html('<code>{}</code> is too small. The minimum allowed value is {}.', header, e_validator_value) # noqa

        if e_validator == 'maximum':
            message_safe = format_html('<code>{}</code> is too large. The maximum allowed value is {}.', header, e_validator_value) # noqa

        if message is not None:
            error['message'] = message
        if message_safe is not None:
            error['message_safe'] = message_safe

        new_validation_errors.append([json.dumps(error), values])
    try:
        new_validation_errors.sort()
    except TypeError:
        pass
    common_checks['context']['validation_errors'] = new_validation_errors

    context.update(common_checks['context'])

    additional_checks = RunAdditionalChecks(json_data, lib_cove_bods_config, schema_obj).run()
    get_statistics = GetStatistics(json_data, lib_cove_bods_config, schema_obj).run()

    context.update({
        'statistics': get_statistics,
        'additional_checks': additional_checks,
        'additional_checks_count': len(additional_checks),
    })

    return context
