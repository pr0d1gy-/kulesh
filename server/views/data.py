from flask import request, jsonify

from views.base_view import BaseMethodView

from models import db
from models.data import Data

from oauth_provider import CodeRunnerOAuth2Provider


oauth = CodeRunnerOAuth2Provider()


class DataListMethodView(BaseMethodView):
    """
    Data list resource.
    """
    @oauth.require_oauth()
    def get(self):
        data_set = Data.query.all()
        if not data_set:
            return jsonify(
                status='Error',
                msg='No data available'
            )

        data_list = []
        for data in data_list:
            data_list.append({
                'id': data.id,
                'data': data.data,
                'link': data.link
            })

        return jsonify(
            status='Success',
            msg='Data list',
            data_list=data_list
        )

    @oauth.require_oauth()
    def post(self):
        link = request.values.get('link', None)
        data = request.values.get('data', None)

        try:
            data = Data(link=link, data=data)

            db.session.add(data)
            db.session.commit()

            return jsonify(
                status='Success',
                msg='Data row added',
                data_id=data.id
            ), 201

        except Exception:
            db.session.rollback()

            return jsonify(
                status='Error',
                msg='Data not added'
            ), 500


class DataItemMethodView(BaseMethodView):
    """
    Data item resource.
    """
    @oauth.require_oauth()
    def delete(self, result_id):
        data = Data.query.get(result_id)
        if not data:
            return jsonify(
                status='Error',
                msg='Data row #%s not exist' % result_id
            ), 400

        try:
            db.session.delete(data)
            db.session.commit()

            return jsonify(
                status='Success',
                msg='Data row removed',
                data_id=data.id
            )

        except Exception:
            return jsonify(
                status='Error',
                msg='Can not remove data row'
            ), 500
