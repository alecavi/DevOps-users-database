#!/bin/bash
docker build -t users-database .
docker run -dp 80:80 --name users-database users-database