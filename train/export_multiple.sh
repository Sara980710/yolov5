#!/bin/bash

arr=( "192" "384" "768" "1152" "1536" ) # Multiple of 32
weights="/project/yolo_results/exp16/weights/best.pt"
batch_sizes=( "2" "5" "10" "50" "100")


# Export float32
for item in "${arr[@]}"
do  
    for bs in "${batch_sizes[@]}"
    do  
    echo " "
    echo "---------------------------------------------------"
    echo "Running command: python3 yolov5/export.py --weights ${weights} --include tflite --imgsz ${item} --name ${item} --keep_f32 --batch_size ${bs}"
    python3 yolov5/export.py --weights $weights --include tflite --imgsz $item --name $item --keep_f32 --batch-size ${bs}
    done
done

# Export float16
for item in "${arr[@]}"
do  
    for bs in "${batch_sizes[@]}"
    do  
        echo " "
        echo "---------------------------------------------------"
        echo "python3 yolov5/export.py --weights ${weights} --include tflite --imgsz ${item} --name ${item} --batch_size ${bs}"
        python3 yolov5/export.py --weights $weights --include tflite --imgsz $item --name $item --batch-size ${bs}
    done
done

# Export int8
#for item in "${arr[@]}"
#do
#    echo " "
#    echo "---------------------------------------------------"
#    echo "python3 yolov5/export.py --weights ${weights} --include tflite --imgsz ${item} --name ${item} --int8 --data datadef/airbus_kaggle_aiqu.yaml"
#    python3 yolov5/export.py --weights $weights --include tflite --imgsz $item --name $item --int8 --data datadef/airbus_kaggle_aiqu.yaml
#done
