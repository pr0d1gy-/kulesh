from flask import request, jsonify

from views.base_view import BaseMethodView

from models import db
from models.user import User

from oauth_provider import CodeRunnerOAuth2Provider

from utils import current_user


oauth = CodeRunnerOAuth2Provider()


@oauth.require_oauth()
def me():
    user = request.oauth.user

    return jsonify(
        username=user.name,
        email=user.email
    )


class UserItemMethodView(BaseMethodView):
    """
    User item resource.
    """
    @oauth.require_oauth()
    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(
                status='Error',
                msg='User was not found.'
            ), 400

        if current_user().id != user.id:
            return jsonify(
                status='Error',
                msg='Not permission'
            ), 403

        name = request.values.get('name', None)
        email = request.values.get('email', None)
        password = request.values.get('password', None)

        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.password_hash = password

        try:
            db.session.commit()

            return jsonify(
                status='Success',
                msg='User info updated'
            )

        except Exception:
            return jsonify(
                status='Error',
                msg='Can not update user'
            ), 500

    @oauth.require_oauth()
    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(
                status='Error',
                msg='User was not found.'
            ), 400

        if current_user().id != user.id:
            return jsonify(
                status='Error',
                msg='Not permission'
            ), 403

        try:
            db.session.delete(user)
            db.session.commit()

            return jsonify(
                status='Success',
                msg='User removed'
            )

        except Exception:
            return jsonify(
                status='Error',
                msg='Can not remove user'
            ), 500

    @oauth.require_oauth()
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(
                status='Error',
                msg='User was not found.'
            ), 400

        if current_user().id != user.id:
            return jsonify(
                status='Error',
                msg='Not permission'
            ), 403

        return jsonify(
            status='Success',
            msg='User info',
            name=user.name,
            email=user.email
        )
