from flask import session, redirect


def logout():
    if 'id' in session and \
            session['id']:
        session.clear()
    
    return redirect('/login')
