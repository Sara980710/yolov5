# Preprocessing data

Test locally by starting docker container:
````bash
docker run -it sara980710/yolov5_kd_env:v1.0
````


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
* datadir - path to you datasets (folder containing different datasets)
* source - folder name of source images (NOTE! images are directly stored in this folder)
* savedir - path to where you want to save the txt-files
* trainsize - size of the training-set in percent
* valsize - size of the validation-set in percent

* name - what you would like to name this collection of images

An example how to run convert.py in the terminal:
````bash
python3 preprocessing/divide.py --datadir /home/sara/Documents/Master-thesis/dataset/ --source train/images --savedir /home/sara/Documents/Master-thesis/yolov5/datasets/ --trainsize 0.7 --valsize 0.15 --name test
````
In Aiqu:
````bash
cd yolov5
python3 preprocessing/divide.py --datadir /data/ --source train/images --savedir /project/datasets/  --name div
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
* sourcedir - path to the folder containing images
* csv - your csv file (path)
* destdir - folder where no_boat/boat directory is saved

An example how to run convert.py in the terminal:
````bash
python3 preprocessing/divide_boat_no_boat.py --sourcedir /home/sara/Desktop/Master-thesis/dataset/images/ --csv /home/sara/Desktop/Master-thesis/dataset/train_ship_segmentations_v2.csv --destdir /home/sara/Desktop/Master-thesis/dataset/
````
The output will be two new folders with "boats/" and "no_boats/" where respectively image is copied to. 

