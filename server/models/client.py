from models import db


class Client(db.Model):
    """
    Client model.
    """
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
