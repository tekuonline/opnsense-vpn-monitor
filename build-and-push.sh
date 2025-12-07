#!/bin/bash

# Build and Push Script for OPNsense VPN Monitor
# Usage: ./build-and-push.sh [tag]

set -e

# Default tag is latest
TAG=${1:-latest}

# Get repository name from git
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
USERNAME=${DOCKER_USERNAME:-$(whoami)}

echo "Building and pushing $USERNAME/$REPO_NAME:$TAG"

# Build for multiple platforms
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag $USERNAME/$REPO_NAME:$TAG \
    --tag $USERNAME/$REPO_NAME:latest \
    --push \
    .

echo "Successfully built and pushed $USERNAME/$REPO_NAME:$TAG"