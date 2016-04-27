import settings

from flask import session, redirect, jsonify, url_for

from werkzeug.security import gen_salt

from models.client import Client

from utils import current_user

from models import db


def client():
    user = current_user()
    if not user:
        # session['id'] = 1  # temporary decision
        return redirect(url_for('register'))

    item = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=' '.join([
            '%s/%s' % (settings.BASE_URL, 'authorized'),
            'http://localhost:8000/authorized',
            'http://127.0.0.1:8000/authorized',
            'http://127.0.1:8000/authorized',
            'http://127.1:8000/authorized',
            ]),
        _default_scopes='email',
        user_id=session['id'],
    )

    db.session.add(item)
    db.session.commit()

    return jsonify(
        client_id=item.client_id,
        client_secret=item.client_secret,
    )
