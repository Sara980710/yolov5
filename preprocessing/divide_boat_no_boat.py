import argparse
import os
import pandas as pd
import shutil
from IPython.display import clear_output, display

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', type=str, help='path to dataset')
    parser.add_argument('--source', type=str, help='folder name of source images')

    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt

def main(opt):
    # Get target and source directories
    dataset_folder = opt.datadir
    images_path = os.path.join(dataset_folder, opt.source)

    destination_path_boats = f"{dataset_folder}/only_boats_test/images/"
    destination_path_no_boats = f"{dataset_folder}/no_boats_test/images/"

    # Check if directory needs to be created
    tmp  = destination_path_boats.strip("images/")
    if not os.path.exists(tmp):
        os.makedirs(tmp)
        print(f"'{tmp}' directory is created!")
        tmp  = destination_path_no_boats.strip("images/")
    if not os.path.exists(tmp):
        os.makedirs(tmp)
        print(f"'{tmp}' directory is created!")
    if not os.path.exists(destination_path_boats):
        os.makedirs(destination_path_boats)
        print(f"'{destination_path_boats}' directory is created!")
    if not os.path.exists(destination_path_no_boats):
        os.makedirs(destination_path_no_boats)
        print(f"'{destination_path_no_boats}' directory is created!")

    # Load csv-file
    dataset_csv = f"{dataset_folder}/train_ship_segmentations_v2.csv"

    df = pd.read_csv(dataset_csv)
    print("csv-file loaded:")
    print(df.head())

    # Start copying! 
    print("------------------------------------")
    print("Starting to copy and divide files...")
    max = df.shape[0]

    nr_boats = 0
    nr_no_boats = 0

    for index, row in df.iterrows():
        mask = row["EncodedPixels"]

        img_path = os.path.join(images_path,row['ImageId'])
        img_path_boats = os.path.join(destination_path_boats,row['ImageId'])
        img_path_no_boats = os.path.join(destination_path_no_boats,row['ImageId'])

        # Check boat or not boat
        if os.path.isfile(img_path) and not pd.isna(mask) and not os.path.isfile(img_path_boats):
            shutil.copy(img_path, destination_path_boats)
            nr_boats += 1
        elif os.path.isfile(img_path)and pd.isna(mask) and not os.path.isfile(img_path_no_boats):
            shutil.copy(img_path, destination_path_no_boats)
            nr_no_boats += 1
        
        # Print
        if index % 1000 == 0:
            clear_output()
            display(f"{index}/{max}")
            display(f"Added number of boats: {nr_boats}")
            display(f"Added number of no boats: {nr_no_boats}")
            
    clear_output()
    display(f"{max}/{max}")
    display(f"Added number of boats: {nr_boats}")
    display(f"Added number of no boats: {nr_no_boats}")
    display("DONE!")

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)