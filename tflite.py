import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tensorflow as tf
import time


model_path = 'yolov8n_float16.tflite'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Obtain the height and width of the corresponding image from the input tensor
image_height = input_details[0]['shape'][1] # 640
image_width = input_details[0]['shape'][2] # 640

# Image Preparation
image_name = 'image0.png'
image = Image.open(f'{image_name}')
image_resized = image.resize((640, 640)) # Resize the image to the corresponding size of the input tensor and store it in a new variable

image_np = np.array(image_resized) #
image_np = np.true_divide(image_np, 255, dtype=np.float32) 
image_np = image_np[np.newaxis, :]

# inference
interpreter.set_tensor(input_details[0]['index'], image_np)

start = time.time()
interpreter.invoke()
print(f'run time：{time.time() - start:.2f}s')

# Obtaining output results
output = interpreter.get_tensor(output_details[0]['index'])
output = output[0]
output = output.T

boxes_xywh = output[..., :4] #Get coordinates of bounding box, first 4 columns of output tensor
scores = np.max(output[..., 5:], axis=1) #Get score value, 5th column of output tensor
classes = np.argmax(output[..., 5:], axis=1) # Get the class value, get the 6th and subsequent columns of the output tensor, and store the largest value in the output tensor.

# Threshold Setting
threshold = 0.3

# Bounding boxes, scores, and classes are drawn on the image
draw = ImageDraw.Draw(image_resized)

for box, score, cls in zip(boxes_xywh, scores, classes):
    if score >= threshold:
        x_center, y_center, width, height = box
        x1 = int((x_center - width / 2) * image_width)
        y1 = int((y_center - height / 2) * image_height)
        x2 = int((x_center + width / 2) * image_width)
        y2 = int((y_center + height / 2) * image_height)

        draw.rectangle([x1, y1, x2, y2], outline="red", width=1)
        text = f"Class: {cls}, Score: {score:.2f}"
        print(text)
        draw.text((x1, y1), text, fill="blue")

# Saving Images
image_resized.save(f"detected_{image_name}")