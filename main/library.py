import re
import time
import urllib.request
import cv2
import numpy as np
import os
import tkinter as tk
import requests
import cv2
from PIL import Image, ImageTk
import numpy as np
import qrcode
import threading
import time
import cv2
import numpy as np
import os
import requests
import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import time
import numpy as np

import DetectChars
import DetectPlates
import PossiblePlate

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

# ESP32-CAM URL and Control URLs
url_or = 'http://192.168.3.61'

url_cam = url_or + '/cam'
url1 = url_or + '/left'
url2 = url_or + '/right'
url3 = url_or + '/up'
url4 = url_or + '/down'

def detect_plate(imgOriginalScene):
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # attempt KNN training

    if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")  # show error message
        return  # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

    listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
    
    licPlate = listOfPossiblePlates[0]
    return licPlate.strChars

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return ImageTk.PhotoImage(img)