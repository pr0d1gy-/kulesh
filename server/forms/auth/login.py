from wtforms import Form, PasswordField, StringField
from wtforms.validators import Email, Length, DataRequired


class LoginForm(Form):

    email = StringField('email', [
        DataRequired(),
        Email()
    ])

    password = PasswordField('password', [
        DataRequired(),
        Length(min=6, max=12)
    ])
