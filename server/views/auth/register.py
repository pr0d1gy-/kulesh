from views.base_view import BaseMethodView

from flask import render_template
from werkzeug.exceptions import NotImplemented


class RegisterMethodView(BaseMethodView):

    def get(self):
        return render_template('register.html')

    def post(self):
        raise NotImplemented
