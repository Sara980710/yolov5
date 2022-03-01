#!/usr/bin/python3

from yolov5 import train

train.run(
    imgsz=768,
    epochs=2,
    batch_size=64,
    cfg="models/yolov5n.yaml",
    data="datadef/airbus_kaggle.yaml",
    weights="yolov5n.pt",
    project="runs/train",
   # workers=2,
)