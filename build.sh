#!/bin/bash
docker rm user-database --force
docker rm mongo --force

docker network create dbnetwork
docker build -t user-database .
docker run -dp 80:80 --name user-database --network dbnetwork user-database 
docker run -dp 27017:27017 --name mongo --network dbnetwork mongo 