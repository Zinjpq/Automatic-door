import cv2
import pytesseract
from datetime import datetime
import os

# Hàm xử lý nhận diện biển số
def recognize_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    license_plate = pytesseract.image_to_string(gray, config='--psm 8')
    return license_plate.strip()

# Kiểm tra biển số hợp lệ
def is_valid_license_plate(license_plate):
    # Ví dụ: kiểm tra định dạng biển số Việt Nam
    return bool(re.match(r'[0-9]{2}[A-Z]{1,2}[0-9]{4,5}', license_plate))

# Thiết lập folder để lưu ảnh
output_folder = 'detected_plates'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Khởi động camera (giả sử sử dụng OpenCV với ESP32-CAM)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Nhận diện biển số
    license_plate = recognize_license_plate(frame)
    print(f"Detected License Plate: {license_plate}")

    # Nếu biển số hợp lệ
    if is_valid_license_plate(license_plate):
        # Lấy thời gian hiện tại
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Lưu ảnh kèm thời gian vào folder
        filename = os.path.join(output_folder, f'{license_plate}_{timestamp}.jpg')
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")

    # Thoát vòng lặp nếu nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
