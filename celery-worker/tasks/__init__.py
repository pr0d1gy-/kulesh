from celery import Celery
import celeryconfig


app = Celery('tasks')
app.config_from_object(celeryconfig)


@app.task
def add(x, y):
    print('---------')
    return x + y
