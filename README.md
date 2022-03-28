# Master's thesis - yolov5
&rarr;[Link to master's thesis repo](https://github.com/Sara980710/master_thesis)

[YOLOv5 repo](https://github.com/ultralytics/yolov5)

https://github.com/wonbeomjang/yolov5-knowledge-distillation

https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9731227

## Prerequisites
This demo is using Linux, Ubuntu 20.04.

## Build own Docker images locally (and upload in Docker Hub)
The Dockerfile in [preprocessing directory](https://github.com/Sara980710/yolov5/tree/main/preprocessing), [train directory](https://github.com/Sara980710/yolov5/tree/main/train) or [export directory](https://github.com/Sara980710/yolov5/tree/main/export) is used to instruct the building process of a docker image. Build the files using the instructions in the foleders respectively.   

## Setup docker container
Start the image in you rengine using the uploaded image (don't forget the version number) and use following mounted folders:
* Your dataset --> data/
* Folder where you save the results --> project/

Use [Tmux](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) to be able to connect to the terminal if your account is logged out from Aiqu. [Cheat sheet for Tmux](https://tmuxcheatsheet.com/)

## SSH to Aiqu
https://docs.aiqu.ai/include/user_docs/ports.html

