#!/bin/zsh

set -e  # Exit on errors
set -x  # Print commands

# Resolve the full path to the directory this script is in
SCRIPT_DIR="${0:A:h}"
PROJECT_DIR="${SCRIPT_DIR}"

CONTAINER_NAME="ptm_test_container"

# Step 1: Start container in detached mode
docker run -dit --name "$CONTAINER_NAME" python:3.13-slim bash

# Step 2: Install dependencies inside the container
docker exec "$CONTAINER_NAME" apt-get update
docker exec "$CONTAINER_NAME" apt-get install -y git build-essential

# Step 3: Copy your project into the container
docker cp "$PROJECT_DIR" "$CONTAINER_NAME":/root/pytestmate

# Step 4: Install your project (with pip)
docker exec "$CONTAINER_NAME" bash -c "cd /root/pytestmate && pip install ."

# Step 5: Drop into interactive shell
docker exec -it "$CONTAINER_NAME" bash
