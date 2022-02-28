#!/bin/bash

set -e

IMAGE_NAME="sara980710/yolov5_env"

ROOT_DIR=$PWD
DATA_DIR=/home/erik/local/data/seabirds/datasets/2019/yolov5
SRC_DIR=/home/erik/git/package/yolov5

docker run --ipc=host -it --rm --runtime nvidia \
-v $ROOT_DIR:/app \
-v $DATA_DIR:/data \
-v $SRC_DIR:/src \
$IMAGE_NAME \
python3 main.py
