# coding: utf-8

# # Imports

# In[1]:

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

import json
import time
import threading
import csv
import collections

# myself function pack
import pic_cut_copy_v2

# Image caption's pack
from im2txt import run_inference


# ## Env setup

# In[2]:

# This is needed to display the images.
# get_ipython().magic(u'matplotlib inline')

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# ## Object detection imports
# Here are the imports from the object detection module.

# In[3]:


from utils import label_map_util

from utils import visualization_utils as vis_util

# # Model preparation

# ## Variables

# In[4]:


# What model to download.
# Establish a directory for downloaded models
PATH_TO_CKPT = 'pretrain_model/faster_rcnn_resnet101_coco_11_06_2017/frozen_inference_graph.pb'

# Models name:
#
# ssd_mobilenet_v1_coco_11_06_2017
# ssd_inception_v2_coco_11_06_2017
# rfcn_resnet101_coco_11_06_2017
# faster_rcnn_resnet101_coco_11_06_2017
# faster_rcnn_inception_resnet_v2_atrous_coco_11_06_2017
#

# MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
# MODEL_FILE = MODEL_NAME + '.tar.gz'
# DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
# PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

# ## Download Model

# In[5]:


# opener = urllib.request.URLopener()
# opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
# tar_file = tarfile.open(MODEL_FILE)
# for file in tar_file.getmembers():
#    file_name = os.path.basename(file.name)
#    if 'frozen_inference_graph.pb' in file_name:
#        tar_file.extract(file, os.getcwd())


# ## Load a (frozen) Tensorflow model into memory.

# In[6]:


detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`,
#  we know that this corresponds to `airplane`.  Here we use internal utility functions,
# but anything that returns a dictionary mapping integers to appropriate string labels would be fine.

# In[7]:


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# global variables
dir_to_sort = []


# Helper code

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


def csv2dict(in_file, key, value):
    new_dict = {}
    with open(in_file, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        fieldnames = next(csv_reader)
        csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames, delimiter=',')
        for row in csv_reader:
            new_dict[row[key]] = row[value]
    return new_dict


def csv2list(in_file):
    new_list = []
    with open(in_file, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file)
        fieldnames = next(csv_reader)
        for row in csv_reader:
            new_list.append(row[0])
    return new_list


def comparefileASC(x, y):
    stat_x = os.stat(dir_to_sort + "/" + x)
    stat_y = os.stat(dir_to_sort + "/" + y)
    if stat_x.st_ctime < stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return 1
    else:
        return 0


def getplistASC(dir_in):
    fs = os.listdir(dir_in)
    iterms = []
    for f in fs:
        if f.endswith('.jpg'):
            iterms.append(f)
    iterms.sort(comparefileASC)
    return iterms


def name2num(file_name_in):
    file_timeinf = file_name_in.split('.')
    file_date, file_time = file_timeinf[0].split('-')
    name_num = long(file_date + file_time)
    return name_num


def loadOldProc(dir_in):
    fs = os.listdir(dir_in)
    cam_name_loaded = []
    proc_name_loaded = []
    for f in fs:
        pa, pb = f.split('x')
        cam_name_loaded.append(pa)
        proc_name_loaded.append(pb)
    proc_dict = dict(zip(cam_name_loaded, proc_name_loaded))
    return proc_dict


def saveNowProc(dir_in, proc_now):
    for c in proc_now:
        save_path = dir_in + '/' + c + 'x' + proc_now[c]
        f = open(save_path, 'w')
        f.close()
    print 'Process Saved Success!'


def removeOldProc(dir_in):
    fs = os.listdir(dir_in)
    for f in fs:
        if f.endswith(".jpg"):
            os.remove(os.path.join(dir_in, f))


# load images dir

list_cam = []
list_cam_pic = []
dir_cams = []

dir_picproj_master = '../getpicture/CaptureImg/output/'
dir_cam_master = dir_picproj_master + 'camera/'
path_camlist_ini = dir_picproj_master + 'CameraList.txt'
dir_proc_load = dir_picproj_master + 'pos_mem'
dir_crop_buffer = 'crop_buffer/'

for line in open(path_camlist_ini):
    this_line = line.strip('\n')
    list_cam.append(this_line)
print 'Camera list:', list_cam

for cam in list_cam:
    dir_cams.append(dir_cam_master + cam)

print dir_cams

cam_dir_dict = dict(zip(list_cam, dir_cams))

print cam_dir_dict

# make list in order
list_cam_now_num_proc = []
list_cam_now_str_proc = []
for dir_now in dir_cams:
    dir_to_sort = dir_now
    list_pic_ASC = getplistASC(dir_to_sort)
    firstpic = list_pic_ASC[0]
    lastpic = list_pic_ASC[-1]
    num_firstpic = name2num(firstpic)
    num_lastpic = name2num(lastpic)
    print list_pic_ASC
    print firstpic, '----->', num_firstpic
    print lastpic, '----->', num_lastpic
    now_pic_num = num_lastpic  # str(num_lastpic)
    list_cam_now_num_proc.append(now_pic_num)
    list_cam_now_str_proc.append(lastpic)
test = dict(zip(list_cam, list_cam_now_str_proc))

for nowcam in test:
    print nowcam, '|', test[nowcam]

# removeOldProc(dir_proc_load)
# saveNowProc(dir_proc_load,test)

test2 = loadOldProc(dir_proc_load)
for nowcam in test2:
    print nowcam, 'x', test[nowcam]

ttt = ['a', 'b']
print len(ttt), ttt.index('b'), ttt[1]

# print stop_here_checkpoint
# ## Load dataset

# In[9]:
'''
dataset_csv = csv2list('big_image/dataset_list.csv')  # <---------HERE
print dataset_csv

# dataset_csv = csv2dict('test_images_100/dataset_100_3.csv', 'name', 'people')
print 'Loaded dataset length = ', len(dataset_csv)
file_name_list = []
file_code_list = []

path = 'big_image/'  # <---------HERE
counter_a = 0
print '\nContent:\n'
for ti in dataset_csv:
    file_front = str(ti)
    file_name = file_front + '.jpg'
    file_path = path + file_name
    file_name_list.append(file_path)
    file_code_list.append(ti)
    # print ti,'  ',dataset_csv[ti]
print '\nFile path: (', len(file_name_list), ')\n'

print file_code_list
print file_code_list[0]
'''

# # Detection

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

# In[11]:

# Variables to statics someting
time_total = 0
old_time_total = 0
time_average = 0
old_time_average = 0
num_pic = 0
correct_num = 0
# total_num = len(file_name_list)
pos_pic = 0

path_csv_write = 'crop_buffer/cut_buffer.csv'
path_dup_buffer = 'dup_buffer/'
path_crop_buffer = 'crop_buffer/'

intial_time = time.clock()

first_time = 1
flag_to_process = 1

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        # can put in multiple images by image_path's kind = list.
        while True:
            time.sleep(1)  # Detect term 1 second
            if first_time == 1:
                print 'x', time.strftime("%Y-%m-%d %X", time.localtime())
            flag_processed = 0
            proc_mem = loadOldProc(dir_proc_load)
            for cam2p in cam_dir_dict:
                dir_to_sort = cam_dir_dict[cam2p]
                list_pic_now = getplistASC(dir_to_sort)
                last_name = proc_mem[cam2p]

                # if proc_mem = last pic
                if list_pic_now.index(proc_mem[cam2p]) == (len(list_pic_now) - 1):
                    flag_to_process = 0
                    print 'Do not need to process in this term. (', cam2p, ')'
                else:
                    flag_to_process = 1
                    flag_processed = 1
                    print 'Need to process.'

                if flag_to_process == 1:

                    csv_dstfile_2 = open(path_csv_write, 'ab')
                    csv_writer_2 = csv.writer(csv_dstfile_2)

                    index_0 = list_pic_now.index(proc_mem[cam2p]) + 1  # start after process pointed one
                    path_pic2proc = []
                    for i in range(index_0, len(list_pic_now)):
                        pic_path = cam_dir_dict[cam2p] + '/' + list_pic_now[index_0]
                        path_pic2proc.append(pic_path)
                        index_0 = index_0 + 1
                    print path_pic2proc

                    TEST_IMAGE_PATHS = path_pic2proc

                    for image_path in TEST_IMAGE_PATHS:
                        image_name = image_path.split('/')[-1]
                        print '*'
                        image = Image.open(image_path)
                        # the array based representation of the image will be used later in order to prepare the
                        # result image with boxes and labels on it.
                        image_np = load_image_into_numpy_array(image)
                        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                        image_np_expanded = np.expand_dims(image_np, axis=0)
                        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                        # Each box represents a part of the image where a particular object was detected.
                        boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                        # Each score represent how level of confidence for each of the objects.
                        # Score is shown on the result image, together with the class label.
                        scores = detection_graph.get_tensor_by_name('detection_scores:0')
                        classes = detection_graph.get_tensor_by_name('detection_classes:0')
                        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                        timerstart = time.time()

                        # Actual detection.
                        (boxes, scores, classes, num_detections) = sess.run(
                            [boxes, scores, classes, num_detections],
                            feed_dict={image_tensor: image_np_expanded})

                        timerend = time.time()

                        det_term_time = timerend - timerstart
                        if (num_pic > 0):
                            time_total = time_total + det_term_time
                            print '+Time add+'

                        print 'Image path:\n', image_path, '\n Take ', det_term_time, ' Second .'
                        if (num_pic == 0):
                            print 'INFO: First image term time will not be counted!'

                        num_pic = num_pic + 1

                        # Visualization of the results of a detection.
                        np_boxes = np.squeeze(boxes)
                        np_classes = np.squeeze(classes).astype(np.int32)
                        np_scores = np.squeeze(scores)
                        vis_util.visualize_boxes_and_labels_on_image_array(
                            image_np,
                            np_boxes,
                            np_classes,
                            np_scores,
                            category_index,
                            use_normalized_coordinates=True,
                            line_thickness=8)
                        plt.figure(figsize=IMAGE_SIZE)
                        #  plt.imshow(image_np)
                        #  plt.show()

                        max_boxes_to_draw = 20  # threshold of human boxes
                        min_score_thresh = 0.7  # threshold of confidence
                        min_pixels_thresh = 10000  # threshold of pic pixels prevent strange things
                        agnostic_mode = False
                        instance_masks = None
                        keypoints = None
                        box_to_display_str_map = collections.defaultdict(list)
                        box_to_color_map = collections.defaultdict(str)
                        box_to_instance_masks_map = {}
                        box_to_keypoints_map = collections.defaultdict(list)
                        num_person = 0
                        box_code = 0

                        if not max_boxes_to_draw:
                            max_boxes_to_draw = np_boxes.shape[0]
                        for i in range(min(max_boxes_to_draw, np_boxes.shape[0])):
                            if np_scores is None or np_scores[i] > min_score_thresh:
                                box = tuple(np_boxes[i].tolist())
                                if instance_masks is not None:
                                    box_to_instance_masks_map[box] = instance_masks[i]
                                if keypoints is not None:
                                    box_to_keypoints_map[box].extend(keypoints[i])
                                if np_scores is None:
                                    box_to_color_map[box] = 'black'
                                else:
                                    if not agnostic_mode:
                                        if np_classes[i] in category_index.keys():
                                            class_name = category_index[np_classes[i]]['name']
                                            # print class_name
                                            if class_name == "person":
                                                num_person = num_person + 1
                                                im_score = int(100 * np_scores[i])
                                                print 'pos:', box, '\nscore:', im_score
                                                ymin, xmin, ymax, xmax = box
                                                image_pil_t = Image.fromarray(np.uint8(image)).convert('RGB')
                                                im_width, im_height = image.size
                                                im_left = int(xmin * im_width)
                                                im_right = int(xmax * im_width)
                                                im_top = int(ymin * im_height)
                                                im_bottom = int(ymax * im_height)
                                                print 'Image size:\n', im_width, 'x', im_height
                                                print 'Box position:', 'Left:', im_left, 'Right:', im_right, 'Top:', im_top, 'Bottom:', im_bottom
                                                if ((im_right - im_left) * (im_bottom - im_top)) >= min_pixels_thresh:
                                                    im_camera = cam2p
                                                    filename = image_name
                                                    csv_writer_2.writerow(
                                                        [filename, im_camera, box_code, im_score, im_left, im_right,
                                                         im_top, im_bottom])
                                                    box_code = box_code + 1
                                                    print 'Write csv buffer file success!'
                                                else:
                                                    print 'Too Small than threshold', min_pixels_thresh, ',so drop it :('
                                        else:
                                            class_name = 'N/A'
                                        display_str = '{}: {}%'.format(
                                            class_name,
                                            int(100 * np_scores[i]))
                                        # print display_str
                                    else:
                                        display_str = 'score: {}%'.format(int(100 * np_scores[i]))
                                    box_to_display_str_map[box].append(display_str)

                        print 'People in this image is ', num_person
                        if num_person == 0:
                            os.remove(image_path)
                            print 'No people in this image, so delete it.'
                            image_name = last_name
                        else:
                            last_name = image_name
                        proc_mem[cam2p] = image_name
                        pos_pic = pos_pic + 1

                    removeOldProc(dir_proc_load)
                    saveNowProc(dir_proc_load, proc_mem)
                    csv_dstfile_2.close()

            if flag_processed == 1:
                time.sleep(1)
                print 'Cutting pictures now!'
                pic_cut_copy_v2.MyWork(dir_cam_master, path_csv_write, path_crop_buffer)
                time.sleep(1)
                # print 'Deduplicate this to earlier image.'
                # MyDeduplication.MyWork()
                # time.sleep(1)
                print 'Image captioning now!'
                run_inference.main(path_crop_buffer, path_csv_write, path_dup_buffer, dir_cam_master)

                # print dasdasdas

                # Remove csv record before next term, prevent too long file.
                os.remove(path_csv_write)

            print '******* WAIT FOR NEXT TERM *******'

# In[ ]:

print 'Will not be there!'
'''
# Show results
print '============================', '\nIn this term:'
print 'Model used:', PATH_TO_CKPT
print 'The total time is ', time_total, 'seconds'
time_average = time_total / (num_pic - 1)
print time_average, 'seconds per image'
accuracy = float(correct_num) / float(total_num) * 100
print 'Box position and score data are written in:', path_csv_write
print '============================'
'''
print 'Will not be there!'
# In[ ]:
