from views.base_view import BaseMethodView

from flask import render_template, redirect, url_for, flash, request

from forms.auth.register import RegisterForm

from models import db
from models.user import User

from sqlalchemy.exc import IntegrityError


class RegisterMethodView(BaseMethodView):

    def get(self):
        return render_template('register.html', form=RegisterForm)

    def post(self):
        fields = ['username', 'email', 'password', 'password_confirm']

        form = RegisterForm(**{field: request.form.get(field, '').strip()
                               for field in fields})

        if not form.validate():
            for field in fields:
                field_errors = getattr(form, field).errors
                if field_errors:
                    field_name = field.split('_')
                    for i, name in enumerate(field_name):
                        field_name[i] = name[0].upper() + name[1:].lower()
                    field = ' '.join(field_name)

                    flash('%s: %s' % (field, '\n'.join(field_errors)), 'error')

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
