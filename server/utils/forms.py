from flask import flash, request


def flash_form_errors(form, fields):
    for field in fields:
        field_errors = getattr(form, field).errors
        if field_errors:
            field_name = field.split('_')
            for i, name in enumerate(field_name):
                field_name[i] = name[0].upper() + name[1:].lower()
            field = ' '.join(field_name)

            flash('%s: %s' % (field, '\n'.join(field_errors)), 'error')


def request_fields_to_kwargs(fields):
    return {field: request.form.get(field, '').strip() for field in fields}
