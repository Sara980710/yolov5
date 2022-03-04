# Master thesis yolov5

[YOLOv5 repo](https://github.com/ultralytics/yolov5)

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

## Train or preprocessing in a docker image
Start the image in you rengine using the uploaded image (don't forget the version number) and use following mounted folders:
* Your dataset --> data/
* Folder where you save the results --> project/

When you have started the image, go to the desired repo and clone this repo
````bash
git clone https://github.com/Sara980710/yolov5
````
Use [Tmux](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) to be able to connect to the terminal if your account is logged out from Aiqu. [Cheat sheet for Tmux](https://tmuxcheatsheet.com/)

Follow the instructions in the [preprocessing directory](https://github.com/Sara980710/yolov5/tree/main/preprocessing).

  OR
  
Follow the instructions in the [train directory](https://github.com/Sara980710/yolov5/tree/main/train). 

### Run the Docker image -locally
Test the image locally on your desktop. 

Change the settings in "train/run_locally.sh" and "main.py" for your fit, then use:

````bash
cd scripts
sh run.sh
````

## Inference
````bash
python3 yolov5/yolov5/detect.py --weights best.pt --img 768 --source dataset/test_v2/ --project dataset/
````

