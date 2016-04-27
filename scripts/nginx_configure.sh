#!/bin/bash


# ----------------------------------------------------------------------------

SUDO=sudo
sudo true

PWD=$(pwd)/scripts

# ----------------------------------------------------------------------------

# Default values
UPDATE_CONFIG=true
RESTART_NGINX=false

# ----------------------------------------------------------------------------

if [[ -f /etc/nginx/sites-available/nginx.conf ]];
then
    echo -n "Configuration file is exist. Update? [Y/n]: "
    read IS_UPDATE_CONFIG
    if [[ $IS_UPDATE_CONFIG == "n" || $IS_UPDATE_CONFIG == "N" ]];
    then
        UPDATE_CONFIG=false
    else
        echo "Removing old configure file..."
        $SUDO rm /etc/nginx/sites-available/nginx.conf
        echo "Removed."
    fi
fi


if [[ $UPDATE_CONFIG == true ]];
then
    echo "Coping nginx configuration file..."
    $SUDO cp $PWD/nginx.conf /etc/nginx/sites-available/nginx.conf
    echo "Copied."

    RESTART_NGINX=true
fi


if [[ -f /etc/nginx/sites-enabled/nginx.conf ]];
then
    echo "Nginx configuration file is already actived."
else
    echo "Activation nginx configuration file..."
    $SUDO ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf
    echo "Activated."

    RESTART_NGINX=true
fi


if [[ $RESTART_NGINX == true ]];
then
    echo "Restarting nginx..."
    $SUDO service nginx restart
    echo "Nginx restarted."
else
    echo "Nginx is not updated."
fi
