import json
from wtforms.validators import StopValidation


class JsonValidator(object):

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        value = field.data

        if not value:
            return None

        try:
            value = json.loads(value)
        except ValueError:
            message = field.ngettext('Must be a valid json.',
                                     'Must be a valid json.')

            raise StopValidation(message)
