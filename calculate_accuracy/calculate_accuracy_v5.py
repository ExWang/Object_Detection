# -*- coding:utf-8 -*-
# import xlrd
import random
# import nltk
import json
import os

path = "E:\\out_image\\"


def del_files(path_in):
    for root, dirs, files in os.walk(path_in):
        for name in files:
            if name.endswith(".jpg"):
                os.remove(os.path.join(root, name))


# load ground truth
with open(path + "test_ground_truth.json") as f:
    ground_truth = json.load(f)

predict_filename = "caption_testother.json"  # Best conclusion
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

action_list = ['', 'stand', 'sit', '', 'walk', 'calling', '', 'bend', '', '', '', 'squat']

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

    if False:#image_name not in ground_truth:
        print("wrong {}".format(image_name))
    else:
        sex_item = 0
        predict_color = []
        predict_action = []
        i = 0
        for caption in captions:
            # print '\norder:', i
            i += 1
            item = caption[0]
            # print item
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
        # Data to show
        predict_action_str = []
        color_pre_now = []
        predict_color = list(set(predict_color))

        for key in list(set(predict_action)):
            predict_action_str.append(action_list[key])
        for color in predict_color:
            color_pre_now.append(color)
        predict_sex = 1 if sex_item > 0 else 0

        # Show data
        print '\n=============='
        print 'Image name:', image_name
        print 'Sex:', sex_list[predict_sex]
        print 'Color', color_pre_now
        print 'Predict actions:', predict_action_str
        print '================'

print 'Finished!'
