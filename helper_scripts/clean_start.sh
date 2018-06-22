#!/bin/bash
# This file is intended to be used in case of docker problems. It stops and
# removes all docker containers, followed by a docker-compose up.

docker-compose rm -v -s -f
docker-compose up
