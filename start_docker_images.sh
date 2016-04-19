#!/bin/bash


# ----------------------------------------------------------------------------

SUDO=sudo
sudo true


# ----------------------------------------------------------------------------


source variables.sh


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


# Reset postgres
echo -n "Reset postgre N/y? "
read IS_RESET_POSTGRES

# ----------------------------------------------------------------------------


# Redis start
if [[ $($SUDO docker ps | grep "$REDIS_CONTAINER_NAME") == "" ]];
then
    echo 'Redis starting...'
    $SUDO docker run -d \
      --name "$REDIS_CONTAINER_NAME" -P redis
    echo 'Redis started.'
else
    echo 'Redis is already started.'
fi


# Postgres start
if [[ $($SUDO docker ps | grep "$POSTGRES_CONTAINER_NAME") == "" ]];
then
    echo 'Postgres starting...'
    $SUDO docker run -d \
      --name "$POSTGRES_CONTAINER_NAME" -P postgres
    echo 'Postgres started.'

    if [[ $IS_RESET_POSTGRES == "y" || $IS_RESET_POSTGRES == "Y" ]];
    then
        $SUDO chmod +x reset_postgres.sh
        $SUDO reset_postgres.sh
    fi
else
    echo 'Postgres is already started.'
fi


# Celery workers start
for WORKER_NUM in $(seq 1 $WORKER_COUNT);
do
    if [[ $($SUDO docker ps | grep "$CELERY_WORKER_CONTAINER_NAME-$WORKER_NUM") == "" ]];
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
if [[ $($SUDO docker ps | grep "$SERVER_CONTAINER_NAME") == "" ]];
then
    echo 'Server starting...'
    $SUDO docker run -d \
      -p 5555:5555 \
      --link $POSTGRES_CONTAINER_NAME:postgres \
      -e DB_NAME=$SERVER_DB_NAME \
      -e DB_USER=$SERVER_DB_USER \
      -e DB_PASSWD=$SERVER_DB_PASSWD \
      -e DB_HOST="postgres" \
      --name $SERVER_CONTAINER_NAME server
    echo 'Server started.'
else
    echo 'Server is already started.'
fi


# Client start
# $SUDO
