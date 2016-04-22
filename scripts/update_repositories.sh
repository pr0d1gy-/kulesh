#!/bin/bash


# ----------------------------------------------------------------------------


PWD=$(pwd)
MERCURIAL_REPOS=('celery-worker' 'client' 'server' 'scripts')

# ----------------------------------------------------------------------------

for REPOSITORY in ${MERCURIAL_REPOS[@]};
do
    if [[ -d $PWD/$REPOSITORY ]];
    then
        hg pull -u https://$USERNAME:$PASSWORD@bitbucket.org/lightitcr/$REPOSITORY -R $PWD/$REPOSITORY
    else
        hg clone https://$USERNAME:$PASSWORD@bitbucket.org/lightitcr/$REPOSITORY -R $PWD/$REPOSITORY
    fi
done;
