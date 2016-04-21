import os


CLIENT_ID = 'EiP1YEdKoBnhOV5LrmXGPLbfp8OSqxkuQnqlu9M0'
CLIENT_SECRET = 'EXksbecWsatbcO5LDEtUDeFwp5gJduQXuQXHlDViFUlq257MLR'


BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:8000')

BASE_SERVER_URL = 'http://server:5000'

ACCESS_TOKEN_URL = BASE_SERVER_URL + '/oauth/token'
AUTHORIZE_URL = BASE_SERVER_URL + '/oauth/authorize'
BASE_API_URL = BASE_SERVER_URL + '/api/'
