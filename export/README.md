# Export model 

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
or
````bash
cd yolov5/
python export.py --weights /home/sara/Desktop/Master-thesis/best.pt --include onnx
````

Aiqu:
````bash
cd yolov5/
python export.py --weights /project/yolo_results/exp/weights/best.pt --include tflite
````
````bash
cd yolov5/
python export.py --weights /project/yolo_results/exp/weights/best.pt --include onnx
````

