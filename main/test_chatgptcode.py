import cv2
import numpy as np
import pytesseract


# Hàm nhận diện biển số xe từ ảnh
def detect_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    plate_images = []
    for (x, y, w, h) in plates:
        # Vẽ khung xung quanh biển số phát hiện
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Cắt ảnh chứa biển số
        plate_images.append(gray[y:y + h, x:x + w])

    return image, plate_images


# Hàm xử lý ngưỡng cho ảnh
def preprocess_plate(plate_image):
    # Áp dụng GaussianBlur để giảm nhiễu
    imgBlurred = cv2.GaussianBlur(plate_image, (5, 5), 0)
    # Áp dụng ngưỡng (threshold) để tạo ảnh đen trắng
    _, imgThresh = cv2.threshold(imgBlurred, 150, 255, cv2.THRESH_BINARY_INV)
    return imgThresh


# Hàm nhận diện ký tự từ ảnh biển số
def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
    strChars = ""  # Chuỗi trả về các ký tự nhận diện được trong biển số

    height, width = imgThresh.shape
    imgThreshColor = np.zeros((height, width, 3), np.uint8)  # Ảnh màu

    listOfMatchingChars.sort(key=lambda matchingChar: matchingChar.intCenterX)  # Sắp xếp ký tự từ trái sang phải

    cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR, imgThreshColor)  # Chuyển ảnh sang màu

    # Duyệt qua từng ký tự trong biển số
    for currentChar in listOfMatchingChars:
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = (currentChar.intBoundingRectX + currentChar.intBoundingRectWidth,
               currentChar.intBoundingRectY + currentChar.intBoundingRectHeight)

        # Vẽ khung xanh quanh ký tự
        cv2.rectangle(imgThreshColor, pt1, pt2, (0, 255, 0), 2)

        # Cắt phần ảnh chứa ký tự
        imgROI = imgThresh[
                 currentChar.intBoundingRectY: currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
                 currentChar.intBoundingRectX: currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]

        # Nhận diện ký tự bằng Tesseract OCR
        config = '--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        char = pytesseract.image_to_string(imgROI, config=config)

        strChars += char.strip()  # Thêm ký tự vào chuỗi kết quả

    return strChars


# Hàm chính để nhận diện biển số từ ảnh
def process_image_for_plate_recognition(image):
    # Bước 1: Phát hiện biển số trong ảnh
    detected_image, plate_images = detect_license_plate(image)

    # Bước 2: Nhận diện ký tự từ từng biển số phát hiện được
    for plate_image in plate_images:
        # Tiền xử lý ảnh biển số
        imgThresh = preprocess_plate(plate_image)
        # Giả sử bạn đã có danh sách các ký tự tìm được trong biển số (ví dụ: từ kết quả contour detection)
        listOfMatchingChars = []  # Phần này bạn cần tùy chỉnh dựa trên thuật toán tìm contour của bạn

        # Bước 3: Nhận diện ký tự trong biển số
        plate_text = recognizeCharsInPlate(imgThresh, listOfMatchingChars)
        print("Ký tự biển số:", plate_text)

    # Hiển thị ảnh có khung biển số phát hiện
    cv2.imshow("Detected License Plates", detected_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Giả sử ảnh đầu vào
image = cv2.imread('image/image2.jpg')
process_image_for_plate_recognition(image)
