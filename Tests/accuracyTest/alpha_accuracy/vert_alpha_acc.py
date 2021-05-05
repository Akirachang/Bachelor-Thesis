import sys
sys.path.insert(0, '../../..')

import pyrealsense2.pyrealsense2 as rs
import numpy as np
import math
import cv2
import json
from GUI_model import *
from calc_model import *

pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 15)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 15)

# Start streaming
pipeline.start(config)

align_to = rs.stream.depth
align = rs.align(align_to)

distanceCM = int(input("enter a distance: "))

# rs_alpha_file = open('../../../getAlpha_angle/rs_calculate/json/'+str(distanceCM)+'cm.json')
rs_alpha_file = open('../../../getAlpha_angle/rs_calculate/json/60cm-exposuretest.json')

dict_alpha = json.load(rs_alpha_file)

correct_alpha_file = open('../../../getAlpha_angle/correct_calculate/json/'+str(distanceCM)+'cm.json')


dict_correct = json.load(correct_alpha_file)
    
dict_acc = {}

origin_x = 320
origin_y = 180

try:
    for i in range(100,200):
        accurateangle = dict_correct[str(origin_x+i)]
        alpha = dict_alpha[str(origin_x+i)]
        print(accurateangle)
        print(alpha)
        accuracy_alpha = 100.0-100.0*((abs(accurateangle-alpha)/accurateangle))
        dict_acc[origin_x+i] = accuracy_alpha  
except:
    print("error value!")
    pass

finally:
    with open("json/60cm-exposuretest.json", "w") as write_file:
        json.dump(dict_acc, write_file)

    pipeline.stop()