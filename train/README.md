# Train model 

Adjust parameters to fit your dataset in following files:
* models/yolov5n.yaml - To change the model structure
* datadef/airbus_kaggle.yaml - To change the paths to your .txt files for data
* train/train_yolo.py - Other settings in the training

## Setup docker image
Goto train directory and make sure to check following:
- ".netrc": change password to your wandb API token found in [account settings](https://wandb.ai/settings)
- "build.sh": change the image name and tag to your desired one
````bash
sh build.sh
````
## Upload to Docker Hub (required for access remotely)
To upload image to access remotely, create a login in [Docker Hub](https://hub.docker.com/). 
Login locally [instructions](https://docs.docker.com/engine/reference/commandline/login/).

Use the following command to upload the image:
````bash
docker push user/repo:tag
````

## Start the training
* batch_size: -1 gives AutoBatch (only for one GPU)
* data: path to dataset configuration file (yaml)
* device:  '0' for one GPU or '0,1,2,3' for multiple gpus or 'cpu'
### Test training locally
CPU: 
````bash
docker run --shm-size=1g  -it  -v /home/sara/Documents/Master-thesis/dataset/only_boats:/example_data sara980710/yolov5_kd_env:v1.0
````
````bash
python3 yolov5/train.py --imgsz 768 --epochs 3 --batch-size 16 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle.yaml --weights yolov5n.pt --project /project/yolo_results --device cpu --workers 1
````

train with knowledge distillation:
````bash
python3 yolov5/train.py --imgsz 768 --epochs 3 --batch-size 16 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle.yaml --weights yolov5n.pt --project /project/yolo_results --device cpu --workers 1 --kd_weights yolov5s.pt
````
### Aiqu
One GPU:
````bash
python3 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 64 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights yolov5n.pt --project /project/yolo_results --device 0 --save-period 1 
````
Multiple GUP:s [From documentation](https://docs.ultralytics.com/tutorials/multi-gpu-training/) (nproc_per_node is number of cores).
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 256 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights yolov5n.pt --project /project/yolo_results --device 0,1 --save-period 10 --cache
````
resume training (you can chane nr epochs in opt.yaml in the exp-folder):
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --device 0,1 --save-period 10 --cache --resume /project/yolo_results/exp16/weights/best.pt
````
train with knowledge distillation:
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 256 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights yolov5n.pt --project /project/yolo_results --device 0,1 --save-period 10 --cache --kd_weights /project/yolo_results/exp/weights/epoch80.pt
````

## Batch size
https://github.com/ultralytics/yolov5/issues/2377

## Results 
### Models
- yolov5n.pt: 270 layers, 1765270 parameters, 1765270 gradients, 4.2 GFLOPs
- yolov5n.pt: 270 layers, 7022326 parameters, 7022326 gradients, 15.8 GFLOPs
- yolov5l.pt: 468 layers, 46138294 parameters, 46138294 gradients, 107.9 GFLOPs

### Trained so far...
| Epochs  | Batch size | workers | exp | GPUs | pretrained weights | wandb |
| ------ | --------- | ------ | ---- | ------ | --| -- |
| 81  | 256  | 16 | 16  | 2 | yolov5n | solar-wind-2 |
| 82  | 256  | 16 | 17  | 2 | no | iconic-bee-4 |
| 81  | 256  | 16 | 1  | 2 | yolov5s | legendary-wood-5 |
| 80  | 100  | 16 | 21  | 2 | yolov5l | jumping-shape-11 |
| 82  | 256  | 16 | 24  | 2 | no | scarlet-bee-25 |
| 80  | 256  | 16 | 25  | 2 | yolov5n | twilight-sponge-26 |

## Validation
* --task, 'train, val, test, speed or study'
````bash
python3 yolov5/val.py --imgsz 768 --batch-size 1 --data datadef/airbus_kaggle_aiqu.yaml --weights /project/yolo_results/exp16/weights/best.pt --project /project/yolo_results_test --device 0 --task test --save-txt
````

### test for 28884 images and 12416 labels
| exp | training   | Batch size  | GPUs | P | R | mAP@.5 | mAP@.5:.95 | Speed |
| --- | ---------- | ----------  | ---- | - | - | ------ | ---------- | ----- |
| 11  | 16/epoch80 | 1     | 1 | 0.787 | 0.653 | 0.716 | 0.447 |  0.3ms pre-process, 7.1ms inference, 0.6ms NMS per image at shape (1, 3, 768, 768) |
| 12  | 1/epoch80  | 1     | 1 | 0.787 | 0.702 | 0.76 | 0.489 |  0.3ms pre-process, 8.1ms inference, 0.6ms NMS per image at shape (1, 3, 768, 768) |
| 15  | 16/epoch80-fp16.tflite  | 1     | 1 | 0.781 | 0.654 | 0.71 | 0.439 |  15.8ms pre-process, 198.9ms inference, 48.1ms NMS per image at shape (1, 3, 768, 768) |
| 17  | 24/epoch80 | 256 | 2 | 0.783 | 0.666 | 0.731  | 0.467 | 0.1ms pre-process, 0.9ms inference, 0.5ms NMS per image at shape (256, 3, 768, 768) |
| 16 | 24/epoch80 | 1 | 1 | 0.796 | 0.657 | 0.731  | 0.467 | 0.3ms pre-process, 7.1ms inference, 0.6ms NMS per image at shape (1, 3, 768, 768) |

                  

# Export model 
Export ussing export.py

````bash
python yolov5/export.py --weights /home/sara/Documents/Master-thesis/yolov5/models/yolov5n.pt --include tflite --imgsz 768
````
or
````bash
cd yolov5/
python export.py --weights /home/sara/Desktop/Master-thesis/best.pt --include onnx --imgsz 768
````

Aiqu:
````bash
python3 yolov5/export.py --weights /project/yolo_results/exp/weights/best.pt --include tflite --imgsz 768 --name somename
````
````bash
python3 export.py --weights /project/yolo_results/exp/weights/best.pt --include onnx --imgsz 768
````

# Inference 
## Using yolov5 repo
````bash
python3 yolov5/detect.py --weights /project/yolo_results/exp16/weights/epoch80-fp16.tflite --img 768 --source /data/test_v2/ --project /project/yolo_inference --device 0 --data datadef/airbus_kaggle.yaml
````
