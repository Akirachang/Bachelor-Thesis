import pyrealsense2.pyrealsense2 as rs
import numpy as np
import math
import cv2

def getDepth(x, y, depth_frame):
    return depth_frame.get_distance(x, y)

def getDistance(x, y, color_intrin, depth):
    dx ,dy, dz = rs.rs2_deproject_pixel_to_point(color_intrin, [x,y], depth)
    return math.sqrt(((dx)**2) + ((dy)**2) + ((dz)**2))
