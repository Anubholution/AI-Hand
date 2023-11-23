import os
import utils_vision
import cv2
import random
import datetime
import numpy as np

import autoai_utils

import warnings
warnings.filterwarnings("ignore")

DETECTION_MODEL_ID = "653fc06b1de99379e26ba010"


def send_image_toRLEF(file_path,label):
    request_id = random.randint(1, 9999999)
    datetime_date = datetime.datetime.now().strftime("%d-%m-%Y")
    datetime_time = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    csv = "ID : %s<br>" % request_id   
    autoai_utils.send_to_autoai("backlog",
                                csv,
                                DETECTION_MODEL_ID,
                                label,
                                "DETECTION_%s" % datetime_date,
                                100,
                                "predicted",
                                "annotation",
                                file_path,
                                None,
                                "image/png")