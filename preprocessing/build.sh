#!/bin/bash

set -e

IMAGE_NAME="sara980710/yolov5_preprocessing_env:v1.1"

docker build -f Dockerfile -t $IMAGE_NAME .
