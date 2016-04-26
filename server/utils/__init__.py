from flask import session
from models.user import User


def current_user():
    if 'id' in session:
        uid = session['id']

        return User.query.get(uid)

    return None
