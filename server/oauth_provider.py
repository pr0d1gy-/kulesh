from datetime import datetime, timedelta

from flask_oauthlib.provider import OAuth2Provider

from models.user import User
from models.user_group import UserGroup
from models.client import Client
from models.grant import Grant
from models.token import Token

from utils import current_user

from models import db

from flask import current_app


user = User()
user_group = UserGroup()


class CodeRunnerOAuth2Provider(OAuth2Provider):

    app = current_app

    @staticmethod
    def _clientgetter(client_id):
        return Client.query.filter_by(client_id=client_id).first()

    @staticmethod
    def _grantgetter(client_id, code):
        return Grant.query.filter_by(client_id=client_id, code=code).first()

    @staticmethod
    def _grantsetter(client_id, code, request, *args, **kwargs):
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

    @staticmethod
    def _tokengetter(access_token=None, refresh_token=None):
        if access_token:
            return Token.query.filter_by(access_token=access_token).first()

        elif refresh_token:
            return Token.query.filter_by(refresh_token=refresh_token).first()

        return None

    @staticmethod
    def _tokensetter(token, request, *args, **kwargs):
        Token.query.filter_by(
            client_id=request.client.client_id,
            user_id=request.user.id
        ).delete()

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
