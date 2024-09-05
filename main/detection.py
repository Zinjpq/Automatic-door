import urllib.request  # Thêm thư viện urllib để gửi yêu cầu HTTP
import cv2  # Thêm thư viện OpenCV
# import cvlib as cv  # Thêm thư viện cvlib
import numpy as np  # Thêm thư viện numpy
# from cvlib.object_detection import draw_bbox  # Thêm hàm draw_bbox từ cvlib
import pytesseract 
 
# URL của hình ảnh từ camera
url = 'http://192.168.3.56/stream'
im = None


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
    plate_text = pytesseract.image_to_string(plate_image,config='--psm 8')
    return plate_text.strip()


def run():
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)
    while True:
        # Gửi yêu cầu HTTP để lấy hình ảnh từ URL
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)

        ret, frame = im.read()  # Đọc frame từ camera
        if not ret:
            break

        # Phát hiện và vẽ hộp bao quanh biển số xe
        frame, plate_images = detect_license_plate(frame)

        # for plate_image in plate_images:
        #     plate_text = recognize_plate(plate_image)
        #     if plate_text and is_valid_plate(plate_text) and plate_text not in detected_plates:
        #         detected_plates.append(plate_text)
        #         print(f"Detected Plate: {plate_text} at {datetime.now()}")

        # Hiển thị hình ảnh với các hộp bao quanh đối tượng
        cv2.imshow('detection', im)
        key = cv2.waitKey(5)
        if key == ord('q'):  # Nhấn phím 'q' để thoát
            break

    im.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("started")
    run()
