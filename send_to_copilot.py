import os
import utils_vision
import cv2
import random
import datetime
import numpy as np
import requests

import autoai_utils

import warnings
warnings.filterwarnings("ignore")

DETECTION_MODEL_ID = "65452578510b635f74ec9bc2"

def send_image_copilot(filename):#, imageAnnotations):
    url = "https://autoai-backend-exjsxe2nda-uc.a.run.app/coPilotResource/"
    # annotation = {
    #     'screw',
    #     'tulip',
    #     'rocks',
    #     'washers'
    # }
    payload = {
        'coPilot': '65452578510b635f74ec9bc2',
        'status': 'active',
        'tag': str(datetime.date.today()),
        'type': 'image',
        'name': filename,
        'csv': ''}
        # 'imageAnnotations': annotation}

    files = [('resource', (filename, open(filename, 'rb'), 'image/png'))]
    headers ={}
    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

    if response.status_code == 200:
        print("Sent to copilot")
    else:
        print("error")