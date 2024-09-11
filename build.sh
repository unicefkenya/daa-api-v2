#/bin/bash
set -e
IMAGE=dockerhubusername/moekeapi
VERSION=v1.0.1
# python3 manage.py test
git push origin main
docker build -t $IMAGE:$VERSION . --platform=linux/arm64
docker tag  $IMAGE:$VERSION  $IMAGE:latest
docker push $IMAGE:$VERSION
