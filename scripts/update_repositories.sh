#!/bin/bash


# ----------------------------------------------------------------------------


PWD=$(pwd)
TEAM_NAME='lightitcr'
MERCURIAL_REPOS=('celery-worker' 'client' 'server' 'scripts')

# ----------------------------------------------------------------------------

if [[ -f  _saved_username ]]; then
  USERNAME=$(cat _saved_username)
  echo "Using saved username: $USERNAME"
else
  echo -n "Username: "
  read USERNAME
  echo $USERNAME > _saved_username
fi


if [[ -f  _saved_fullname ]]; then
  FULLNAME=$(cat _saved_fullname)
  echo "Using saved full name: $FULLNAME"
else
  echo -n "Full name and email to display, e.g. John Doe <john@coolbet.com>: "
  read FULLNAME
  echo $FULLNAME > _saved_fullname
fi

echo -n "Password: "
read -s PASSWORD

# ----------------------------------------------------------------------------

for REPOSITORY in ${MERCURIAL_REPOS[@]};
do
    if [[ -d $PWD/$REPOSITORY ]];
    then
        hg pull -u https://$USERNAME:$PASSWORD@bitbucket.org/$TEAM_NAME/$REPOSITORY -R $PWD/$REPOSITORY
    else
        hg clone https://$USERNAME:$PASSWORD@bitbucket.org/$TEAM_NAME/$REPOSITORY -R $PWD/$REPOSITORY
    fi

    # Setup Mercurial.
    echo "[paths]
default = https://$USERNAME@bitbucket.org/$TEAM_NAME/$REPOSITORY

[ui]
username = $FULLNAME

[extensions]
color =
purge =
" > "$PWD/$REPOSITORY/.hg/hgrc2"

done;
