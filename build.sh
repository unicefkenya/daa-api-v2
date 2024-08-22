#/bin/bash
set -e
IMAGE=dockerhubusername/moekeapi
VERSION=v1.0.15
# python3 manage.py test
git push origin main
docker build -t $IMAGE:$VERSION .
docker tag  $IMAGE:$VERSION  $IMAGE:latest
docker push $IMAGE:$VERSION
