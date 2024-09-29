import re
import time
import urllib.request
import cv2
import numpy as np
import os

import DetectChars
import DetectPlates
import PossiblePlate

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

# Hàm kiểm tra biển số xe có hợp lệ không
def check_plate(plate_text):
    patterns = [
        r'^\d{2}[A-Z]{1}\s\d{3}\d{2}$',  # Pattern cho định dạng 1
        r'^\d{2}[A-Z]{1}\s\d{2,3}\d{2}$'  # Pattern cho định dạng 2
    ]
    return any(re.match(pattern, plate_text) for pattern in patterns)


# cach dung cua ham tren
# for plate_image in plate_images:
#             plate_text = recognize_plate(plate_image)
#             if plate_text and is_valid_plate(plate_text) and plate_text not in detected_plates:
#                 detected_plates.append(plate_text)
#                 print(f"Detected Plate: {plate_text} at {datetime.now()}")

# Hàm đọc ảnh từ URL
def read_url(url):
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    image = cv2.imdecode(imgnp, -1)
    return image


# Hàm lưu ảnh
def save_image(image, file_path):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_name = f"{timestamp}_{file_path}"
    cv2.imwrite(file_name, image)

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
