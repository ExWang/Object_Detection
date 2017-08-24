import os
import sys
from PIL import Image
import csv


# Help functions

def csv2list(in_file):
    new_list = []
    with open(in_file, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file)
        x = 0
        for row in csv_reader:
            if x > 0:
                new_list.append(row)
            x += 1
    return new_list


# Prepare global var(s)
path_output = 'E:\\out_image'
path_input = 'E:\\big_image'

threshold_score = 50  # 80
threshold_ratio_min = 1.0  # 1.5
threshold_ratio_max = 6.0  # 5.0
threshold_pixel_min = 10000  # 20000

name_position = 1

def del_files(path_in):
    for root, dirs, files in os.walk(path_in):
        for name in files:
            if name.endswith(".jpg"):
                os.remove(os.path.join(root, name))

# Debug position
debug_a = 0

del_files(path_output)


for root, dirs, files in os.walk(path_input):
    for dir in dirs:

        # if debug_a == 1:
        # break

        # Create CSV files paths
        dir_path = os.path.join(root, dir)
        csv_filename = 'dataset_cutinf.csv'  # csv_filename = dir + '.csv'
        csv_path = os.path.join(dir_path, csv_filename)
        print csv_path

        now_list = csv2list(csv_path)

        # CSV Form: | name | score | left | right | top | bottom |
        print now_list

        for key in now_list:
            print '*'
            name = key[0]
            score = key[1]
            left = float(key[2])
            right = float(key[3])
            top = float(key[4])
            bottom = float(key[5])
            if score >= threshold_score:
                # print name, score, left, right, top, bottom
                img_name = name + '.jpg'
                img_path = os.path.join(dir_path, img_name)
                print 'Image path:', img_path
                img_file = Image.open(img_path)
                print 'Image info:', img_file.format, img_file.size, img_file.mode
                box = [left, top, right, bottom]
                region = img_file.crop(box)
                region_pixel = region.size[0] * region.size[1]
                region_ratio = float(region.size[1]) / float(region.size[0])
                print 'Region pixels:', region_pixel, '\nRegion height/width:', region_ratio
                if region_pixel >= threshold_pixel_min:
                    if region_ratio >= threshold_ratio_min:
                        if region_ratio <= threshold_ratio_max:
                            img_save_name = str(name_position) + '.jpg'
                            img_save_path = os.path.join(path_output, img_save_name)
                            region.save(img_save_path)
                            name_position += 1
        print 'Images which are in {} finished'.format(dir)
        # debug_a += 1

print '\nThe work finished successfully!'
