import argparse
import os
import pandas as pd
from IPython.display import clear_output, display
import numpy as np
import cv2

def calculate_mask(line, w_image, h_image, nr_pixels):
    if not pd.isna(line):
        # Create mask
        mask = np.zeros(nr_pixels, dtype="uint8")
        line = line.split(" ")
        pair = []
        for value in line:
            pair.append(int(value))
            if len(pair) == 2:
                start = pair[0]
                end = start + pair[1]
                mask[start:end] = 1
                pair = []
        mask = mask.reshape(h_image,w_image)
        mask = np.rot90(mask, k=1)
        mask = np.flip(mask, axis=0)
        return mask
    return None

def calculate_bounding_box(mask, w_image, h_image, mode=None):
    if mask is not None:
        # Create bounding box
        x,y,w,h = cv2.boundingRect(mask)
        centerx = int(x+(w/2))
        centery = int(y+(h/2))

        if mode == "percentage":
            centerx = centerx/w_image
            centery = centery/h_image
            w = w/w_image
            h = h/h_image

        return f"0 {centerx} {centery} {w} {h}"

    return None

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', type=str, help='path to your datasets (folder containing different datasets)')
    parser.add_argument('--source', type=str, help='folder name of your specific dataset (images should be stored in a subfolder here called images)')
    parser.add_argument('--width', type=int, help='the with of the images')
    parser.add_argument('--height', type=int, help='the height of the images')

    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt

def main(opt):
    w_image = opt.width
    h_image = opt.height
    nr_pixels = w_image*h_image

    # Get target and source directories
    dataset_folder = opt.datadir
    images_path = os.path.join(dataset_folder, opt.source)

    # Load csv-file
    dataset_csv = f"{dataset_folder}/train_ship_segmentations_v2.csv"

    df = pd.read_csv(dataset_csv)
    print("csv-file loaded:")
    print(df.head())

    # Start copying! 
    print("------------------------------------")
    print("Starting to create yolo labels...")
    max = df.shape[0]

    images_path = os.path.join(dataset_folder, opt.source, "images")
    labels_path = os.path.join(dataset_folder, opt.source, "labels")

    if not os.path.exists(labels_path):
        os.makedirs(labels_path)
        print(f"'{labels_path}' directory is created!")

    for index, row in df.iterrows():
        # Check if file exist
        path = os.path.join(images_path,row['ImageId'])
        if os.path.isfile(path):
        
            # Create txt
            path = f"{os.path.join(labels_path, row['ImageId'].strip('.jpg'))}.txt"
            file_object  = open(path, "a")

            # Create mask
            mask = calculate_mask(row["EncodedPixels"], w_image, h_image, nr_pixels)

            # Calculate bounding box
            line = calculate_bounding_box(mask, w_image, h_image, mode="percentage")
            
            if line is not None:
                file_object.write(f"{line} \n")

            file_object.close()

        # Print
        if index % 1000 == 0:
            clear_output()
            display(f"{index}/{max}")
            
    clear_output()
    display(f"{max}/{max}")
    print("DONE!")


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)