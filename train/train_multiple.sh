#!/bin/bash

BATCH_SIZE=256 
MODEL="models/yolov5n.yaml" 
WEIGHTS="train/weights/yolov5n.pt" 
ITERATIONS=5

CACHE_TRAINS="/project/yolo_results/trains.cache"
CACHE_DONE="/project/yolo_results/done.cache"

# If training should continue
if test -f "$CACHE_TRAINS"; then
    echo "Found cache file: $CACHE_TRAINS."
    CACHE_TRAINS_EXIST=true
else
    echo "Cache file not found: $CACHE_TRAINS."
    CACHE_TRAINS_EXIST=false
fi
if test -f "$CACHE_DONE"; then
    echo "Found cache file: $CACHE_DONE."
    CACHE_DONE_EXIST=true
else
    echo "Cache file not found: $CACHE_DONE. "
    CACHE_DONE_EXIST=false
fi

# Check if resume is needed
if $CACHE_TRAINS_EXIST && $CACHE_DONE_EXIST; then
    IFS=$'\n' read -d '' -r -a TRAININGS < $CACHE_TRAINS
    IFS=$'\n' read -d '' -r -a DONE < $CACHE_DONE
    NR_STARTED=${#TRAININGS[@]}
    NR_DONE=${#DONE[@]}
    echo "Number of started trainings: $NR_STARTED"
    echo "Number of finished trainings: $NR_DONE"
    echo "Number of targeted iterations: $ITERATIONS"

    if test $NR_DONE -lt $NR_STARTED; then
        if [ $# -eq 0 ]
        then
            echo "Please add exp number to resume to the argument"
            exit
        fi
        echo "Resuming a training of: $1"
        python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --device 0,1 --save-period 10 --cache --resume /project/yolo_results/exp$1/weights/best.pt
        echo "$NR_STARTED" >> done.cache
    fi
    IFS=$'\n' read -d '' -r -a TRAININGS < $CACHE_TRAINS
    IFS=$'\n' read -d '' -r -a DONE < $CACHE_DONE
    NR_STARTED=${#TRAININGS[@]}
    NR_DONE=${#DONE[@]}
    let START=NR_STARTED+1
else
    echo "Starting the sequence of trainings from the beginning..."
    NR_DONE=0
    START=1
fi

# Start train sequence
if test $NR_DONE -lt $ITERATIONS; then 
    for i in $(eval echo "{$START..$ITERATIONS}"); do
        echo "Starting training $i"
        echo "$i" >> trains.cache
        python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 81 --batch-size $BATCH_SIZE --cfg $MODEL --data datadef/airbus_kaggle_aiqu.yaml --weights $WEIGHTS --project /project/yolo_results --device 0,1 --save-period 10 --cache
        echo "$i" >> done.cache
    done
fi