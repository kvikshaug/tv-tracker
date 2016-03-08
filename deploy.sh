#!/bin/bash

# Ensure css is compiled before creating the image
docker-compose run --rm builder sass --scss --update scss:css

IMAGE_NAME=${PWD##*/}_app
docker-compose build app
docker tag ${IMAGE_NAME} kvikshaug/tv.kvikshaug.no
docker tag ${IMAGE_NAME} eu.gcr.io/monkey-island-1227/tv.kvikshaug.no

gcloud docker push eu.gcr.io/monkey-island-1227/tv.kvikshaug.no

# can't use rolling-update with rw GCE PD
kubectl delete -f rc.yml -f cron/rc.yml
kubectl create -f rc.yml -f cron/rc.yml
