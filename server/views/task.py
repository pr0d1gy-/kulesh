from flask import request, jsonify

from datetime import datetime

from views.base_view import BaseMethodView

from tasks import execute_code

from models import db
from models.task import Task
from models.function import Function
from models.data import Data

from oauth_provider import CodeRunnerOAuth2Provider

from utils import current_user

from forms.task import TaskForm


oauth = CodeRunnerOAuth2Provider()


class TaskListView(BaseMethodView):
    """
    Task list resource.
    """
    @oauth.require_oauth()
    def get(self):
        tasks = Task.query.join('data').join('function').all()

        if not tasks:
            return jsonify(
                status='Error',
                msg='No data available'
            ), 400

        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'name': task.function.name,
                'code': task.code,
                'data': task.data.data,
                'updated': task.updated
            })

        return jsonify(
            status='Success',
            msg='Task list',
            task_list=task_list
        )

    @oauth.require_oauth()
    def post(self):
        name = request.values.get('name', None)
        code = request.values.get('code', None)
        data = request.values.get('data', '')

        form = TaskForm(name=name, code=code, data_field=data)

        if not form.validate():
            errors = {}
            if len(form.name.errors):
                errors['name'] = form.name.errors
            if len(form.code.errors):
                errors['code'] = form.code.errors
            if len(form.data_field.errors):
                errors['data'] = form.data_field.errors

            return jsonify(
                status='Error',
                type='Validation',
                msg=errors
            ), 400

        try:

            created = datetime.utcnow()

            function = Function(
                name=name,
                created=created,
                user=current_user(),
            )

            db.session.add(function)
            db.session.commit()

            data = Data(data=data)
            db.session.add(data)
            db.session.commit()

            updated = created
            task = Task(
                function_id=function.id,
                updated=updated,
                code=code,
                version=None,
                data_id=data.id
            )

            db.session.add(task)
            db.session.commit()

            return jsonify(
                status='Success',
                msg='Task was created.',
                task_id=task.id
            ), 201

        except Exception as e:
            db.session.rollback()

            return jsonify(
                status='Error',
                msg='Task was not created.',
                details=str(e)
            ), 500


class TaskItemView(BaseMethodView):
    """
    Task item resource.
    """
    @oauth.require_oauth()
    def get(self, task_id):
        task = Task.query.get(task_id).join('data').join('function')
        if not task:
            return jsonify(
                status='Error',
                msg='No data available.'
            ), 400

        task = {
            'id': task.id,
            'name': task.function.name,
            'code': task.code,
            'data': task.data.data,
            'updated': task.updated
        }

        return jsonify(
            status='Success',
            msg='Task list',
            task=task
        )

    # @oauth.require_oauth()
    # def put(self, task_id):
    #     pass

    @oauth.require_oauth()
    def delete(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify(
                status='Error',
                msg='Task #%s not exist' % task_id
            ), 400

        try:
            db.session.delete(task)
            db.session.commit()

            return jsonify(
                status='Success',
                msg='Task removed',
                task_id=task.id
            )

        except Exception:
            return jsonify(
                status='Error',
                msg='Can not remove task'
            ), 500


@oauth.require_oauth()
def run_task(task_id):
    try:

        task = Task.query.get(task_id)
        if not task:
            raise Exception('Task was not found.')

        execute_code.delay(task_id)

        resp = jsonify(
            status='Success',
            msg='Result row added'
        )

    except Exception as e:
        resp = jsonify(
            status='Error',
            msg='Result not added. ' + str(e)
        ), 400

    return resp
