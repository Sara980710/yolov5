#!/bin/bash

BATCH_SIZE=$3
MODEL=$1
WEIGHTS=$2
ITERATIONS=$4

echo "training $ITERATIONS iterations on $MODEL with weights $WEIGHTS and batch size $BATCH_SIZE"

# Start train sequence
for i in $(eval echo "{1..$ITERATIONS}"); do
    echo "Starting training $i"
    python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 81 --batch-size $BATCH_SIZE --cfg $MODEL --data datadef/airbus_kaggle_aiqu.yaml --weights $WEIGHTS --project /project/yolo_results --device 0,1 --save-period 10 --cache
done
