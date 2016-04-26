import os


SERVER_HOST = '0.0.0.0'
SERVER_POST = 5000


DEBUG = True


# BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:8000')
BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1')


DB_SETTINGS = {
    'name': os.environ.get('DB_NAME', 'cr'),
    'user': os.environ.get('DB_USER', 'cr_user'),
    'password': os.environ.get('DB_PASSWD', 'crpswrd'),
    'host': os.environ.get('DB_HOST', 'localhost')
}


# Flask configuration
CONFIG = {
    'SQLALCHEMY_DATABASE_URI':
        'postgresql://{user}:{password}@{host}/{name}'.format(**DB_SETTINGS),
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
}
