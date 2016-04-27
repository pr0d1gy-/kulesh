#!/bin/bash


# ----------------------------------------------------------------------------


PWD=$(pwd)
TEAM_NAME='lightitcr'
MERCURIAL_REPOS=('celery-worker' 'client' 'server' 'scripts')

# ----------------------------------------------------------------------------

if [[ -f _saved_username ]];
then
    USERNAME=$(cat _saved_username)
    echo "Using saved username: $USERNAME"
else
    echo -n "Username: "
    read USERNAME
    echo $USERNAME > _saved_username
fi


if [[ -f _saved_fullname ]];
then
    FULLNAME=$(cat _saved_fullname)
    echo "Using saved full name: $FULLNAME"
else
    echo -n "Full name and email to display, e.g. John Doe <john@mail.com>: "
    read FULLNAME
    echo $FULLNAME > _saved_fullname
fi

SAVED_PASSWORD=""
if [[ ! -f _saved_password ]];
then
    echo -n "Password: "
    read -s PASSWORD
    echo ""

    echo -n "Save password? [N/y] "
    read IS_PASSWORD_SAVE
    if [[ $IS_PASSWORD_SAVE == "Y" || $IS_PASSWORD_SAVE == "y" ]];
    then
        echo $PASSWORD > _saved_password
        SAVED_PASSWORD=":$PASSWORD"
    fi
else
    PASSWORD=$(cat _saved_password)
    echo "Using saved password."
    SAVED_PASSWORD=":$PASSWORD"
fi


# ----------------------------------------------------------------------------



for REPOSITORY in ${MERCURIAL_REPOS[@]};
do

    HGRC="[paths]\ndefault = https://$USERNAME$SAVED_PASSWORD@bitbucket.org/$TEAM_NAME/$REPOSITORY\n\n"
    HGRC+="[ui]\nusername = $FULLNAME\n\n[extensions]\ncolor =\npurge =\n"

    if [[ -d $PWD/$REPOSITORY ]];
    then
        echo "$REPOSITORY folder was found."
        if [[ -d $PWD/$REPOSITORY/.hg ]];
        then
            echo "$REPOSITORY hg was found."
        else
            echo "$REPOSITORY hg was not found."
            echo "$REPOSITORY init hg..."
            hg init $PWD/$REPOSITORY
            echo -e "$HGRC" > "$PWD/$REPOSITORY/.hg/hgrc"
            echo "$REPOSITORY hg initiated."
        fi
        echo "$REPOSITORY pulling..."
        hg pull -u https://$USERNAME:$PASSWORD@bitbucket.org/$TEAM_NAME/$REPOSITORY -R $PWD/$REPOSITORY
        echo "$REPOSITORY pulled."
    else
        echo "$REPOSITORY folder was not found."
        echo "$REPOSITORY cloning..."
        hg clone https://$USERNAME:$PASSWORD@bitbucket.org/$TEAM_NAME/$REPOSITORY -R $PWD/$REPOSITORY
        echo "$REPOSITORY cloned."
        echo -e "$HGRC" > "$PWD/$REPOSITORY/.hg/hgrc"
    fi

done;
