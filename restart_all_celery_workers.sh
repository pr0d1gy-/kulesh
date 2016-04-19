#!/bin/bash


# ----------------------------------------------------------------------------

SUDO=sudo
sudo true


# ----------------------------------------------------------------------------


CELERY_WORKERS=$(sudo docker ps -a | grep 'celery-worker-' | awk  '{print $13}')

for CELERY_WORKER in ${CELERY_WORKERS[@]};
do
    $SUDO docker restart $CELERY_WORKER
done;
