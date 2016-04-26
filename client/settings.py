import os


CLIENT_ID = '9MmWLbkXfaWUYXCibA1393Ov46JKGJDKU4J7vVro'
CLIENT_SECRET = 'rGJ6GzmXRX7NglMkaVSbrowiwX9ZpDHhz9eSuFRHXkyHDgBRPs'


BASE_URL = os.environ.get('BASE_URL', '/')

BASE_SERVER_URL = os.environ.get('BASE_SERVER_URL', 'http://127.0.0.1:5000')

ACCESS_TOKEN_URL = BASE_SERVER_URL + '/oauth/token'
AUTHORIZE_URL = '/oauth/authorize'
BASE_API_URL = '/api/'
