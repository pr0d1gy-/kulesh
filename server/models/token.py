from models import db


class Token(db.Model):
    """
    Token model.
    """
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
