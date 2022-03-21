#!/bin/bash

git clone https://github.com/Sara980710/yolov5;
cd yolov5;
git clone -b v6.1 https://github.com/ultralytics/yolov5.git;
cp -r knowledge_distillation/train.py yolov5/