#!/bin/bash
set -ev

TARGET_IMAGE="${DOCKER_USERNAME}/${DOCKER_REPO}"
TARGET_IMAGE_LATEST="${TARGET_IMAGE}:latest"
TARGET_IMAGE_VERSIONED="${TARGET_IMAGE}:${TRAVIS_COMMIT}"
HEROKU_APP_REGISTRY_URL="registry.heroku.com/${HEROKU_APP_NAME}/web"

# Push to Docker Hub

docker login --username $DOCKER_USERNAME --password $DOCKER_PASSWORD
docker build \
 --target production \
 --tag ${TARGET_IMAGE_LATEST} \
 --tag ${TARGET_IMAGE_VERSIONED} .
docker push ${TARGET_IMAGE_LATEST}
docker push ${TARGET_IMAGE_VERSIONED}

# Push to Heroku Registry

echo $HEROKU_AUTH_TOKEN | docker login --username=_ --password-stdin registry.heroku.com
docker pull $TARGET_IMAGE
docker tag $TARGET_IMAGE $HEROKU_APP_REGISTRY_URL
docker push $HEROKU_APP_REGISTRY_URL

# Release
curl https://cli-assets.heroku.com/install.sh | sh
heroku container:release web --app=$HEROKU_APP_NAME