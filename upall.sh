#!/bin/bash


# ----------------------------------------------------------------------------

SUDO=sudo
sudo true
PWD=$(pwd)

# ----------------------------------------------------------------------------

$SUDO chmod "+x" "$PWD/scripts/up.sh"
$SUDO chmod "+x" "$PWD/scripts/update_repositories.sh"

$PWD/scripts/update_repositories.sh
$PWD/scripts/up.sh
