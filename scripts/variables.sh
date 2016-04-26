#!/bin/bash

REDIS_CONTAINER_NAME="redis-brocker"
POSTGRES_CONTAINER_NAME="postgresql"
CELERY_WORKER_CONTAINER_NAME="celery-worker"
SERVER_CONTAINER_NAME="web-server"
CLIENT_CONTAINER_NAME="web-client"

SERVER_DB_NAME="cr"
SERVER_DB_USER="cr_user"
SERVER_DB_PASSWD="crpswrd"

BASE_URL="/"

CLIENT_REDIRECT_URI="http://127.0.0.1/authorized"
