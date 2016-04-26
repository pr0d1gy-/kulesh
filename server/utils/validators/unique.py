from wtforms.validators import StopValidation


class UniqueValidator(object):

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        value = field.data

        assert value, '`%s` must be not empty.'

        obj = self.model.query.filter_by(**{self.field: value}).first()
        if obj:
            message = field.ngettext('`%s` must be unique.',
                                     '`%s` must be unique.',
                                     self.field)

            raise StopValidation(message)
