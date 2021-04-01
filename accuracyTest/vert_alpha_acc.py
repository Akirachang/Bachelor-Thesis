import sys
sys.path.insert(0, '..')

import pyrealsense2.pyrealsense2 as rs
import numpy as np
import math
import cv2
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

distanceCM = 30.0
pixel_cm = 0.0264583333 
cm_pixel = 37.7952755906

try:
    while True:
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
        # dec_filter = rs.decimation_filter ()
        # filtered = dec_filter.process(depth_frame)
        #Use pixel value of  depth-aligned color image to get 3D axes
        x, y = 320, 180
        depth = getDepth(x,y,depth_frame)
        distance = getDistance(x,y,color_intrin,depth)
        print("Distance from camera to P1:", distance*100)
        print("Z-depth from camera surface to P1 surface:", depth*100)

        accurateDistance = distanceCM
        # accuracy_virtDist = 100-100*((abs(accurateDistance-depth)/accurateDistance))
        accuracy_virtDist = depth / accurateDistance
        print("accuracy of virtical distance is: ", accuracy_virtDist)

        x1, y1 = 420, 180
        depth1 = getDepth(x1,y1,depth_frame)
        distance1 = getDistance(x1,y1,color_intrin,depth1)
        print("Distance from camera to P2:", distance1*100)
        print("Z-depth from camera surface to P2 surface:", depth1*100)

        Z_coordinate = distance * cm_pixel # coordinate of the Z axis according to distance to object
        point_distance_px = math.sqrt(((x1-x)**2) + ((y1-y)**2) + ((0)**2))
        point_distance_cm = point_distance_px * pixel_cm
        accurateangle = math.degrees(math.atan(point_distance_cm/accurateDistance))

        #calcurate alpha angle
        try:
            print((math.acos(distance/distance1)))
            alpha = math.degrees((math.acos(distance/distance1)))
            print("Alpha angle is: ",alpha)
            display(distance, distance1, pipeline, x1, y1)
            print("accurate angle is: ",accurateDistance)
            print("alpha is: ",alpha)
            # accuracy_alpha = 100.0-100.0*((abs(accurateangle-alpha)/accurateangle))
            accuracy_alpha = alpha/accurateangle
            print("accuracy of alpha is: ", accuracy_alpha)

        except:
            print("error value!")


        display(distance, distance1, pipeline, x1, y1)

except Exception as e:
    print(e)
    pass

finally:
    pipeline.stop()