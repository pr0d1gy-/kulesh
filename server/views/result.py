from flask import request, jsonify

from datetime import datetime

from views.base_view import BaseMethodView

from models import db
from models.result import Result
from models.status import Status

from oauth_provider import CodeRunnerOAuth2Provider


oauth = CodeRunnerOAuth2Provider()


class ResultListMethodView(BaseMethodView):
    """
    Result list resource.
    """
    @oauth.require_oauth()
    def get(self):
        results = Result.query.all()
        if not results:
            return jsonify(
                status='Error',
                msg='No results available'
            )

        result_list = []
        for result in results:
            task_name = '-'
            if result.task and \
                    result.task.function and \
                    result.task.function.name:
                task_name = result.task.function.name

            result_list.append({
                'id': result.id,
                'task_name': task_name,
                'date_start': result.date_start,
                'date_end': result.date_end,
                'task_id': result.task_id,
                'result': result.result,
            })

        return jsonify(
            status='Success',
            msg='Results list',
            result_list=result_list
        )

    @oauth.require_oauth()
    def post(self):
        date_start = None  # Task was started at
        date_end = datetime.utcnow()
        task_id = request.values.get('task_id', None)
        status_id = request.values.get('status_id', None)
        result = request.values.get('result', None)

        status = Status(id=status_id)

        try:
            result = Result(
                date_start=date_start,
                date_end=date_end,
                task_id=task_id,
                status_id=status.id,
                result=result
            )

            db.session.add(result)
            db.session.commit()

            return jsonify(
                status='Success',
                msg='Task result added',
                result_id=result.id
            ), 201

        except Exception:
            db.session.rollback()

            return jsonify(
                status='Error',
                msg='Result not added'
            ), 500


class ResultItemMethodView(BaseMethodView):
    """
    Result item resource.
    """
    @oauth.require_oauth()
    def delete(self, result_id):
        result = Result.query.get(result_id)
        if not result:
            return jsonify(
                status='Error',
                msg='Result row #%s not exist' % result_id
            ), 400

        try:
            db.session.delete(result)
            db.session.commit()

            return jsonify(
                status='Success',
                msg='Result row removed',
                result_id=result.id
            )

        except Exception:
            return jsonify(
                status='Error',
                msg='Can not remove result row'
            ), 500
