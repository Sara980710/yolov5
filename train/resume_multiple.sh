#!/bin/bash

projects=( "exp16" "exp17" "exp" "exp21" "exp24" "exp25" "exp27" "exp34" "exp35" "exp36" )

echo "resuming following projects: ${projects[@]}"

# Start train sequence
for project in "${projects[@]}"; do
    echo "Starting validation on $project"
    python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --device 0,1 --save-period 10 --cache --resume /project/yolo_results/$project/weights/best.pt
done

