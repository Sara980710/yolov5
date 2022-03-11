# Export model 

Clone the original yolov5 repo
````bash
cd yolov5/
git clone https://github.com/ultralytics/yolov5.git
````
Export ussing export.py

````bash
cd yolov5/
python export.py --weights /home/sara/Desktop/Master-thesis/best.pt --include tflite --imgsz 768, 768 
````
or
````bash
cd yolov5/
python export.py --weights /home/sara/Desktop/Master-thesis/best.pt --include onnx --imgsz 768, 768 
````

Aiqu:
````bash
cd yolov5/
python3 export.py --weights /project/yolo_results/exp/weights/best.pt --include tflite --imgsz 768, 768 
````
````bash
cd yolov5/
python3 export.py --weights /project/yolo_results/exp/weights/best.pt --include onnx --imgsz 768, 768 
````

````bash
python3 detect.py --weights /project/yolo_results/exp/weights/best-fp16.tflite --img 768 --source /data/test_v2/ --project /project/yolo_results/
````
