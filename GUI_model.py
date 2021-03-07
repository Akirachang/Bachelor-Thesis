import pyrealsense2.pyrealsense2 as rs
import numpy as np
import math
import cv2

def drawCircle(images,x,y):  
    #Draw a circle
    # Center coordinates
    center_coordinates = (x, y)
    
    # Radius of circle
    radius = 5
    
    # Red color in BGR
    color = (0, 0, 255)
    
    # Line thickness of -1 px
    thickness = -1

    return cv2.circle(images, center_coordinates, radius, color, thickness)

def drawWords(images,x,y,point):
    font = cv2.FONT_HERSHEY_SIMPLEX 
  
    # org 
    org = (x, y) 
    
    # fontScale 
    fontScale = 1
    
    # Blue color in BGR 
    color = (0, 0, 255) 
    
    # Line thickness of 1 px 
    thickness = 1
    
    # Using cv2.putText() method 
    return cv2.putText(images, point, org, font, fontScale, color, thickness, cv2.LINE_AA) 

def display(depth,depth1,pipeline):
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
        return

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape

    # If depth and color resolutions are different, resize color image to match depth image for display
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        images = np.hstack((resized_color_image, depth_colormap))
    else:
        images = np.hstack((color_image, depth_colormap))

    window_name = 'Image'

    # Using cv2.circle() method
    # Draw a circle of red color of thickness -1 px
    image = drawCircle(images,320,180)
    # image1 = drawWords(images,330,180,'P1')
    image1 = drawWords(images,330,160,str(depth))


    image2 = drawCircle(images,500,180)
    # image3 = drawWords(images,410,180,'P2')
    image3 = drawWords(images,510,200,str(depth1))


    # Displaying the image 
    cv2.imshow('RealSense', image) 
    cv2.imshow('RealSense', image1)  
    cv2.imshow('RealSense', image2)  
    cv2.imshow('RealSense', image3)  

    # Show images 
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)
    cv2.waitKey(1)
