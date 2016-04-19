FROM python:2.7-slim

RUN apt-get update
RUN apt-get install build-essential libpq-dev python-dev gcc -y

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
COPY . /home/user/server
WORKDIR /home/user/server

RUN pip install -r requirements.txt
# RUN python -m flake8 .

USER user

CMD ["uwsgi", "--chdir=/home/user/server", "--http-socket=0.0.0.0:5555", "--master", "--module=server:app", "--py-autoreload=3", "--pidfile=/tmp/uwsgi.pid", "--processes=2", "--threads=2"]
