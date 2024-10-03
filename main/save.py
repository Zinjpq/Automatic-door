import cv2
import numpy as np
import random
import Main  # assuming Main contains necessary variables like showSteps, SCALAR_WHITE, SCALAR_RED
import Preprocess
import DetectChars

def detectPlatesInScene(imgOriginalScene):
    listOfPossiblePlates = []
    height, width, numChannels = imgOriginalScene.shape

    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
    imgThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if Main.showSteps:
        cv2.imshow("0", imgOriginalScene)

    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)

    if Main.showSteps:
        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)

    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)

    if Main.showSteps:
        print(f"step 2 - len(listOfPossibleCharsInScene) = {len(listOfPossibleCharsInScene)}")

        imgContours = np.zeros((height, width, 3), np.uint8)
        contours = [possibleChar.contour for possibleChar in listOfPossibleCharsInScene]
        cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)
        cv2.imshow("2b", imgContours)

    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

    if Main.showSteps:
        print(f"step 3 - listOfListsOfMatchingCharsInScene.Count = {len(listOfListsOfMatchingCharsInScene)}")

        imgContours = np.zeros((height, width, 3), np.uint8)
        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            intRandomBlue, intRandomGreen, intRandomRed = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            contours = [matchingChar.contour for matchingChar in listOfMatchingChars]
            cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
        cv2.imshow("3", imgContours)

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)
        if possiblePlate.imgPlate is not None:
            listOfPossiblePlates.append(possiblePlate)

    print(f"\n{len(listOfPossiblePlates)} possible plates found")

    if Main.showSteps:
        for i, possiblePlate in enumerate(listOfPossiblePlates):
            p2fRectPoints = cv2.boxPoints(possiblePlate.rrLocationOfPlateInScene)
            for j in range(4):
                cv2.line(imgContours, tuple(p2fRectPoints[j]), tuple(p2fRectPoints[(j+1) % 4]), Main.SCALAR_RED, 2)

            cv2.imshow("4a", imgContours)
            cv2.imshow("4b", possiblePlate.imgPlate)
            cv2.waitKey(0)

        print("\nplate detection complete, click on any image and press a key to begin char recognition.\n")
        cv2.waitKey(0)

    return listOfPossiblePlates

# Video Stream Processing for ESP32-CAM
def processESP32CamStream(stream_url):
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("Error: Unable to open the video stream.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break

        possiblePlates = detectPlatesInScene(frame)

        for plate in possiblePlates:
            cv2.imshow('Detected Plate', plate.imgPlate)

        # Press 'q' to exit video processing
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example ESP32-CAM video stream URL (adjust the IP address to match your ESP32-CAM)
esp32_cam_url = "http://192.168.1.100:81/stream"
processESP32CamStream(esp32_cam_url)



# import cv2
#
# import DetectChars
# import DetectPlates
#
# # module level variables ##########################################################################
# SCALAR_BLACK = (0.0, 0.0, 0.0)
# SCALAR_WHITE = (255.0, 255.0, 255.0)
# SCALAR_YELLOW = (0.0, 255.0, 255.0)
# SCALAR_GREEN = (0.0, 255.0, 0.0)
# SCALAR_RED = (0.0, 0.0, 255.0)
#
# showSteps = False
#
#
# # Hàm để phát hiện và vẽ hộp bao quanh biển số xe
# def detect_license_plate(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
#     plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#
#     plate_images = []
#     for (x, y, w, h) in plates:
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         plate_images.append(gray[y:y + h, x:x + w])
#
#     return image, plate_images
#
#
# # blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()
#
#
# # Hàm chính để chạy vòng lặp phát hiện biển số xe
# def run_license_plate_detection():
#     cap = cv2.VideoCapture(0)  # Mở camera mặc định của laptop
#
#     while True:
#         ret, imgOriginalScene = cap.read()  # Đọc frame từ camera
#         if not ret:
#             break
#
#         listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates
#         listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates
#         listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
#         licPlate = listOfPossiblePlates[0]
#         cv2.imshow("imgPlate", licPlate.imgPlate)  # show crop of plate and threshold of plate
#         # cv2.imshow("imgThresh", licPlate.imgThresh)
#         print(licPlate.strChars)
#
#         # Hiển thị hình ảnh
#         cv2.imshow('detection', imgOriginalScene)
#         key = cv2.waitKey(5)
#         if key == ord('q'):  # Nhấn phím 'q' để thoát
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#
# # Gọi hàm chính
# run_license_plate_detection()
