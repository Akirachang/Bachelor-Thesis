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


try:
    while True:
        # This call waits until a new coherent set of frames is available on a device
        frames = pipeline.wait_for_frames()
        
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        aligned_color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not aligned_color_frame: continue
        ##MY CODE
        colorizer = rs.colorizer()
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.filter_magnitude,5)
        spatial.set_option(rs.option.filter_smooth_alpha,1)
        spatial.set_option(rs.option.filter_smooth_delta,50)
        filtered_depth = spatial.process(depth_frame)
        colorized_depth = np.asanyarray(colorizer.colorize(filtered_depth).get_data())
        cv2.imshow('filtered depth',colorized_depth)
        ##MY CODE
        color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics
        depth_image = np.asanyarray(depth_frame.get_data())
        # dec_filter = rs.decimation_filter ()
        # filtered = dec_filter.process(depth_frame)
        #Use pixel value of  depth-aligned color image to get 3D axes
        x, y = 320, 180

        # print(type(decimationed_depth))
        # print(type(depth_frame))

        depth = getDepth(x,y,depth_frame)
        distance = getDistance(x,y,color_intrin,depth)
        print("Distance from camera to P1:", distance*100)
        print("Z-depth from camera surface to P1 surface:", depth*100)

        x1, y1 = 400, 180
        depth1 = getDepth(x1,y1,depth_frame)
        distance1 = getDistance(x1,y1,color_intrin,depth1)
        print("Distance from camera to P2:", distance1*100)
        print("Z-depth from camera surface to P2 surface:", depth1*100)

        display(distance, distance1, pipeline, x1, y1)

except Exception as e:
    print(e)
    pass

finally:
    pipeline.stop()