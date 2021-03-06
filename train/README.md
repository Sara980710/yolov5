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

````bash
docker run --shm-size=1g  -it  -v /home/sara/Documents/Master-thesis/dataset/only_boats:/example_data sara980710/yolov5_env:v2.8
````
CPU: 
````bash
python3 yolov5/train.py --imgsz 768 --epochs 3 --batch-size 16 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle.yaml --weights train/weights/yolov5n.pt --project /project/yolo_results --device cpu --workers 1
````
Knowledge distillation: Feature imitation
````bash
python3 yolov5/train.py --imgsz 768 --epochs 3 --batch-size 16 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle.yaml --weights train/weights/yolov5n.pt --project /project/yolo_results --device cpu --workers 1 --kd_weights train/weights/yolov5s.pt --kd_factor 0.01 --kd_warmup 400 --kd_feature_map [1,1,1,1] --kd_use_anchors [1,1,1]
````
Knowledge distillation: Hard labels
````bash
python3 yolov5/train.py --imgsz 768 --epochs 3 --batch-size 16 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle.yaml --weights train/weights/yolov5n.pt --project /project/yolo_results --device cpu --workers 1 --kd_weights train/weights/yolov5s.pt --kd_factor 0.01  --kd_hard_labels 
````
Knowledge distillation: Feature imitation (COCO dataset)
````bash
python3 yolov5/train.py --epochs 3 --batch-size 16 --cfg models/yolov5n.yaml --data coco.yaml --weights '' --project /project/yolo_results --device cpu --save-period 10 --kd_weights train/weights/yolov5l.pt --kd_factor 0.01 --kd_warmup 400 --kd_feature_map 2 --kd_use_anchors [1,1,1]
````
### Aiqu
One GPU:
````bash
python3 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 64 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights train/weights/yolov5n.pt --project /project/yolo_results --device 0 --save-period 1 
````

COCO one-GPU
````bash
cd yolov5/
python3 train.py --epochs 300 --batch-size 160 --cfg /yolov5/models/yolov5n.yaml --data coco.yaml --weights '' --project /project/yolo_results --device 0 --save-period 10
````

Multiple GUP:s [From documentation](https://docs.ultralytics.com/tutorials/multi-gpu-training/) (nproc_per_node is number of cores).
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 256 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights train/weights/yolov5n.pt --project /project/yolo_results --device 0,1 --save-period 10
````
COCO multi-GPU
````bash
cd yolov5/
python3 -m torch.distributed.launch --nproc_per_node 2 train.py --epochs 300 --batch-size 256 --cfg /yolov5/models/yolov5n.yaml --data coco.yaml --weights '' --project /project/yolo_results --device 0,1 --save-period 10
````

run multiple (important: use bash, read command line in case of instructions):
````bash
bash train_multiple.sh models/yolov5n.yaml train/weights/yolov5n.pt 256 3
````
Resume training (you can chane nr epochs in opt.yaml in the exp-folder):
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --device 0,1 --save-period 10 --resume /project/yolo_results/exp16/weights/best.pt
````

Knowledge distillation: Feature imitation - One core 
````bash
python3 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 64 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights train/weights/yolov5n.pt --project /project/yolo_results --device 0 --save-period 10 --kd_weights /project/yolo_results/exp39/weights/epoch80.pt --kd_factor 0.01 --kd_warmup 400 --kd_feature_map 2 --kd_use_anchors [1,1,1]
````
Knowledge distillation: Feature imitation (COCO dataset) - One core 
````bash
cd yolov5/
python3 train.py --epochs 81 --batch-size 160 --cfg /yolov5/models/yolov5n.yaml --data coco.yaml --weights '' --project /project/yolo_results --device 0 --save-period 10 --kd_weights /yolov5/train/weights/yolov5l.pt --kd_factor 0.01 --kd_warmup 400 --kd_feature_map [1,1,1,1] --kd_use_anchors [1,1,1]
````
Knowledge distillation: Soft labels - One core 
````bash
 python3 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 160 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights '' --project /project/yolo_results --device 0 --save-period 10 --kd_weights /project/yolo_results/exp40/weights/epoch80.pt --kd_factor 0.01  --kd_hard_labels
 ````
 
Knowledge distillation: Feature imitation - Two cores
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 256 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights train/weights/yolov5n.pt --project /project/yolo_results --device 0,1 --save-period 10 --kd_weights /project/yolo_results/exp40/weights/epoch80.pt --kd_factor 0.01 --kd_warmup 400 --kd_feature_map [1,1,1,1] --kd_use_anchors [1,1,1]
````
Knowledge distillation: Feature imitation (coco)- Two cores
````bash
cd yolov5/
python3 -m torch.distributed.launch --nproc_per_node 2 train.py --epochs 81 --batch-size 256 --cfg /yolov5/models/yolov5n.yaml --data coco.yaml --weights '' --project /project/yolo_results --device 0,1 --save-period 10  --kd_weights /yolov5/train/weights/yolov5l.pt --kd_factor 0.01 --kd_warmup 400 --kd_feature_map [0,1,0,0] --kd_use_anchors [1,1,1]
````
Knowledge distillation: Soft labels - Two cores
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 256 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights train/weights/yolov5n.pt --project /project/yolo_results --device 0,1 --save-period 10 --kd_weights /project/yolo_results/exp40/weights/epoch80.pt --kd_factor 0.01  --kd_hard_labels --kd_warmup 400
````
Knowledge distillation: Soft labels (coco)- Two cores
````bash
cd yolov5/
python3 -m torch.distributed.launch --nproc_per_node 2 train.py --epochs 81 --batch-size 256 --cfg /yolov5/models/yolov5n.yaml --data coco.yaml --weights '' --project /project/yolo_results --device 0,1 --save-period 10 --kd_weights /yolov5/train/weights/yolov5l.pt --kd_factor 0.01  --kd_hard_labels 1 --kd_warmup 400
````

Knowledge distillation: [wonbeomjang](https://github.com/wonbeomjang/yolov5-knowledge-distillation) - Two cores
````bash
python3 -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --imgsz 768 --epochs 81 --batch-size 256 --cfg models/yolov5n.yaml --data datadef/airbus_kaggle_aiqu.yaml --weights train/weights/yolov5n.pt --project /project/yolo_results --device 0,1 --save-period 10 --cache --teacher_weight /project/yolo_results/exp39/weights/epoch80.pt
````

## Validation
* --task, 'train, val, test, speed or study'
````bash
python3 yolov5/val.py --imgsz 768 --batch-size 1 --data datadef/airbus_kaggle_aiqu.yaml --weights /project/yolo_results/exp16/weights/epoch80.pt --project /project/yolo_results_test --device 0 --task test --save-txt --save-conf --save-info --save-result
````

# Export model 
Export ussing export.py

````bash
python yolov5/export.py --weights /home/sara/Documents/Master-thesis/yolov5/models/yolov5n.pt --include tflite --imgsz 768 --name 768 --batch-size 2
````

Aiqu:
````bash
python3 yolov5/export.py --weights /project/yolo_results/exp16/weights/best.pt --include tflite --imgsz 3360 --name 3360 --batch-size 2
````

## Export multiple input-sizes
Modify and run in docker image:
````bash
sh export_multiple.sh
````

# Inference 
## Using yolov5 repo
````bash
python3 yolov5/detect.py --weights /project/yolo_results/exp16/weights/epoch80-fp16.tflite --img 768 --source /data/test_v2/ --project /project/yolo_inference --device 0 --data datadef/airbus_kaggle.yaml
````
