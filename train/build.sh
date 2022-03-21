#!/bin/bash

set -e

IMAGE_NAME="sara980710/yolov5_train_env:v1.1"

docker build --no-cache -f Dockerfile -t $IMAGE_NAME .
