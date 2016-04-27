#!/bin/bash


# ----------------------------------------------------------------------------


SUDO=sudo
sudo true

PWD=$(pwd)/scripts


# ----------------------------------------------------------------------------


DOWNLOAD_IMAGES=('redis' 'postgres')
BUILD_IMAGES=('celery-worker' 'server' 'client')


# ----------------------------------------------------------------------------

# Download docker images?
echo -n "Download docker images [N/y]: "
read IS_DOWNLOAD_IMAGES
if [[ $IS_DOWNLOAD_IMAGES == "y" || $IS_DOWNLOAD_IMAGES == "Y" ]];
then
    IS_DOWNLOAD_IMAGES=true
else
    IS_DOWNLOAD_IMAGES=false
fi


# Build docker local images?
echo -n "Build docker local images [N/y]: "
read IS_BUILD_LOCAL_IMAGES
if [[ $IS_BUILD_LOCAL_IMAGES == "y" || $IS_BUILD_LOCAL_IMAGES == "Y" ]];
then
    IS_BUILD_LOCAL_IMAGES=true
else
    IS_BUILD_LOCAL_IMAGES=false
fi


# Start docker images?
echo -n "Start dockers images [n/Y]: "
read IS_START_IMAGES
if [[ $IS_START_IMAGES == "n" || $IS_START_IMAGES == "N" ]];
then
    IS_START_IMAGES=false
else
    IS_START_IMAGES=true
    $SUDO chmod "+x" "$PWD/start_docker_images.sh"
fi


# Cofigure nginx?
echo -n "Configure nginx [N/y]: "
read IS_CONFIGURE_NGINX
if [[ $IS_CONFIGURE_NGINX == "n" || $IS_CONFIGURE_NGINX == "N" ]];
then
    IS_CONFIGURE_NGINX=true
else
    IS_CONFIGURE_NGINX=false
    $SUDO chmod "+x" "$PWD/nginx_configure.sh"
fi

# ----------------------------------------------------------------------------

# Download local images
if [[ $IS_DOWNLOAD_IMAGES == true ]];
then
    echo "Downloading..."

    for DOWNLOAD_IMAGE in ${DOWNLOAD_IMAGES[@]};
    do
      echo "Download $DOWNLOAD_IMAGE"
      $SUDO docker pull $DOWNLOAD_IMAGE:latest
      echo "Compleate download $DOWNLOAD_IMAGE"
    done;

    echo "Downloading was complete."
fi


# Build local images
if [[ $IS_BUILD_LOCAL_IMAGES == true ]];
then
    echo "Building..."

    for BUILD_IMAGE in ${BUILD_IMAGES[@]};
    do
      echo "Build $BUILD_IMAGE"
      $SUDO docker build -t $BUILD_IMAGE $BUILD_IMAGE
      echo "Builded $BUILD_IMAGE"
    done;

    echo "Building was complete."
fi


# Nginx config
if [[ $IS_CONFIGURE_NGINX == true ]];
then
    echo "Configure nginx..."
    $SUDO "$PWD/nginx_configure.sh"
    echo "Nginx was configured."
fi


# Start
if [[ $IS_START_IMAGES == true ]];
then
    echo "Starting..."
    $SUDO "$PWD/start_docker_images.sh"
    echo "Starting was complete."
fi

# ----------------------------------------------------------------------------
