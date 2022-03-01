import argparse
import os
from sklearn.model_selection import train_test_split


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', type=str, help='path to you datasets (folder containing different datasets)')
    parser.add_argument('--source', type=str, help='folder name of source images (images are directly stored in this folder)')
    parser.add_argument('--savedir', type=str, help='path to where you want to save the txt-files')
    parser.add_argument('--name', type=str, help='name of this collection')
    parser.add_argument('--trainsize', type=float, default=0.7, help='size of the training-set in percent (optional)')
    parser.add_argument('--valsize', type=float, default=0.15, help='size of the validation-set in percent (optional)')

    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt

def main(opt):
    # Create papths
    path_data_images = os.path.join(opt.datadir, opt.source)
    train_size = opt.trainsize
    val_size = opt.valsize
    assert(train_size+val_size <= 1)
    
    path_datasets_txt = opt.savedir
    if not os.path.exists(path_datasets_txt):
        os.makedirs(path_datasets_txt)
        print(f"'{path_datasets_txt}' directory is created!")

    path_train_file = os.path.join(path_datasets_txt,f"{opt.name}_train.txt")
    path_val_file = os.path.join(path_datasets_txt,f"{opt.name}_val.txt")
    path_test_file = os.path.join(path_datasets_txt,f"{opt.name}_test.txt")
    path_all_file = os.path.join(path_datasets_txt,f"{opt.name}_all.txt")

    files = os.listdir(path_data_images)

    nr_of_images = len(files)

    print(f"Number of files: {nr_of_images}")

    X_train, X_val = train_test_split(files, train_size=train_size, shuffle=True)
    X_val, X_test = train_test_split(X_val, test_size=val_size/(1-train_size)) # 0.15 per list

    with open(path_all_file, "w") as output_all:

        with open(path_train_file, "w") as output:

            for file in X_train:
                output.write(f"{str(os.path.join(path_data_images, file))}\n")
                output_all.write(f"{str(os.path.join(path_data_images, file))}\n")
        output.close()
        print(f"{len(X_train)} images stored in {path_train_file}")
        
        with open(path_val_file, "w") as output:

            for file in X_val:
                output.write(f"{str(os.path.join(path_data_images, file))}\n")
                output_all.write(f"{str(os.path.join(path_data_images, file))}\n")
        output.close()
        print(f"{len(X_val)} images stored in {path_val_file}")

        with open(path_test_file, "w") as output:

            for file in X_test:
                output.write(f"{str(os.path.join(path_data_images, file))}\n")
                output_all.write(f"{str(os.path.join(path_data_images, file))}\n")
        output.close()
        print(f"{len(X_test)} images stored in {path_test_file}")
        
    output_all.close()

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)