from flask import Flask, render_template, url_for, redirect, \
    session, request, jsonify
from flask_oauthlib.client import OAuth

from settings import CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN_URL, \
    AUTHORIZE_URL, BASE_API_URL


app = Flask(__name__)
app.debug = True
app.secret_key = 'c0derunner'
oauth = OAuth(app)


remote = oauth.remote_app(
    'remote',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url=BASE_API_URL,
    request_token_url=None,
    access_token_url=ACCESS_TOKEN_URL,
    authorize_url=AUTHORIZE_URL,
)


@app.route('/me')
def user_get():
    if 'remote_oauth' in session:
        resp = remote.get('me')
        try:
            return jsonify(resp.data)
        except TypeError:
            return resp.data

    return redirect(url_for('index'))


@app.route('/authorized')
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args.get('error_reason', None),
            request.args.get('error_description', None)
        )

    session['remote_oauth'] = (resp['access_token'], '')
    return redirect(url_for('index'))


@remote.tokengetter
def get_oauth_token():
    return session.get('remote_oauth')


# Flask application part


@app.route('/')
def index():
    if 'remote_oauth' in session:
        oauth_token = session['remote_oauth']
        return render_template('index.html', access_token=oauth_token)

    next_url = None  # request.args.get('next') or request.referrer or None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@app.route('/create_task')
def create_task():
    if 'remote_oauth' in session:
        oauth_token = session['remote_oauth']
        return render_template('create_task.html', access_token=oauth_token)

    next_url = None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@app.route('/task_table')
def get_table_task():
    if 'remote_oauth' in session:
        oauth_token = session['remote_oauth']
        return render_template('task_table.html', access_token=oauth_token)

    next_url = None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@app.route('/data_storage')
def get_data_storage():
    if 'remote_oauth' in session:
        oauth_token = session['remote_oauth']
        return render_template('data_storage.html', access_token=oauth_token)

    next_url = None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@app.route('/results_storage')
def get_results_storage():
    if 'remote_oauth' in session:
        oauth_token = session['remote_oauth']
        return render_template('result_storage.html', access_token=oauth_token)

    next_url = None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@app.route('/profile_settings')
def get_profile_settings():
    if 'remote_oauth' in session:
        oauth_token = session['remote_oauth']

        return render_template(
            'profile_settings.html',
            access_token=oauth_token
        )

    next_url = None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@app.route('/quit')
def quit():
    next_url = None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )

if __name__ == '__main__':
    import os
    os.environ['DEBUG'] = 'true'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    app.run(host='0.0.0.0', port=8000)
