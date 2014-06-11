#!/bin/bash

set -u
set -e

KDOCKER_DIR=$(dirname $(readlink -f "$0"))
KITSUNE_DIR=$(readlink -f "$KDOCKER_DIR/../..")

# Check for docker
if ! which docker 2>/dev/null >&2; then
    echo 'You need to install Docker for this to work.'
    echo 'You can get it at http://www.docker.com/'
    exit 1
fi

echo "BUILDING"
docker build -t $(whoami)/kitsune "$KDOCKER_DIR"
echo "RUNNING"
docker run -v "${KITSUNE_DIR}":/kitsune $(whoami)/kitsune "$@"
