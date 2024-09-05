import re
import time
import urllib.request
import cv2
import easyocr
import pytesseract
import numpy as np
from matplotlib import pyplot as plt


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


# Hàm để nhận diện ký tự trong biển số xe
def recognize_plate(plate_image, method):
    if method == "pytesseract":
        # PSM 8 là chế độ tốt nhất cho nhận diện ký tự đơn
        plate_text = pytesseract.image_to_string(plate_image, config='--psm 8')
        return plate_text.strip()
    elif method == "easyocr":
        reader = easyocr.Reader(['en'])
        results = reader.readtext(plate_image)
        plate_text = ''.join([result[1] for result in results])
        return plate_text.strip()
    else:
        raise ValueError("Phương pháp không hợp lệ. Vui lòng chọn 'pytesseract' hoặc 'easyocr'.")
