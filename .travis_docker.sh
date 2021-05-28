#!/bin/bash
set -ev

TARGET_IMAGE="${DOCKER_USERNAME}/${DOCKER_REPO}"
TARGET_IMAGE_LATEST="${TARGET_IMAGE}:latest"
TARGET_IMAGE_VERSIONED="${TARGET_IMAGE}:${TRAVIS_COMMIT}"

# Push to Docker Hub

docker login --username $DOCKER_USERNAME --password $DOCKER_PASSWORD
docker build \
 --target production \
 --tag ${TARGET_IMAGE_LATEST} \
 --tag ${TARGET_IMAGE_VERSIONED} .
docker push ${TARGET_IMAGE_LATEST}
docker push ${TARGET_IMAGE_VERSIONED}

# POST to Deploy Webhook

WEBHOOK_URL=$(terraform output cd_webhook)
curl -dH -X POST "${WEBHOOK_URL}"