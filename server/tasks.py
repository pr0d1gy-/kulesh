import celeryconfig

from celery import Celery


app = Celery('tasks')
app.config_from_object(celeryconfig)


@app.task
def execute_code(task_id):
    pass
