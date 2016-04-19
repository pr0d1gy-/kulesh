# from werkzeug.security import generate_password_hash, \
#      check_password_hash
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_group_id', db.Integer, db.ForeignKey('user_group.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(40), unique=True)
    pwdhash = db.Column(db.String(80))
    user_groups = db.relationship('UserGroup', secondary=user_groups,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


class Client(db.Model):
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Function(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created = db.Column(db.DateTime)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    updated = db.Column(db.DateTime)
    version = db.Column(db.String(100))
    function_id = db.Column(
        db.Integer, db.ForeignKey('function.id', ondelete='CASCADE')
    )
    function = db.relationship('Function')
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'))
    data = db.relationship('Data')


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    link = db.Column(db.Text)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    task_id = db.Column(
        db.Integer, db.ForeignKey('task.id', ondelete='CASCADE')
    )
    task = db.relationship('Task')
    result = db.Column(db.Text)
    status_id = db.Column(
        db.Integer, db.ForeignKey('status.id', ondelete='CASCADE')
    )
    status = db.relationship('Status')


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))