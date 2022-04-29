#!/bin/bash

projects=( "exp34" "exp35" "exp36" )

echo "Validating following projects: ${projects[@]}"

# Start train sequence
for project in "${projects[@]}"; do
    echo "Starting validation on $project"
    python3 yolov5/val.py --imgsz 768 --batch-size 1 --data datadef/airbus_kaggle_aiqu.yaml --weights /project/yolo_results/$project/weights/epoch80.pt --project /project/yolo_results_test --device 0 --task test --save-txt --save-conf --save-info --save-result
done
