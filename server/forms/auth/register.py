from wtforms import Form, PasswordField, StringField
from wtforms.validators import Email, Length, DataRequired, EqualTo

from utils.validators.unique import UniqueValidator

from models.user import User


class RegisterForm(Form):

    username = StringField('username', [
        DataRequired(),
        Length(min=2, max=50)
    ])

    email = StringField('email', [
        DataRequired(),
        Email(),
        UniqueValidator(
            model=User,
            field='email',
            message='Email must be unique.'
        )
    ])

    password = PasswordField('password', [
        DataRequired(),
        Length(min=6, max=12),
        EqualTo('password_confirm', message='Password do not match.')
    ])

    password_confirm = PasswordField('password_confirm')
