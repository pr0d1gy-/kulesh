#!/bin/bash


# ----------------------------------------------------------------------------

SUDO=sudo
sudo true

# ----------------------------------------------------------------------------

source variables.sh

# ----------------------------------------------------------------------------

SQL_DB_DROP="DROP DATABASE IF EXISTS $SERVER_DB_NAME;"
SQL_DB_CREATE="CREATE DATABASE $SERVER_DB_NAME;"

SQL_USER_DROP="DROP USER IF EXISTS $SERVER_DB_USER;"
SQL_USER_CREATE="CREATE USER $SERVER_DB_USER WITH PASSWORD '$SERVER_DB_PASSWD';"

SQL_DB_GRANT_USER="GRANT ALL PRIVILEGES ON DATABASE $SERVER_DB_NAME TO $SERVER_DB_USER;"

# ----------------------------------------------------------------------------

POSTGRE_CONTAINER_ID=$($SUDO docker ps | grep "$POSTGRES_CONTAINER_NAME" | awk '{ print $1 }')

if [[ $POSTGRE_CONTAINER_ID == "" ]];
then
	echo "Postgre was not found."
	exit
fi


echo "Postgres container id: $POSTGRE_CONTAINER_ID"
echo "Start reseting..."


# DROP AND CREATE NEW DATABASE
echo $SQL_DB_DROP
$SUDO docker exec -it $POSTGRE_CONTAINER_ID psql -U postgres -c "$SQL_DB_DROP"

echo $SQL_DB_CREATE
$SUDO docker exec -it $POSTGRE_CONTAINER_ID psql -U postgres -c "$SQL_DB_CREATE"


# DROP AND CREATE NEW USER
echo $SQL_USER_DROP
$SUDO docker exec -it $POSTGRE_CONTAINER_ID psql -U postgres -c "$SQL_USER_DROP"

echo $SQL_USER_CREATE
$SUDO docker exec -it $POSTGRE_CONTAINER_ID psql -U postgres -c "$SQL_USER_CREATE"


# GRANT DB TO USER
echo $SQL_DB_GRANT_USER
$SUDO docker exec -it $POSTGRE_CONTAINER_ID psql -U postgres -c "$SQL_DB_GRANT_USER"


echo 'Reseting is finished.'
