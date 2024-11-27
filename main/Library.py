# Library.py

import re
import cv2
import numpy as np
import requests
from PIL import Image, ImageTk, Label

import DetectChars
import DetectPlates

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


# Function to send control signals to ESP32
def send_command(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent successfully: {url}")
            status_label.config(text=f"Command successful: {url}")
        else:
            print(f"Error: {response.status_code}")
            status_label.config(text=f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        status_label.config(text=f"Connection error: {e}")

# Function to display video stream from ESP32-CAM
def update_video():
    try:
        # Fetch the frame from ESP32-CAM
        img_resp = requests.get(url_cam)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        # Convert the frame to a format compatible with Tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the video label
        video_label.imgtk = imgtk
        video_label.config(image=imgtk)
    except Exception as e:
        print(f"Error in video stream: {e}")
        status_label.config(text=f"Video stream error: {e}")

    # Update the video every 30ms
    root.after(30, update_video)
