#!/bin/bash

set -u
set -e

KDOCKER_DIR=$(dirname $(realpath "$0"))
KITSUNE_DIR=$(realpath "$KDOCKER_DIR/../..")

# Check for docker
if ! which docker 2>/dev/null >&2; then
    echo 'You need to install Docker for this to work.'
    echo 'You can get it at http://www.docker.com/'
    exit 1
fi

# MariaDB
if docker inspect mariadb >/dev/null; then
    docker start mariadb > /dev/null
else
    docker run --detach --name mariadb tutum/mariadb:5.5
fi

# Kitsune
if docker inspect kitsune >/dev/null; then
    docker start kitsune > /dev/null
else
    docker run \
        --detach \
        --publish-all=true \
        --volume "${KITSUNE_DIR}":/kitsune \
        --name kitsune \
        --link mariadb:mariadb \
        local/kitsune
fi

BIND=$(docker port kitsune 8000)
echo "Kitsune is running on $BIND"
docker attach kitsune
