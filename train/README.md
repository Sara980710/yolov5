# Train model 

Adjust parameters to fit your dataset in following files:
* models/yolov5n.yaml - To change the model structure
* datadef/airbus_kaggle.yaml - To change the paths to your .txt files for data
* train/train_yolo.py - Other settings in the training

#### Clone the original yolov5 repo
````bash
cd yolov5/
git clone -b v6.1 https://github.com/ultralytics/yolov5.git
````
#### Start the training
* batch_size: -1 gives AutoBatch 
Using one GPU:
````bash
python3 yolov5/train.py \
--imgsz 768 \
--epochs 2 \
--batch_size 64 \
--cfg models/yolov5n.yaml \
--data datadef/airbus_kaggle.yaml \
--weights yolov5n.pt \
--project runs/train
````
Using one GPU Aiqu:
````bash
python3 yolov5/train.py --imgsz 768 --epochs 300 --batch-size 64 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights yolov5n.pt --project /project/yolo_results --device 0 --save-period 1 --resume /project/yolo_results/exp13/weights/best.pt
````
Using multiple (ex. 2) GUP:s Aiqu:
[From documentation](https://docs.ultralytics.com/tutorials/multi-gpu-training/)
nproc_per_node is number of cores.
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 300 --batch-size 128 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights yolov5n.pt --project /project/yolo_results --device 0,1 --save-period 1 --resume /project/yolo_results/exp13/weights/best.pt
````

## Batch size
https://github.com/ultralytics/yolov5/issues/2377

## Trained so far...
| Epochs  | Batch size | workers | memory usage | exp | job ID | GPUs |
| ------ | --------- | ------ | ----------- | ---- | ------ | - |
| 300  | 128  | 16 | approx.9G | 12 | 295 | 2 | 
