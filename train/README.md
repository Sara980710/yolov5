# Train model 

Adjust parameters to fit your dataset in following files:
* models/yolov5n.yaml - To change the model structure
* datadef/airbus_kaggle.yaml - To change the paths to your .txt files for data
* train/train_yolo.py - Other settings in the training

Clone the original yolov5 repo
````bash
cd yolov5/
git clone https://github.com/ultralytics/yolov5.git
````
Start the training
````bash
python3 train/train_yolo.py
````
