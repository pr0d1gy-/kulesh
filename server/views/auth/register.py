from views.base_view import BaseMethodView

from flask import render_template, redirect, url_for, flash

from forms.auth.register import RegisterForm

from models import db
from models.user import User

from sqlalchemy.exc import IntegrityError

from utils.forms import request_fields_to_kwargs


class RegisterMethodView(BaseMethodView):

    def get(self):
        return render_template('register.html', form=RegisterForm)

    def post(self):
        form = RegisterForm(**request_fields_to_kwargs(fields=[
            'username', 'email', 'password', 'password_confirm']))

        if not form.validate():
            return render_template('register.html', form=form)

        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            form.email.errors.append('This email is already in use.')

            return render_template('register.html', form=form)

        flash('Registration successful.', 'success')

        return redirect(url_for('login'))
