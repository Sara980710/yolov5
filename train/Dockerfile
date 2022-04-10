FROM nvcr.io/nvidia/pytorch:21.03-py3

# Install linux packages
RUN apt update && apt install -y zip tmux libgl1-mesa-glx 

# Install python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip uninstall -y nvidia-tensorboard nvidia-tensorboard-plugin-dlprof
RUN pip install --no-cache -r requirements.txt coremltools onnx gsutil notebook

WORKDIR /

# (workaround for skipping cache):
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache 
# Clone from github
RUN git clone https://github.com/Sara980710/yolov5 
WORKDIR /yolov5/ 

#RUN git clone https://github.com/wonbeomjang/yolov5-knowledge-distillation.git yolov5
#Or
RUN git clone -b v6.1 https://github.com/ultralytics/yolov5.git
COPY train.py yolov5/
COPY export.py yolov5/
COPY val.py yolov5/
COPY export_multiple.sh .

# login to wandb
COPY .netrc /root/