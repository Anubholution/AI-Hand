import numpy as np
import requests
import cv2
import numpy as np
import io
import base64
import bytesbufio as BytesIO
from io import BytesIO
import time

def get_image_handler(img_arr):
    ret, img_encode = cv2.imencode('.jpg', img_arr)
    str_encode = img_encode.tostring()
    img_byteio = io.BytesIO(str_encode)
    img_byteio.name = 'img.jpg'
    reader = io.BufferedReader(img_byteio)
    return reader

def segment(label,image,index):
    print("Going for segmentation")
    before_time=time.time()
    url = 'http://34.173.105.110:5000/segment'
    my_img = {'image': ('img.jpg', get_image_handler(image)),'query':label}  # Create a dictionary with the expected format
    response = requests.post(url, files=my_img)

    if response.status_code == 200:
        after_time=time.time()
        print("Inference Time is : ",after_time-before_time)
        data = response.json()
        width, height = data['size']
        channels = data['channels']
        image_data_base64 = data['img']
        screw_width = data["width"]*77.56
        angle_of_inclination = data["angle"]

        # Decode the base64-encoded image data back to bytes
        image_data = base64.b64decode(image_data_base64.encode('utf-8'))

        # Create a NumPy array from the image data
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

        # Now, you have the image, width, height, and channels
                # Now, you have the image, width, height, and channels
        print(f'Image dimensions: {width}x{height}')
        print(f'Number of channels: {channels}')
        print(f"width of the {label} is:{screw_width}")
        print(f"angle of incination is : {angle_of_inclination}")
        window_name="frame"+str(index)
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
# while True:

#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break

#     # frame=cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
#     # frame = image.astype('uint8')
#     cv2.imshow('frame', frame)
#     # print(type(frame))
#     k=cv2.waitKey(33)
#     #99 refers to c
#     if (k==99):
        
#     #113 refers to q
#     if k==113:
#         break
# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()