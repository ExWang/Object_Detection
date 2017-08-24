# -*- coding:utf-8 -*-
# import xlrd
import random
# import nltk
import json
import os

path = "E:\\Dataset_7.26\\"


def del_files(path_in):
    for root, dirs, files in os.walk(path_in):
        for name in files:
            if name.endswith(".jpg"):
                os.remove(os.path.join(root, name))


# load ground truth
with open(path + "test_ground_truth.json") as f:
    ground_truth = json.load(f)

predict_filename = "crop-4924.json"  # Best conclusion
with open(path + predict_filename) as f1:
    predict = json.load(f1)

total_num = len(ground_truth)
sex_num = 0
color_rough_num = 0
color_fine_num = 0
action_num = 0
sex_list = ['girl', 'boy']
color_list = ['blue', 'gray', 'brown', 'purple', 'yellow', 'pink', 'black', 'green', 'striped', 'white', 'red', "plaid"]
action_hash = {'standing': 1, 'stands': 1, 'sitting': 2, 'sits': 2, 'walking': 4, 'walks': 4, 'calling': 5, 'calls': 5,
               'bending': 7, 'bends': 7, 'squatting': 11, 'squats': 11}

total_sex = 0
total_col_rou = 0
total_col_fin = 0
total_action = 0

condition_A = 'yellow'  # color
condition_B = 'yellow'  # color
condition_C = 'boy'  # sex
condition_D = 4  # action
path_output = path + 'result'

del_files(path_output)

for image in predict:
    captions = predict[image]
    image_name = str(int(image.split("/")[-1].strip(".jpg")))
    # print(image_name)
    # if image_name != "1346":
    #     continue
    # print captions
    imgname_jpg = image.split("/")[-1]

    if image_name not in ground_truth:
        print("wrong {}".format(image_name))
    else:
        sex_item = 0
        predict_color = []
        predict_action = []
        i = 0
        for caption in captions:
            #print '\norder:', i
            i += 1
            item = caption[0]
            #print item
            if item.find("boy") > 0 or item.find(" man ") > 0:
                sex_item += 1
            elif item.find("girl") > 0 or item.find("woman") > 0:
                sex_item -= 1
            else:
                print("sex miss!")

            for color in color_list:
                if item.find(color) > 0:
                    predict_color.append(color)
            for action in action_hash:
                if item.find(action) > 0:
                    predict_action.append(action_hash[action])

        # sex accuracy
        predict_sex = 1 if sex_item > 0 else 0
        if predict_sex == ground_truth[image_name]["sex"]:
            #print 'predict_sex:', predict_sex
            sex_num += 1
        else:
            # Save images
            print imgname_jpg, 'Wrong: Truth value', sex_list[ground_truth[image_name]["sex"]], ' Predict value:', sex_list[predict_sex]
            #if predict_sex == 1
            src_path = path + 'test'
            dst_path = path_output
            sourceFile = os.path.join(src_path, imgname_jpg)
            targetFile = os.path.join(dst_path, imgname_jpg)
            if os.path.isfile(sourceFile):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
            # end

        predict_color = list(set(predict_color))
        # rough color accuracy
        for color in predict_color:
            if color in ground_truth[image_name]["color"]:
                color_rough_num += 1
                break

        # fine color accuracy
        set_A = set(predict_color)
        set_B = set(ground_truth[image_name]["color"])
        set_C = set_A & set_B
        C_len = len(set_C)
        D_len = len(ground_truth[image_name]["color"])

        if C_len == D_len:
            # print('+++Correct!+++')
            color_fine_num += 1.

        # action accuracy
        if ground_truth[image_name]["action"] in list(set(predict_action)):
            action_num += 1


print("Predict JSON file name:", predict_filename)
print("sex accuracy {}".format(sex_num * 1.0 / total_num))
print("color rough accuracy {}".format(color_rough_num * 1.0 / total_num))
print("color fine accuracy {}".format(color_fine_num * 1.0 / total_num))
print("action accuracy {}".format(action_num * 1.0 / total_num))
total_sex = total_sex + (sex_num * 1.0 / total_num)
total_col_rou = total_col_rou + (color_rough_num * 1.0 / total_num)
total_col_fin = total_col_fin + (color_fine_num * 1.0 / total_num)
total_action = total_action + (action_num * 1.0 / total_num)
