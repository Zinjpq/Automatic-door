import library
import cv2
from datetime import datetime

url = 'http://192.168.1.15/cam-hi.jpg'
detected_plates = []

# Or image: 
# image = cv2.imread('image5.jpg')


while True:
    image = library.read_url(url)
    # Phát hiện và vẽ hộp bao quanh biển số xe
    image, plate_images = library.detect_license_plate(image)

    for plate_image in plate_images:
        plate_text = library.recognize_plate(plate_image, "pytesseract")
        print(plate_text)
        if plate_text and library.check_plate(plate_text) and plate_text not in detected_plates:
            detected_plates.append(plate_text)
            print(f"Detected Plate: {plate_text} at {datetime.now()}")
    if library.check_plate(plate_text):
        print('Plate detected')
        library.save_image(plate_images, '.jpg')

    cv2.namedWindow("Automatic Door", cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Automatic Door', image)

    # text = library.easy_ocr(crop)
    # print(text)
    # if library.check_plate(text):
    #     print('Plate detected')
    #     library.save_image(text, '.jpg')

    key = cv2.waitKey(5)
    if key == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
