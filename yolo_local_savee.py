from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pyrealsense2 as rs
from send_to_copilot import send_image_copilot
import os
print("started")
# Load the YOLO model
model_path = "best1.pt"
yolo_model = YOLO(model_path)
incorrect_folder = "/home/aih/Downloads/incorrect_folder"
pipe = rs.pipeline()
cfg  = rs.config()

cfg.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)
#cfg.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30)

pipe.start(cfg)

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

    if(k==99):    

        cv2.imwrite('image_temp.png',color_image)
        image_np = np.array(cv2.imencode('.jpg', color_image)[1])
        image_np = color_image
        print("image loaded")
            # Perform object detection using YOLO
        results = yolo_model(['image_temp.png'])[0]

        print("yolo detected")
        boxes = results.boxes.xyxy
        confidence_scores = results.boxes.conf.tolist()
        print(confidence_scores)
        class_names = results.names
        class_labels = [class_names[int(class_id)] for class_id in results.boxes.cls.tolist()]
        print(class_labels)
        for i in range(len(class_labels)):
            if (class_labels[i] == 'rocks'):
                class_labels[i] = 'washers'

            # Process detection results and draw bounding boxes on the image
         # Process detection results and draw bounding boxes on the image
        for box, label, confidence in zip(boxes, class_labels, confidence_scores):
            x1, y1, x2, y2 = map(int, box[:4])
            cv2.rectangle(image_np, (x1, y1), (x2, y2), (0, 0, 255), 4)
            label_text = f"{label}: {confidence:.2f}"
            cv2.putText(image_np, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            print(f"Label: {label}, Confidence: {confidence:.2f}")
            RGB_img= cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB)
            cv2.imwrite('/home/aih/Downloads/fail_image.png',RGB_img)
            for i in confidence_scores:
                if i < 0.7:
                    send_image_copilot('/home/aih/Downloads/fail_image.png')
                    save_path = os.path.join(incorrect_folder, f'incorrect_image_{len(os.listdir(incorrect_folder))}.png')
                    cv2.imwrite(save_path, RGB_img)
                    print(f"Image saved at {save_path}")#,

            # Convert the annotated image to a base64-encoded string
        ret, img_encoded = cv2.imencode('.jpg', image_np)
        
        
        for label, confidence in zip(class_labels, confidence_scores):
            print(f"Label: {label}, Confidence: {confidence:.2f}")
        cv2.imshow('Object Detection', image_np)

    '''        # Prompt user for feedback
        feedback = int(input("Enter 0 if the annotation is correct, 1 if it's wrong: ")) 

    # Save the image based on user feedback
        if feedback == 1:
            save_path = os.path.join(incorrect_folder, f'incorrect_image_{len(os.listdir(incorrect_folder))}.png')
            cv2.imwrite(save_path, RGB_img)
            print(f"Image saved at {save_path}")
'''

    if(k==113):
        pipe.stop()
        break
            