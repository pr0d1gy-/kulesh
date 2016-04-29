from views.base_view import BaseMethodView

from flask import render_template, session, redirect, flash

from forms.auth.login import LoginForm

from models.user import User

from utils.forms import request_fields_to_kwargs


class LoginMethodView(BaseMethodView):
    """
    Authorization resource.
    """
    def get(self):
        return render_template('login.html', form=LoginForm)

    def post(self):
        form = LoginForm(**request_fields_to_kwargs(['email', 'password']))

        if not form.validate():
            return render_template('login.html', form=form)

        user = User.query.filter_by(email=form.email.data).limit(1).first()
        if user and user.check_password(form.password.data):
            session['id'] = user.id
            flash('Login successful.', 'success')

            return redirect('/')

        else:
            form.email.errors.append('User does not exist or '
                                     'the password is incorrect')

        return render_template('login.html', form=form)

    def dispatch_request(self, *args, **kwargs):
        if 'id' in session:
            return redirect('/')

        return super(LoginMethodView, self).dispatch_request(*args, **kwargs)
