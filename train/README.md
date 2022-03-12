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
#### Use Weights and Biases
````bash
wandb login
````
use your token from your project to connect

### Start the training
* batch_size: -1 gives AutoBatch (only for one GPU)
#### Using one GPU:
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
#### Using one GPU Aiqu:
````bash
python3 yolov5/train.py --imgsz 768 --epochs 300 --batch-size 64 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights yolov5n.pt --project /project/yolo_results --device 0 --save-period 1 
````
If you want to resume a run use --resume /project/yolo_results/exp13/weights/best.pt

#### Using multiple (ex. 2) GUP:s Aiqu:
[From documentation](https://docs.ultralytics.com/tutorials/multi-gpu-training/)
nproc_per_node is number of cores.
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 300 --batch-size 256 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights yolov5n.pt --project /project/yolo_results --device 0,1 --save-period 10 --cache
````
resume training (you can chane nr epochs in opt.yaml in the exp-folder)
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --device 0,1 --save-period 10 --cache --resume /project/yolo_results/exp13/weights/best.pt
````

## Batch size
https://github.com/ultralytics/yolov5/issues/2377

## Trained so far...
| Epochs  | Batch size | workers | exp | job ID | GPUs | pretrained weights | wandb |
| ------ | --------- | ------ | ----------- | ---- | ------ | --| -- |
| 81  | 256  | 16 | 16 | 306 | 2 | yolov5n | solar-wind-2 |
| 82  | 256  | 16 | 17 | 309 | 2 | no | iconic-bee-4 |
| 81  | 256  | 16 | 1 | 348 | 2 | yolov5s | legendary-wood-5 |

# Validation
* --task, 'train, val, test, speed or study'
````bash
python3 yolov5/val.py --imgsz 768 --batch-size 1 --data datadef/airbus_kaggle_aiqu.yaml --weights /project/yolo_results/exp16/weights/best.pt --project /project/yolo_results_test --device 0 --task test --save-txt
````

## test for 28884 images and 12416 labels
| exp | training  | Batch size  | GPUs | P | R | mAP@.5 | mAP@.5:.95 | Speed |
| --- | --------- | ----------  | ---- | - | - | ------ | ---------- | ----- |
| 3   | 16/epoch52 | 256   | 2 | 0.767 | 0.661 | 0.711 | 0.442 |  0.1ms pre-process, 0.9ms inference, 0.6ms NMS per image at shape (256, 3, 768, 768) |
| 4   | 17/best  | 256   | 2 | 0.755 | 0.63  | 0.683 | 0.425 |  0.1ms pre-process, 0.9ms inference, 0.5ms NMS per image at shape (256, 3, 768, 768) |
| 1   | 16/epoch52  | 1     | 1 | 0.755 | 0.63  | 0.683 | 0.425 |  0.2ms pre-process, 7.2ms inference, 0.6ms NMS per image at shape (1, 3, 768, 768) |
| 7   | 17/last  | 1     | 1 | 0.766 | 0.622 | 0.683 | 0.425 |  0.2ms pre-process, 7.2ms inference, 0.6ms NMS per image at shape (1, 3, 768, 768) |??
