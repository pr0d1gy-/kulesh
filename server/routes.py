from views.task import TaskListView, run_task, TaskItemView
from views.result import ResultListMethodView, ResultItemMethodView
from views.data import DataListMethodView, DataItemMethodView
from views.user import UserItemMethodView, me

from views.auth.client import client
from views.auth.login import LoginMethodView
from views.auth.register import RegisterMethodView
from views.auth.oauth import access_token, authorize


routes = {
    # Tasks
    '/api/tasks/<task_id>/run/': ['run_task', run_task, {
        'methods': ['GET']
    }],
    '/api/tasks/': TaskListView.as_view('tasks'),
    '/api/tasks/<int:task_id>/': TaskItemView.as_view('task'),

    # Results
    '/api/results/': ResultListMethodView.as_view('results'),
    '/api/results/<int:result_id>/': ResultItemMethodView.as_view('result'),

    # Data
    '/api/data/': DataListMethodView.as_view('datas'),
    '/api/data/<int:data_id>/': DataItemMethodView.as_view('data'),

    # Oauth
    '/client': ['client', client],
    '/login': LoginMethodView.as_view('login'),
    '/register': RegisterMethodView.as_view('register'),
    '/oauth/authorize': ['authorize', authorize, {
        'methods': ['GET', 'POST']
    }],
    '/oauth/token': ['access_token', access_token, {
        'methods': ['GET', 'POST']
    }],

    # Users
    '/api/me': ['me', me],
    '/api/users/<int:user_id>': UserItemMethodView.as_view('user'),
}
