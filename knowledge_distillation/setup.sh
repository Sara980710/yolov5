#!/bin/bash

git clone -b v6.1 https://github.com/ultralytics/yolov5.git;
cp -r knowledge_distillation/train.py yolov5/