import argparse
import os
import pandas as pd
import shutil
from IPython.display import clear_output, display

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--sourcedir', type=str, help='path to the folder containing images')
    parser.add_argument('--csv', type=str, help='your csv file (path)')
    parser.add_argument('--destdir', type=str, help='folder where no_boat/boat directory is saved')

    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt

def main(opt):
    # Get target and source directories
    images_path = opt.sourcedir

    destination_path_boats = f"{opt.destdir}/boats/"
    destination_path_no_boats = f"{opt.destdir}/no_boats/"

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
    dataset_csv = f"opt.csv"

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