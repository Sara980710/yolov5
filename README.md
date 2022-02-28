# Master thesis yolov5

[YOLOv5 repo](https://github.com/ultralytics/yolov5)

[Convert YOLOv5 to TF Lite](https://www.codeproject.com/Articles/5293077/Converting-YOLOv5-PyTorch-Model-Weights-to-TensorF)

[Inference TF Lite](https://www.tensorflow.org/lite/guide/inference)

## Prerequisites
This demo is using Linux, Ubuntu 20.04.

## Build own Docker image locally (and upload in Docker Hub)
Write your Dockerfile in preprocessing, train or predict folder. If use the same image-name as the repository in your [Docker Hub](https://hub.docker.com/) "user/repo:tag", ex. "sara980710/yolov5_train:v1.0". 
````bash
cd build
sh build.sh
````
To upload image to access remotely, create a login in [Docker Hub](https://hub.docker.com/). 
Login locally [instructions](https://docs.docker.com/engine/reference/commandline/login/).

Create a repository with the same name as your image (without version number), ex. "sara980710/yolov5_env". 

Use the following command to upload the image:
````bash
docker push user/repo:tag
````

## Preprocessing in a docker image
Start the image in you rengine using the uploaded image (don't forget the version number) and use following mounted folders:
* Your dataset --> data/

When you have started the image, go to the desired repo and clone this repo
````bash
git clone https://github.com/Sara980710/yolov5
````
Bla bla bla...

## Train the model in a docker image
Start the image in you rengine using the uploaded image (don't forget the version number) and use following mounted folders:
* Your dataset --> data/
* Folder where you save the results --> project/

When you have started the image, go to the desired repo and clone this repo
````bash
git clone https://github.com/Sara980710/yolov5
````
Adjust parameters to fit your dataset in following files:
* models/yolov5n.yaml
* datadef/airbus_kaggle.yaml
* train/train_yolo.py

Start the training
````bash
cd train/
````
````bash
python3 train_yolo.py
````
The results will be written to 'runs/expX'where X is the training number. 

### Run the Docker image -locally
Test the image locally on your desktop. 

Change the settings in "train/run_locally.sh" and "main.py" for your fit, then use:

````bash
cd scripts
sh rund.sh
````
