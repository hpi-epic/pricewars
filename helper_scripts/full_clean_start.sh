#!/bin/bash
# This file is intended to be used in case of severe docker problems. It stops
# and removes all docker containers, rebuilds them and executes docker-compose up
# (leading to a time consuming rebuild).

docker-compose rm -v -s -f
docker-compose up --build
