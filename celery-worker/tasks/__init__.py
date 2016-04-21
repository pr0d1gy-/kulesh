import os
import json
import psycopg2
import psycopg2.extras
import celeryconfig

from datetime import datetime
from celery import Celery


DB_NAME = os.environ.get('DB_NAME', 'cr')
DB_USER = os.environ.get('DB_USER', 'cr_user')
DB_PASSWD = os.environ.get('DB_PASSWD', 'crpswrd')
DB_HOST = os.environ.get('DB_HOST', 'postgres')


app = Celery('tasks')
app.config_from_object(celeryconfig)


POSTGRES_CONNECTION_STRING = \
    "dbname='%s' user='%s' host='%s' password='%s'" % (
        DB_NAME,
        DB_USER,
        DB_HOST,
        DB_PASSWD
    )


SQL_SELECT_TASK_BY_ID = 'SELECT * from task where id=%s;'
SQL_SELECT_TASK_DATA_BY_ID = 'SELECT * from data where id=%s;'
SQL_INSERT_TASK_RESULT = \
    'INSERT INTO result (date_end, task_id, status_id, result) ' \
    'VALUES (%s, %s, %s, %s);'


@app.task
def execute_code(task_id):
    try:
        print(task_id)

        conn = psycopg2.connect(POSTGRES_CONNECTION_STRING)

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(SQL_SELECT_TASK_BY_ID % str(task_id))

        task = cur.fetchall()

        if task:
            task = task[0]

            print(task)

            code = task['code'].strip()

            cur.execute(SQL_SELECT_TASK_DATA_BY_ID % task['data_id'])
            data_obj = cur.fetchall()

            if data_obj:
                data_obj = data_obj[0]
                data = json.loads(data_obj['data'].strip())

                local_vars = {}
                code_obj = compile(code, '<string>', 'exec')

                exec(code_obj, globals(), local_vars)

                f = local_vars['f']

                result = f(data)

                cur.execute(SQL_INSERT_TASK_RESULT % (
                    datetime.utcnow(),
                    task_id,
                    1,
                    json.dumps(result)
                ))

                conn.commit()

    except Exception as e:
        print(e)

    return json.dumps({
        'status': 'Success',
        'msg': 'Task ended'
    })
