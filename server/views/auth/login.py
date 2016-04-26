from views.base_view import BaseMethodView

from flask import render_template, session, redirect, request, flash, \
    url_for

from forms.auth.login import LoginForm

from models.user import User


class LoginMethodView(BaseMethodView):
    """
    Authorization resource.
    """
    def get(self):
        return render_template('login.html')

    def post(self):
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        form = LoginForm(email=email, password=password)
        if not form.validate():
            if len(form.email.errors):
                flash('Email: %s' % '\n'.join(form.email.errors), 'error')
            if len(form.password.errors):
                flash('Password: %s' % '\n'.join(form.password.errors),
                      'error')

            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['id'] = user.id
        else:
            flash('User does not exist or the password is incorrect', 'error')

        return redirect(url_for('login'))

    def dispatch_request(self, *args, **kwargs):
        if 'id' in session:
            return redirect('/')

        return super(LoginMethodView, self).dispatch_request(*args, **kwargs)
