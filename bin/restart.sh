#!/bin/bash

docker-compose down -v
docker rmi snowcap-app
docker rmi snowcap-worker
docker-compose up -d 