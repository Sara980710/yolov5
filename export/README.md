# Export model 

Adjust parameters to fit your dataset in following files:
* models/yolov5n.yaml - To change the model structure
* datadef/airbus_kaggle.yaml - To change the paths to your .txt files for data
* train/train_yolo.py - Other settings in the training

Clone the original yolov5 repo
````bash
cd yolov5/
git clone https://github.com/ultralytics/yolov5.git
````
Export ussing export.py

````bash
cd yolov5/
python export.py --weights /home/sara/Desktop/Master-thesis/best.pt --include tflite
````

Aiqu:
````bash
cd yolov5/
python export.py --weights/embedl_unibap_space_maie/yolo_results/exp/weights/best.pt --include tflite
````

