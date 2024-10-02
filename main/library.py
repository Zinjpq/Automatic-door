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

class ESP32CamApp:
    def __init__(self, root):
        self.status_label_1 = None
        self.status_label_2 = None
        self.video_label = None
        self.root = root
        self.root.title("ESP32-CAM Setup")
        self.root.geometry("1280x720")

        # ESP32-CAM URLs
        self.url_cam = 'http://192.168.1.100/cam'
        self.url1 = 'http://192.168.1.100/left'
        self.url2 = 'http://192.168.1.100/right'
        self.url3 = 'http://192.168.1.100/up'
        self.url4 = 'http://192.168.1.100/down'

        # Initialize scenes
        self.scene_1_frame = tk.Frame(self.root)
        self.scene_2_frame = tk.Frame(self.root)

        self.create_scene_1()  # Create the first scene
        self.create_scene_2()  # Pre-create the second scene, but keep it hidden

        # Start checking for connection
        threading.Thread(target=self.check_connection, daemon=True).start()

    # Scene 1: Connection instructions
    def create_scene_1(self):
        self.scene_1_frame.pack(fill="both", expand=True)

        self.status_label_1 = tk.Label(self.scene_1_frame, text="Chưa kết nối với ESP32-CAM", font=("Arial", 16))
        self.status_label_1.pack(pady=20)

        ssid_label = tk.Label(self.scene_1_frame, text="SSID: ESP32-CAM", font=("Arial", 14))
        ssid_label.pack()

        password_label = tk.Label(self.scene_1_frame, text="Password: 123456789", font=("Arial", 14))
        password_label.pack()

        qr_label = tk.Label(self.scene_1_frame)
        qr_label.pack(pady=10)
        qr_img = generate_qr('http://192.168.4.1')
        qr_label.config(image=qr_img)
        qr_label.image = qr_img  # Keep a reference to avoid garbage collection

        access_point_label = tk.Label(self.scene_1_frame, text="Kết nối vào http://192.168.4.1", font=("Arial", 14))
        access_point_label.pack(pady=20)

    # Scene 2: Video stream and controls
    def create_scene_2(self):
        video_label = tk.Label(self.scene_2_frame)
        video_label.pack(fill="both", expand=True)

        self.status_label_2 = tk.Label(self.scene_2_frame, text="Status: ", font=("Arial", 12))
        self.status_label_2.pack(side="bottom", fill="x")

        button_frame = tk.Frame(self.scene_2_frame)
        button_frame.pack(side="bottom", pady=10)

        tk.Button(button_frame, text="Left", command=lambda: self.send_command(self.url1)).grid(row=0, column=0)
        tk.Button(button_frame, text="Right", command=lambda: self.send_command(self.url2)).grid(row=0, column=2)
        tk.Button(button_frame, text="Up", command=lambda: self.send_command(self.url3)).grid(row=0, column=1)
        tk.Button(button_frame, text="Down", command=lambda: self.send_command(self.url4)).grid(row=1, column=1)

        self.video_label = video_label

    # Function to switch to Scene 2
    def switch_to_scene_2(self):
        self.scene_1_frame.pack_forget()  # Hide Scene 1
        self.scene_2_frame.pack(fill="both", expand=True)  # Show Scene 2
        self.update_video()  # Start video stream update

    # Check ESP32-CAM connection
    def check_connection(self):
        while True:
            try:
                response = requests.get('http://192.168.1.100', timeout=1)
                if response.status_code == 200:
                    self.status_label_1.config(text="Kết nối thành công với ESP32-CAM!")
                    self.switch_to_scene_2()
                    break
            except requests.exceptions.RequestException:
                self.status_label_1.config(text="Chưa kết nối được với ESP32-CAM...")
            time.sleep(2)

    # Generate QR Code

    # Send control commands to ESP32-CAM
    def send_command(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.status_label_2.config(text=f"Command successful: {url}")
            else:
                self.status_label_2.config(text=f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.status_label_2.config(text=f"Connection error: {e}")

    # Update video stream from ESP32-CAM
    def update_video(self):
        try:
            img_resp = requests.get(self.url_cam)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, -1)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)
        except Exception as e:
            self.status_label_2.config(text=f"Video stream error: {e}")
        self.root.after(30, self.update_video)

