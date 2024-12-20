# Library.py

import re
from datetime import datetime
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Frame, Label
import cv2
import numpy as np
import requests
from PIL import Image, ImageTk
import DetectChars
import DetectPlates

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\1.Projects\Automatic-door\main\assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#######################################################################################################################
# ESP32-CAM URL and Control URLs
url_or = 'http://192.168.4.184'
url_cam = url_or + '/cam'
url1 = url_or + '/left'
url2 = url_or + '/right'
url3 = url_or + '/up'
url4 = url_or + '/down'

# module level variables ################################################################################################ module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_RED = (0.0, 0.0, 255.0)
########################################################################################################################

# urlOriginal = 'http://192.168.1.100'
# url_cam = urlOriginal + '/cam'

# url_up = urlOriginal + '/up'
# url_down = urlOriginal + '/down'
# url_left = urlOriginal + '/left'
# url_right = urlOriginal + '/right'


########################################################################################################################
# Hàm để phát hiện và vẽ hộp bao quanh biển số xe
def detect_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    plate_images = []
    for (x, y, w, h) in plates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        plate_images.append(gray[y:y + h, x:x + w])

    return image, plate_images


########################################################################################################################
# Hàm để nhận diện ký tự trên biển số xe
def Detect_License_Plate():
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training
    cap = cv2.VideoCapture(0)  # Mở camera mặc định của laptop
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)

    while True:
        ret, imgOriginalScene = cap.read()  # Đọc frame từ camera
        if not ret:
            break
        cv2.imshow('detection', imgOriginalScene)

        listOfPossiblePlates, imgGrayscaleScene, imgThreshScene = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates

        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)

        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

        if len(listOfPossiblePlates) != 0:
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
            # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
            licPlate = listOfPossiblePlates[0]

            # Kiểm tra nếu chuỗi khớp mẫu "2 số + 1 chữ cái + 5 số"
            pattern = r"^\d{2}[A-Z]\d{5}$"  # 2 chữ số đầu + 1 chữ cái + 5 chữ số
            if re.match(pattern, licPlate.strChars):
                print(licPlate.strChars)


        key = cv2.waitKey(5)
        if key == ord('q'):  # Nhấn phím 'q' để thoát
            break

    cap.release()
    cv2.destroyAllWindows()
# end function##########################################################################################################


# # Function to send control signals to ESP32
# def send_command(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             print(f"Command sent successfully: {url}")
#             status_label.config(text=f"Command successful: {url}")
#         else:
#             print(f"Error: {response.status_code}")
#             status_label.config(text=f"Error: {response.status_code}")
#     except requests.exceptions.RequestException as e:
#         print(f"Connection error: {e}")
#         status_label.config(text=f"Connection error: {e}")

########################################################################################################################
# Function to display video stream from ESP32-CAM
# def update_video():
#     try:
#         # Fetch the frame from ESP32-CAM
#         img_resp = requests.get(url_cam)
#         img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
#         frame = cv2.imdecode(img_arr, -1)
#
#         # Convert the frame to a format compatible with Tkinter
#         img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         img = Image.fromarray(img)
#         imgtk = ImageTk.PhotoImage(image=img)
#
#         # Update the video label
#         video_label.imgtk = imgtk
#         video_label.config(image=imgtk)
#     except Exception as e:
#         print(f"Error in video stream: {e}")
#         status_label.config(text=f"Video stream error: {e}")
#
#     # Update the video every 30ms
#     root.after(30, update_video)


########################################################################################################################

# Function to handle key presses for movement controls
# def on_key_press(event):
#     if event.keysym in ["Left", "a", "A"]:
#         send_command(url1)  # Left
#     elif event.keysym in ["Right", "d", "D"]:
#         send_command(url2)  # Right
#     elif event.keysym in ["Up", "w", "W"]:
#         send_command(url3)  # Up
#     elif event.keysym in ["Down", "s", "S"]:
#         send_command(url4)  # Down

########################################################################################################################
def create_button(image_path, parent, command, x, y, width, height):
            button_image = PhotoImage(file=relative_to_assets(image_path))
            button = Button(parent,image=button_image, borderwidth=0, highlightthickness=0, relief="flat",
                            command=command)
            button.image = button_image  # Keep a reference to avoid garbage collection
            button.place(x=x, y=y, width=width, height=height)

def add_image(image_path, parent, x=0, y=0):
    image = PhotoImage(file=relative_to_assets(image_path))
    label = Label(parent, image=image, bg=parent['bg'])
    label.image = image  # Giữ tham chiếu để tránh bị xoá
    label.place(x=x, y=y)

########################################################################################################################
def create_time_and_date_labels(parent, time_coords, date_coords, font, color="#000000"):
    # Create labels for time and date
    time_label = Label(parent, text="", font=font, fg=color, bg=parent["bg"])
    time_label.place(x=time_coords[0]-256, y=time_coords[1])

    date_label = Label(parent, text="", font=font, fg=color, bg=parent["bg"])
    date_label.place(x=date_coords[0]-256, y=date_coords[1])

    # Function to update time and date
    def update_time_and_date():
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")
        time_label.config(text=current_time)
        date_label.config(text=current_date)
        time_label.after(1000, update_time_and_date)  # Update every second

    update_time_and_date()

########################################################################################################################
import threading
import time


class LivestreamWidget(Frame):
    def __init__(self, parent, camera_url):
        super().__init__(parent, bg="#000000", width=640, height=480)
        self.camera_url = camera_url
        self.canvas = Canvas(self, bg="#000000", width=640, height=480, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.error_label = Label(self, bg="#F2F4F8")
        self.error_image = ImageTk.PhotoImage(file=relative_to_assets("image_Cameraerror.png"))
        self.error_label.config(image=self.error_image)
        self.error_label.place(x=0, y=0)
        self.error_label.lower()

        self.running = True
        threading.Thread(target=self.stream_video, daemon=True).start()

    def stream_video(self):
        while self.running:
            try:
                start_time = time.time()

                # Tải ảnh từ camera
                img_resp = requests.get(self.camera_url, timeout=2)
                img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

                # Resize để giảm tải hệ thống
                frame = cv2.resize(frame, (320, 240))
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Chuyển ảnh thành PhotoImage
                photo = ImageTk.PhotoImage(image=Image.fromarray(img))

                # Cập nhật Canvas trong main thread
                self.canvas.after(0, self.update_canvas, photo)
                self.error_label.lower()

                # Giới hạn FPS (khoảng 10-15 FPS)
                elapsed = time.time() - start_time
                time.sleep(max(0.1 - elapsed, 0))  # Tối thiểu 100ms giữa các khung hình

            except Exception:
                self.canvas.after(0, self.show_camera_error)

    def update_canvas(self, photo):
        self.canvas.create_image(0, 0, anchor="nw", image=photo)
        self.canvas.image = photo

    def show_camera_error(self):
        self.error_label.lift()
        self.canvas.delete("all")

    def stop(self):
        self.running = False
