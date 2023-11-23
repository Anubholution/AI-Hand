import numpy as np
import requests
import cv2
import io 
import base64
import time
import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image
from segmentation_inference import segment
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
conf_score=0.00
count=0
loss_factor=0.0
while True:
    
    frame = pipe.wait_for_frames()
    #depth_frame = frame.get_depth_frame()
    color_frame = frame.get_color_frame()

    #depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    #depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,alpha = 0.5), cv2.COLORMAP_JET)

    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

    cv2.imshow('rgb', color_image)

    k = cv2.waitKey(33)
    # 99 refers to 'c'
    if k == 99:
        #print('c')
        before_time = time.time()
        url = 'http://35.226.240.71:8501/detect_objects' 
        my_img = {'image': base64.b64encode(cv2.imencode('.jpg', color_image)[1]).decode('utf-8')}

        response = requests.post(url, json=my_img)
        print(response.status_code)

        if response.status_code == 200:
            response_data = response.json()

            # Extract response data
            image_with_boxes_base64 = response_data['image_with_boxes']
            class_labels = response_data['labels']
            confidence_scores = response_data['confidence_scores']

            # Decode the image with bounding boxes
            image_with_boxes_bytes = base64.b64decode(image_with_boxes_base64)
            image_with_boxes = cv2.imdecode(np.frombuffer(image_with_boxes_bytes, np.uint8), cv2.IMREAD_COLOR)


            # Display detected labels and confidence scores 
            index=0
            cv2.imshow('Object Detection', image_with_boxes)
            for label, confidence in zip(class_labels, confidence_scores):
                print(f"Label: {label}, Confidence: {confidence:.2f}")
                segment(label,color_image,index)
                index=index+1
            # resp=int(input("Enter 1 for correct prediction and enter 0 for wrong prediction : "))
            # if(resp == 1):
            #     # Display the image with bounding boxes using OpenCV
            #     cv2.imshow('Object Detection', image_with_boxes)
            #     conf_score=conf_score+(confidence*100)
            # else:
            #     loss_factor=loss_factor+1
            # count = count + 1

            # Wait for a key press and then close the image window
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print('Error: Failed to retrieve classification results.')
            break

    if k == 113:
        
        cv2.destroyAllWindows()
        break
conf_score = conf_score/count
loss_factor = (loss_factor*100.0)/count
if(((conf_score)-(loss_factor)) < 0.0):
    print("Integrity of the model is : 0")
else:
    print("Integrity of the model is : ",((conf_score)-(loss_factor)))
pipe.stop()

