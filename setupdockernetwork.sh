#!/bin/bash

NETWORK=ms_default

echo "Trying to create the network if it doesn't exist"

docker network inspect ${NETWORK} >/dev/null 2>&1 || \
    docker network create --driver bridge ${NETWORK}