FROM nvcr.io/nvidia/pytorch:21.03-py3

# Install linux packages
RUN apt update && apt install -y tmux libgl1-mesa-glx 

# Install python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt

WORKDIR ../

# (workaround for skipping cache):
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache 
# Clone from github
RUN git clone https://github.com/Sara980710/yolov5 
WORKDIR ../yolov5/ 
RUN git clone -b v6.1 https://github.com/ultralytics/yolov5.git
COPY train.py yolov5/

# login to wandb
COPY .netrc /root/