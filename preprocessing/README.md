# Preprocessing data

## Convert from Kaggle Airbus data to YOLOv5 format using convert.py
Make sure that your data is in a directory with the files in following structure
````
datasetdir/
|
|__specific_dataset/
|   |__images/
|       |__my_image.jpg
|       |__...
|
|__train_ship_segmentations_v2.csv
````

Use the convert.py script with following arguments:
* datadir - path to your datasets (folder containing different datasets)
* source - folder name of your specific dataset (images should be stored in a subfolder here called images)
* width - of the images
* height - of the images

An example how to run convert.py in the terminal:
````bash
python3 preprocessing/convert.py --datadir /home/sara/Desktop/Master-thesis/dataset/ --source train --width 768 --height 768
````
In Aiqu:
````bash
python3 preprocessing/convert.py --datadir /data/ --source train --width 768 --height 768
````
The output will then consist of a .txt-file for each image in a folder called labels:
````
datasetdir/
|
|__specific_dataset/
|   |__images/
|   |   |__my_image.jpg
|   |   |__...
|   |
|   |__labels/
|       |__my_image.txt
|       |__...
|
|__train_ship_segmentations_v2.csv
````

## Divide dataset into train, test and validation
Use the divide.py script with following arguments:
* datadir - directory to your downloaded dataset
* yolodir - directory to this yolo-repo
* source - the folder name of the images (or the path from datadir to images folder)
* name - what you would like to name this collection of images

An example how to run convert.py in the terminal:
````bash
python3 preprocessing/divide.py --datadir /home/sara/Desktop/Master-thesis/dataset/ --yolodir /home/sara/Desktop/Master-thesis/yolov5 --source train/images --name test
````
Output will be in the yolo directory as .txt-files:
````
yolodir/
|
|__datasets/
|   |__test_all.txt
|   |__test_train.txt
|   |__test_val.txt
|   |__test_test.txt
|
|__...
````

## Divide the dataset into boats/no boats
Use the divide_boat_no_boat.py script with following arguments:
* datadir - directory to your downloaded dataset
* source - the folder name of the images (or the path from datadir to images folder)

An example how to run convert.py in the terminal:
````bash
python3 preprocessing/divide_boat_no_boat.py --datadir /home/sara/Desktop/Master-thesis/dataset/ --source train_v2/images
````
The output will be two new folders with sub-folders "boats/images/" and "no_boats/images/" where respectively image is copied to. 

