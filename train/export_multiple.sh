#!/bin/bash

arr=( "32" "192" "384" "768" "1152" "1536" ) # Multiple of 32
weights="/project/yolo_results/exp16/weights/best.pt"


# Export float32
for item in "${arr[@]}"
do  
    echo " "
    echo "---------------------------------------------------"
    echo "Running command: python3 yolov5/export.py --weights ${weights} --include tflite --imgsz ${item} --name ${item} --keep_f32"
    python3 yolov5/export.py --weights $weights --include tflite --imgsz $item --name $item --keep_f32
done

# Export float16
for item in "${arr[@]}"
do  
    echo " "
    echo "---------------------------------------------------"
    echo "python3 yolov5/export.py --weights ${weights} --include tflite --imgsz ${item} --name ${item}"
    python3 yolov5/export.py --weights $weights --include tflite --imgsz $item --name $item
done

# Export int8
for item in "${arr[@]}"
do
    echo " "
    echo "---------------------------------------------------"
    echo "python3 yolov5/export.py --weights ${weights} --include tflite --imgsz ${item} --name ${item} --int8 --data datadef/airbus_kaggle_aiqu.yaml"
    python3 yolov5/export.py --weights $weights --include tflite --imgsz $item --name $item --int8 --data datadef/airbus_kaggle_aiqu.yaml
done
