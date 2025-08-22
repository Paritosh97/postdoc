#!/bin/bash
set -e

IMAGE_NAME="ghcr.io/paritosh97/threestudio:latest"
TEMP_CONTAINER_NAME="threestudio_temp_container"

# Build the Docker image
docker build -t $IMAGE_NAME .

# Run the container in detached mode (no interactive)
docker run --name $TEMP_CONTAINER_NAME -d $IMAGE_NAME

# Optional: wait a few seconds if you need to ensure container startup
sleep 5

# Stop the running container
docker stop $TEMP_CONTAINER_NAME

# Commit the stopped container to the GHCR image tag
docker commit $TEMP_CONTAINER_NAME $IMAGE_NAME

# Remove the temporary container
docker rm $TEMP_CONTAINER_NAME

# Push the new image to GHCR
docker push $IMAGE_NAME
