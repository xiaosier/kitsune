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

echo "LINKING"
mkdir -p "$KDOCKER_DIR/context/requirements/"
cp -a "$KDOCKER_DIR/Dockerfile" "$KDOCKER_DIR/context/"
cp -a "$KITSUNE_DIR/package.json" "$KDOCKER_DIR/context/"
cp -a "$KITSUNE_DIR/requirements/compiled.txt" "$KDOCKER_DIR/context/requirements/"

echo "BUILDING"
docker build -t local/kitsune "$KDOCKER_DIR/context/"
