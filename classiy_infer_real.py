import numpy as np
import requests
import cv2
import io
import base64 
import time
import pyrealsense2 as rs
import numpy as np
import cv2
#import send_image_RLEF 

pipe = rs.pipeline()
cfg  = rs.config()

cfg.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)
#cfg.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30)

pipe.start(cfg)

def get_image_handler(img_arr):
    ret, img_encode = cv2.imencode('.jpg', img_arr)
    str_encode = img_encode.tostring()
    img_byteio = io.BytesIO(str_encode)
    img_byteio.name = 'img.jpg'
    return img_byteio

while True:
    
    frame = pipe.wait_for_frames()
    #depth_frame = frame.get_depth_frame()
    color_frame = frame.get_color_frame()
    #color_frame.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    #color_frame.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    #depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    #depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,alpha = 0.5), cv2.COLORMAP_JET)

    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    cv2.imshow('rgb', color_image)
    cv2.moveWindow('rgb', 40,30)

    key = cv2.waitKey(33)
    # 99 refers to 'c'
    if key == 32:  # Spacebar key
            file_path = f"realsense-1080p_1.jpg"  # Define file path with unique name
            cv2.imwrite(file_path, color_image)
            print(f"Image saved to {file_path}")
            #image_count += 1  # Increment image count for the next capture
    elif key == 27:  # ESC key
        print("Image capture canceled")
        break

pipe.stop()
cv2.destroyAllWindows()

