FROM nvcr.io/nvidia/pytorch:21.03-py3

# Install linux packages
RUN apt update && apt install -y tmux

# Install python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt

WORKDIR ../

# Clone from github
RUN git clone https://github.com/Sara980710/yolov5 
WORKDIR ../yolov5/