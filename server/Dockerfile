FROM python:3.4-slim

RUN apt-get update
RUN apt-get install build-essential libpq-dev python-dev gcc mercurial -y

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
COPY . /home/user/server

RUN chown user:user /home/user -R

WORKDIR /home/user/server

RUN pip3 install -r requirements.txt
RUN python -m flake8 .

USER user

ENV OAUTHLIB_INSECURE_TRANSPORT=true

CMD ["uwsgi", \
 "--chdir=/home/user/server", \
 "--http-socket=0.0.0.0:5000", \
 "--master", \
 "--module=server:app", \
 "--py-autoreload=3", \
 "--pidfile=/tmp/uwsgi.pid", \
 "--processes=2", \
 "--threads=2", \
 "--logger=file:/home/user/server/uwsgi.log"]
