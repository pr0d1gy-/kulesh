#!/bin/bash


# ----------------------------------------------------------------------------

SUDO=sudo
sudo true


# ----------------------------------------------------------------------------


PWD=$(pwd)/scripts
source $PWD/variables.sh


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


# Reset postgres?
echo -n "Reset postgre N/y? "
read IS_RESET_POSTGRES

# Apply migrations?
echo -n "Apply server migrations N/y? "
read IS_APPLY_MIGRATIONS

# Is insert test user?
echo -n "Is insert test user N/y? "
read IS_INSERT_FIXTURES

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
else
    echo 'Postgres is already started.'
fi

# Postgre reset?
if [[ $IS_RESET_POSTGRES == "y" || $IS_RESET_POSTGRES == "Y" ]];
then
    $SUDO chmod "+x" "$PWD/reset_postgres.sh"
    $SUDO "$PWD/reset_postgres.sh"
fi


# Celery workers start
for WORKER_NUM in $(seq 1 $WORKER_COUNT);
do
    if [[ $($SUDO docker ps | grep "$CELERY_WORKER_CONTAINER_NAME-$WORKER_NUM") == "" ]];
    then
        echo "Celery $WORKER_NUM worker starting..."
        $SUDO docker run -d \
          --link $REDIS_CONTAINER_NAME:redis \
          --link $POSTGRES_CONTAINER_NAME:postgres \
          -e CELERY_BROKER_URL="redis://redis/1" \
          -e CELERY_RESULT_BACKEND="redis://redis/2" \
          -e DB_NAME=$SERVER_DB_NAME \
          -e DB_USER=$SERVER_DB_USER \
          -e DB_PASSWD=$SERVER_DB_PASSWD \
          -e DB_HOST="postgres" \
          -e BASE_URL=$BASE_URL \
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
      -p 5000:5000 \
      --link $POSTGRES_CONTAINER_NAME:postgres \
      --link $REDIS_CONTAINER_NAME:redis \
      -e DB_NAME=$SERVER_DB_NAME \
      -e DB_USER=$SERVER_DB_USER \
      -e DB_PASSWD=$SERVER_DB_PASSWD \
      -e DB_HOST="postgres" \
      -e CELERY_BROKER_URL="redis://redis/1" \
      -e CELERY_RESULT_BACKEND="redis://redis/2" \
      -e BASE_URL=$BASE_URL \
      --name $SERVER_CONTAINER_NAME server
    echo 'Server started.'

    if [[ $IS_APPLY_MIGRATIONS == "y" || $IS_APPLY_MIGRATIONS == "Y" ]];
    then
        echo "Appling migrations..."
        $SUDO docker exec -it $SERVER_CONTAINER_NAME python /home/user/server/server.py db init
        $SUDO docker exec -it $SERVER_CONTAINER_NAME python /home/user/server/server.py db migrate
        $SUDO docker exec -it $SERVER_CONTAINER_NAME python /home/user/server/server.py db upgrade
        echo "Aplied migrations."

        if [[ $IS_INSERT_FIXTURES == "y" || $IS_INSERT_FIXTURES == "Y" ]];
        then
            echo "Inserting test user..."
            $SUDO docker exec -it $POSTGRES_CONTAINER_NAME psql -U postgres -c "insert into public.user(name, email, password_hash) values ('test_user', 'test@mail.ru', 'pbkdf2:sha1:1000$3NOVQPrz$0c1b3a5d6c4a53078d2248ea5c4e19d40953d09f');"
            $SUDO docker exec -it $POSTGRES_CONTAINER_NAME psql -U postgres -c "insert into status (id, title) VALUES (1, 'success');"
            $SUDO docker exec -it $POSTGRES_CONTAINER_NAME psql -U postgres -c "insert into status (id, title) VALUES (2, 'error');"
            echo "Insered test user."
        fi
    fi
else
    echo 'Server is already started.'
fi


# Client start
if [[ $($SUDO docker ps | grep "$CLIENT_CONTAINER_NAME") == "" ]];
then
    echo 'Client starting...'
    $SUDO docker run -d \
      -p 8000:8000 \
      --link $SERVER_CONTAINER_NAME:server \
      -e BASE_URL=$BASE_URL \
      -e BASE_SERVER_URL="http://server:5000" \
      --name $CLIENT_CONTAINER_NAME client
    echo 'Client started.'
else
    echo 'Client is already started.'
fi
