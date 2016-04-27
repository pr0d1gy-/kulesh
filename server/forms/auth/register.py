from wtforms import Form, PasswordField, StringField
from wtforms.validators import Email, Length, DataRequired, EqualTo


class LoginForm(Form):

    email = StringField('email', [
        DataRequired(),
        Email()
    ])

    password = PasswordField('password', [
        DataRequired(),
        Length(min=6, max=12),
        EqualTo('password_confirm', message='Password do not match.')
    ])

    password_confirm = PasswordField('password', [
        DataRequired(),
        Length(min=6, max=12)
    ])
