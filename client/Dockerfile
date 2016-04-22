FROM python:2.7-slim

RUN apt-get update
RUN apt-get install build-essential libpq-dev python-dev gcc mercurial -y

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
COPY . /home/user/client

RUN chown user:user /home/user -R

WORKDIR /home/user/client

RUN pip install -r requirements.txt
RUN python -m flake8 .

USER user

ENV OAUTHLIB_INSECURE_TRANSPORT=true

CMD ["uwsgi", \
 "--chdir=/home/user/client", \
 "--http-socket=0.0.0.0:8000", \
 "--master", \
 "--module=client:app", \
 "--py-autoreload=3", \
 "--pidfile=/tmp/uwsgi.pid", \
 "--processes=2", \
 "--threads=2", \
 "--logger=file:/home/user/client/uwsgi.log"]
