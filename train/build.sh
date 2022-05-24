#!/bin/bash

set -e

IMAGE_NAME="sara980710/yolov5_env:v4.3"
#IMAGE_NAME="sara980710/yolov5_testkd_env:v1.2"

docker build -f Dockerfile -t $IMAGE_NAME . 
