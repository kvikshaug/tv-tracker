#!/bin/bash
docker build -t eu.gcr.io/monkey-island-1227/tv.kvikshaug.no .
gcloud docker push eu.gcr.io/monkey-island-1227/tv.kvikshaug.no

# can't use rolling-update with rw GCE PD
kubectl delete -f rc.yml
kubectl create -f rc.yml
