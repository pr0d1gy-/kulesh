# coding: utf-8

import json
from datetime import datetime, timedelta

from flask import Flask
from flask import session, request, url_for, flash, \
    render_template, redirect, jsonify
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from flask.ext.cors import CORS

from models import db
from models import User, Client, Grant, Token, Function, Task, Result, Data

from jinja_filters import message_alert_glyph, messages_alert_tags


app = Flask(__name__, template_folder='templates')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = True
app.secret_key = 'c0derunner'

app.config.update({
    'SQLALCHEMY_DATABASE_URI': '/postgresql:/web-server/postgres',
    # 'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.cr',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
})

db.init_app(app)
oauth = OAuth2Provider(app)


def run_task(task_id):
    task = Task.query.get(task_id)
    if task:
        code = task.code.strip()
        data_obj = Data.query.get(task.data_id)
        if data_obj:
            data = json.loads(data_obj.data.strip())
        else:
            return jsonify(status='Error', msg='No data available')

        local_vars = {}

        code = compile(code % data, "<string>", "exec")
        exec(code, globals(), local_vars)

        try:
            res = Result(result=local_vars['result'])
            db.session.add(res)
            db.session.commit()
            return jsonify(status='Success', msg='Result row added')
        except:
            db.session.rollback()
            return jsonify(status='Error', msg='Result not added')
    else:
        return jsonify(status='Error', msg='Task is not available')


@app.route('/task/run/<task_id>')
def task(task_id):
    return run_task(task_id)


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def get_tasks():
    tasks = Task.query.all()
    if tasks:
        tlist = []
        for task in tasks:
            tlist.append({
                'id': task.id,
                'code': task.code,
                'name': task.function.name,
                'updated': task.updated,
                'function_id': task.function_id,
                'version': task.version
            })
        return jsonify(status='Success', msg='Task list', tlist=tlist)
    else:
        return jsonify(status='Error', msg='No data available')


