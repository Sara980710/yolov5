#!/bin/bash

set -e

IMAGE_NAME="sara980710/yolov5_train_env"

docker build -f Dockerfile -t $IMAGE_NAME .
