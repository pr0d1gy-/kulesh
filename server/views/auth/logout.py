from flask import session, redirect, url_for


def logout():
    if 'id' in session and \
            session['id']:
        session.clear()

    return redirect(url_for('login'))