def add_task(request):
    name = request.values.get('name', None)
    code = request.values.get('code', None)
    version = request.values.get('version', None)

    created = datetime.utcnow()

    if not name or not code:
        return jsonify(status='Error', msg='Some required field is empty')

    try:
        function = Function(
            name=name,
            created=created,
            user=current_user(),
        )
        db.session.add(function)
        db.session.commit()

        updated = created
        task = Task(
            function_id=function.id,
            updated=updated,
            code=code,
            version=version,
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(status='Success', msg='Task added', task_id=task.id)
    except:
        db.session.rollback()
        return jsonify(status='Error', msg='Task not added')


def remove_task(pk):
    task = Task.query.get(pk)
    if not task:
        return jsonify(status='Error', msg=('Task #%s not exist') % pk)

    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify(status='Success',
                       msg='Task removed', task_id=task.id)
    except:
        return jsonify(status='Error', msg='Can not remove task')


def add_user(request, user):
    name = request.values.get('name', None)
    email = request.values.get('email', None)
    password = request.values.get('password', None)

    if name:
        user.name = name
    if email:
        user.email = email
    if password:
        user.pwdhash = password

    try:
        db.session.commit()
        return jsonify(status='Success', msg='User info updated')
    except:
        return jsonify(status='Error', msg='Can not update user')


def remove_user(user):
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(status='Success', msg='User removed')
    except:
        return jsonify(status='Error', msg='Can not remove user')


def get_all_data():
    data_list = Data.query.all()
    if data_list:
        dlist = []
        for data in data_list:
            dlist.append({
                'id': data.id,
                'data': data.data,
                'link': data.link
            })
        return jsonify(status='Success', msg='Data list', dlist=dlist)
    else:
        return jsonify(status='Error', msg='No data available')


def add_data_row(request):
    link = request.values.get('link', None)
    data = request.values.get('data', None)

    try:
        data = Data(link=link)
        db.session.add(data)
        db.session.commit()
        return jsonify(status='Success', msg='Data row added', data_id=data.id)
    except:
        db.session.rollback()
        return jsonify(status='Error', msg='Data not added')


def remove_data_row(pk):
    data = Data.query.get(pk)
    if not data:
        return jsonify(status='Error', msg=('Data row #%s not exist') % pk)

    try:
        db.session.delete(data)
        db.session.commit()
        return jsonify(status='Success',
                       msg='Data row removed', data_id=data.id)
    except:
        return jsonify(status='Error', msg='Can not remove data row')


def get_all_results():
    results = Result.query.all()
    if results:
        rlist = []
        for result in results:
            rlist.append({
                'id': result.id,
                'task_name': result.task.function.name,
                'date_start': result.date_start,
                'date_end': result.date_end,
                'task_id': result.task_id,
                'result': result.result,
            })
        return jsonify(status='Success', msg='Results list', rlist=rlist)
    else:
        return jsonify(status='Error', msg='No results available')


def add_result(request):
    date_start = None  # Task was started at
    date_end = datetime.utcnow()
    task_id = request.values.get('task_id', None)
    status_id = request.values.get('status_id', None)
    result = request.values.get('result', None)

    try:
        result = Result(
            date_start=date_start,
            date_end=date_end,
            task_id=task_id,
            status_id=status_id,
            result=result)
        db.session.add(result)
        db.session.commit()
        return jsonify(status='Success',
                       msg='Task result added', result_id=result.id)
    except:
        db.session.rollback()
        return jsonify(status='Error', msg='Result not added')


def remove_result(pk):
    result = Result.query.get(pk)
    if not result:
        return jsonify(status='Error', msg=('Result row #%s not exist') % pk)

    try:
        db.session.delete(result)
        db.session.commit()
        return jsonify(status='Success',
                       msg='Result row removed', result_id=result.id)
    except:
        return jsonify(status='Error', msg='Can not remove result row')


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_user(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@app.route('/client')
def client():
    user = current_user()
    if not user:
        session['id'] = 1  # temporary decision
        # return redirect('/register')
    item = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=' '.join([
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


@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None


@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user()
    if not user:
        return redirect(url_for('login'))

    # if user is authorized return True
    return True


@app.route('/api/me')
@oauth.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.name, email=user.email)


@app.route('/api/tasks', methods=['GET', 'POST'])
@app.route('/api/tasks/<pk>', methods=['DELETE'])
@oauth.require_oauth()
def tasks(pk=None):
    if request.method == 'GET':
        return get_tasks()
    elif request.method == 'POST':
        return add_task(request)
    elif request.method == 'DELETE':
        return remove_task(pk)


@app.route('/api/users/<pk>', methods=['GET', 'PUT', 'DELETE'])
@oauth.require_oauth()
def users(pk=None):
    user = User.query.filter_by(id=pk).first()
    if not user:
        return jsonify(status='Error', msg='User not exist')

    if request.method == 'GET':
        return jsonify(status='Success', msg='User info',
                       name=user.name, email=user.email)
    elif request.method == 'PUT':
        return add_user(request, user)
    elif request.method == 'DELETE':
        return remove_user(user)


@app.route('/api/data', methods=['GET', 'POST'])
@app.route('/api/data/<pk>', methods=['DELETE'])
@oauth.require_oauth()
def data(pk=None):
    if request.method == 'GET':
        return get_all_data()
    elif request.method == 'POST':
        return add_data_row(request)
    elif request.method == 'DELETE':
        return remove_data_row(pk)


@app.route('/api/results', methods=['GET', 'POST'])
@app.route('/api/results/<pk>', methods=['DELETE'])
@oauth.require_oauth()
def results(pk=None):
    if request.method == 'GET':
        return get_all_results()
    elif request.method == 'POST':
        return add_result(request)
    elif request.method == 'DELETE':
        return remove_result(pk)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """
    Server authorization page
    """
    if 'id' in session:
        return redirect('http://127.0.0.1:8000/')

    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['id'] = user.id
        else:
            flash(u'User does not exist or the password is incorrect', 'error')

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register')
def register():
    """
    Server registration page
    """
    return render_template('register.html')


app.jinja_env.filters['glyph_class'] = message_alert_glyph
app.jinja_env.filters['tag_class'] = messages_alert_tags
