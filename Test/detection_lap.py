import cv2
import numpy as np
from datetime import datetime
import pytesseract
import re


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
def recognize_plate(plate_image):
    # PSM 8 là chế độ tốt nhất cho nhận diện ký tự đơn
    plate_text = pytesseract.image_to_string(plate_image, config='--psm 8')
    return plate_text.strip()


# Hàm để kiểm tra định dạng biển số xe hợp lệ
def is_valid_plate(plate_text):
    patterns = [
        r'^\d{2}[A-Z]{1}\s\d{3}\.\d{2}$',  # Pattern cho định dạng 1
        r'^\d{2}[A-Z]{1}\s\d{2,3}\.\d{2}$'  # Pattern cho định dạng 2
    ]
    return any(re.match(pattern, plate_text) for pattern in patterns)


# Hàm chính để chạy vòng lặp phát hiện biển số xe
def run_license_plate_detection():
    cap = cv2.VideoCapture(0)  # Mở camera mặc định của laptop
    detected_plates = []

    while True:
        ret, frame = cap.read()  # Đọc frame từ camera
        if not ret:
            break

        # Phát hiện và vẽ hộp bao quanh biển số xe
        frame, plate_images = detect_license_plate(frame)

        for plate_image in plate_images:
            plate_text = recognize_plate(plate_image)
            if plate_text and is_valid_plate(plate_text) and plate_text not in detected_plates:
                detected_plates.append(plate_text)
                print(f"Detected Plate: {plate_text} at {datetime.now()}")

        # Hiển thị hình ảnh
        cv2.imshow('detection', frame)
        key = cv2.waitKey(5)
        if key == ord('q'):  # Nhấn phím 'q' để thoát
            break

    cap.release()
    cv2.destroyAllWindows()


# Gọi hàm chính
run_license_plate_detection()
