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
angle_dict={}

#the middle x coordinate of the screen
origin_x = 320

try:
    for i in range(1,2):
        sum = 0 #sum of all the angles combined
        for j in range(0,100):
            # This call waits until a new coherent set of frames is available on a device
            frames = pipeline.wait_for_frames()
            
            #Aligning color frame to depth frame
            aligned_frames =  align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            aligned_color_frame = aligned_frames.get_color_frame()

            if not depth_frame or not aligned_color_frame: continue

            color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(aligned_color_frame.get_data())
            #Use pixel value of  depth-aligned color image to get 3D axes
            x, y = 320, 180
            depth = getDepth(x,y,depth_frame)
            distance = getDistance(x,y,color_intrin,depth)
            print("Distance from camera to P1:", distance*100)
            print("Z-depth from camera surface to P1 surface:", depth*100)

            x1, y1 = origin_x+i, 180
            depth1 = getDepth(x1,y1,depth_frame)
            distance1 = getDistance(x1,y1,color_intrin,depth1)
            print("Distance from camera to P2:", distance1*100)
            print("Z-depth from camera surface to P2 surface:", depth1*100)

            #calculate Alpha angle
            try:
                print((math.acos(depth/depth1)))
                alpha = math.degrees((math.acos(depth/depth1)))
                sum+=alpha
                print("Alpha angle is: ",alpha)
            except:
                print("error value!")
        average = sum/100
        angle_dict[origin_x+i] = average
    print(angle_dict)

except Exception as e:
    print(e)
    pass

finally:
    #dumps into json file
    with open("10cm.json", "w") as write_file:
        json.dump(angle_dict, write_file)

    pipeline.stop()