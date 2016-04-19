#!/bin/bash


# ----------------------------------------------------------------------------

SUDO=sudo
sudo true


# ----------------------------------------------------------------------------


REDIS_CONTAINER_NAME="redis-brocker"
POSTGRES_CONTAINER_NAME="postgresql"
CELERY_WORKER_CONTAINER_NAME="celery-worker"
SERVER_CONTAINER_NAME="web-server"


# ----------------------------------------------------------------------------


# How many workers to start for cellery?
echo -n "How many workers to start for celery (1 .. 10)?: "
read WORKER_COUNT
IS_VALID_WORKER_COUNT=$(test -z $(echo $WORKER_COUNT | sed s/[0-9]//g) && echo "1" || echo "0")

if [[ $IS_VALID_WORKER_COUNT == "0" ]];
then
		WORKER_COUNT=1
else
		if [[ $WORKER_COUNT -le 1 || $WORKER_COUNT == "" ]];
		then
			  WORKER_COUNT=1
		elif [[ $WORKER_COUNT -gt 10 ]];
		then
				WORKER_COUNT=10
		fi
fi


# ----------------------------------------------------------------------------


# Redis start
if [[ $(sudo docker ps | grep "$REDIS_CONTAINER_NAME") == "" ]];
then
		echo 'Redis starting...'
		$SUDO docker run -d \
			--name "$REDIS_CONTAINER_NAME" -P redis
		echo 'Redis started.'
else
		echo 'Redis is already started.'
fi


# Postgres start
if [[ $(sudo docker ps | grep "$POSTGRES_CONTAINER_NAME") == "" ]];
then
		echo 'Postgres starting...'
		$SUDO docker run -d \
			--name "$POSTGRES_CONTAINER_NAME" -P postgres
		echo 'Postgres started.'
else
		echo 'Postgres is already started.'
fi


# Celery workers start
for WORKER_NUM in $(seq 1 $WORKER_COUNT);
do
		if [[ $(sudo docker ps | grep "$CELERY_WORKER_CONTAINER_NAME-$WORKER_NUM") == "" ]];
		then
				echo "Celery $WORKER_NUM worker starting..."
				$SUDO docker run -d \
					--link $REDIS_CONTAINER_NAME:redis \
					-e CELERY_BROKER_URL="redis://redis/1" \
					-e CELERY_RESULT_BACKEND="redis://redis/2" \
					--name "$CELERY_WORKER_CONTAINER_NAME-$WORKER_NUM" $CELERY_WORKER_CONTAINER_NAME
				echo "Celery $WORKER_NUM worker started."
		else
				echo "Celery $WORKER_NUM worker is already started."

		fi

done;


# Server start
if [[ $(sudo docker ps | grep "$SERVER_CONTAINER_NAME") == "" ]];
then
		echo 'Server starting...'
		$SUDO docker run -d \
			-p 5555:5555 \
			--link postgresql:postgres \
			--name $SERVER_CONTAINER_NAME server
		echo 'Server started.'
else
		echo 'Server is already started.'
fi


# Client start
# $SUDO
