from wtforms import Form, StringField
from wtforms.validators import Length, DataRequired

from utils.validators.json import JsonValidator
from utils.validators.unique import UniqueValidator

from models.function import Function


class TaskForm(Form):

    name = StringField('name', [
        DataRequired(),
        Length(min=1, max=50),
        UniqueValidator(model=Function, field='name')
    ])

    code = StringField('code', [
        DataRequired()
    ])

    data_field = StringField('data', [
        JsonValidator()
    ])
