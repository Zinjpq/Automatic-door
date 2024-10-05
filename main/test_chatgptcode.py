import cv2
import numpy as np
import pytesseract


# Hàm phát hiện biển số từ ảnh
def detect_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    plate_images = []
    for (x, y, w, h) in plates:
        # Vẽ khung xung quanh biển số
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Cắt vùng ảnh chứa biển số
        plate_images.append(gray[y:y + h, x:x + w])

    return image, plate_images


# Hàm tiền xử lý ảnh biển số (ngưỡng và Gaussian blur)
def preprocess_plate(plate_image):
    # Giảm nhiễu với GaussianBlur
    imgBlurred = cv2.GaussianBlur(plate_image, (5, 5), 0)
    # Áp dụng ngưỡng để có ảnh nhị phân (binary)
    _, imgThresh = cv2.threshold(imgBlurred, 150, 255, cv2.THRESH_BINARY_INV)
    return imgThresh


# Hàm tìm và lọc các contour ký tự từ biển số
def find_contours_of_chars(imgThresh):
    contours, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    listOfMatchingChars = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Lọc kích thước hợp lý của ký tự (giả định ký tự có tỷ lệ chiều cao và chiều rộng hợp lý)
        if w > 5 and h > 15 and h / w > 1.5 and h / w < 7:  # Bạn có thể điều chỉnh giá trị này
            matchingChar = {
                'intBoundingRectX': x,
                'intBoundingRectY': y,
                'intBoundingRectWidth': w,
                'intBoundingRectHeight': h,
                'intCenterX': x + (w // 2),
                'intCenterY': y + (h // 2)
            }
            listOfMatchingChars.append(matchingChar)

    return listOfMatchingChars


# Hàm nhận diện ký tự từ biển số
def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
    strChars = ""  # Chuỗi trả về các ký tự nhận diện được

    # Sắp xếp ký tự từ trái sang phải
    listOfMatchingChars.sort(key=lambda char: char['intCenterX'])

    for currentChar in listOfMatchingChars:
        # Lấy tọa độ của ký tự
        x, y, w, h = currentChar['intBoundingRectX'], currentChar['intBoundingRectY'], currentChar[
            'intBoundingRectWidth'], currentChar['intBoundingRectHeight']

        # Cắt phần ảnh chứa ký tự
        imgROI = imgThresh[y:y + h, x:x + w]

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

        # Bước 3: Tìm các contour ký tự
        listOfMatchingChars = find_contours_of_chars(imgThresh)

        # Bước 4: Nhận diện ký tự trong biển số
        plate_text = recognizeCharsInPlate(imgThresh, listOfMatchingChars)
        print("Ký tự biển số:", plate_text)

    # Hiển thị ảnh có khung biển số phát hiện
    cv2.imshow("Detected License Plates", detected_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Giả sử ảnh đầu vào
image = cv2.imread('image/image7.jpg')
process_image_for_plate_recognition(image)
