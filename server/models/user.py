from models import db

from werkzeug.security import generate_password_hash, check_password_hash


user_groups = db.Table(
    'user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_group_id', db.Integer, db.ForeignKey('user_group.id'))
)


class User(db.Model):
    """
    User model.
    """
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50))

    email = db.Column(db.String(50), unique=True)

    password_hash = db.Column(db.String(80))

    user_groups = db.relationship(
        'UserGroup',
        secondary=user_groups,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, name, email, password):
        self.name = name
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
