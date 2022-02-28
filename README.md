# Master thesis yolov5

[YOLOv5 repo](https://github.com/ultralytics/yolov5)

[Convert YOLOv5 to TF Lite](https://www.codeproject.com/Articles/5293077/Converting-YOLOv5-PyTorch-Model-Weights-to-TensorF)

[Inference TF Lite](https://www.tensorflow.org/lite/guide/inference)

## Prerequisites
This demo is using Linux, Ubuntu 20.04.

## Train the model in docker image
Go to the desired repo and clone this repo
````bash
git clone 
````
First time you would need to clone the source code, see below :triangular_flag_on_post:.

Start the training with
````bash
python3 main.py
````
The results will be written to 'runs/expX'.

Before launching the main.py script you might also like to adjust the parameters in [main.py](./main.py).

### :triangular_flag_on_post: Clone the source code
Clone the AI Sweden startup kit:
````bash
git clone https://github.com/aidotse/startupkit-DF.git
cd startupkit-DF/aiqu/seabird
````

Clone the yolov5 code:
````bash
git clone https://github.com/ultralytics/yolov5.git
````

## Build the Docker image and push your image
This step is not strictly necessary. A prebuilt model, 'eriksaidotse/yolov5_v6.0_env', is all ready available on Docker Hub, and also downloaded to the DGX.

However a good exercise would be to build and upload your own model.

````bash
cd build
sh build.sh
````
Finally, upload the image to your [Docker Hub](https://hub.docker.com/) account.

## Run the Docker image -locally
:carousel_horse: Note that this step is only if would like to run the demo outside AiQu, for example, locally on your desktop. 

Fist make appropriate adjustments in the [scrips/run.sh](./scripts/run.sh) file, for example, set your path to the data. Also make sure that the paths in [guillemots.yaml](./datadef/guillemots.yaml) make sense.

Finally, perhaps adjust the parameters in [main.py](./main.py).

````bash
cd scripts
sh rund.sh
````