# import cv2
# import numpy as np
# import random
# import Main  # assuming Main contains necessary variables like showSteps, SCALAR_WHITE, SCALAR_RED
# import Preprocess
# import DetectChars

# def detectPlatesInScene(imgOriginalScene):
#     listOfPossiblePlates = []
#     height, width, numChannels = imgOriginalScene.shape

#     imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
#     imgThreshScene = np.zeros((height, width, 1), np.uint8)
#     imgContours = np.zeros((height, width, 3), np.uint8)

#     cv2.destroyAllWindows()

#     if Main.showSteps:
#         cv2.imshow("0", imgOriginalScene)

#     imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)

#     if Main.showSteps:
#         cv2.imshow("1a", imgGrayscaleScene)
#         cv2.imshow("1b", imgThreshScene)

#     listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)

#     if Main.showSteps:
#         print(f"step 2 - len(listOfPossibleCharsInScene) = {len(listOfPossibleCharsInScene)}")

#         imgContours = np.zeros((height, width, 3), np.uint8)
#         contours = [possibleChar.contour for possibleChar in listOfPossibleCharsInScene]
#         cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)
#         cv2.imshow("2b", imgContours)

#     listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

#     if Main.showSteps:
#         print(f"step 3 - listOfListsOfMatchingCharsInScene.Count = {len(listOfListsOfMatchingCharsInScene)}")

#         imgContours = np.zeros((height, width, 3), np.uint8)
#         for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
#             intRandomBlue, intRandomGreen, intRandomRed = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
#             contours = [matchingChar.contour for matchingChar in listOfMatchingChars]
#             cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
#         cv2.imshow("3", imgContours)

#     for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
#         possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)
#         if possiblePlate.imgPlate is not None:
#             listOfPossiblePlates.append(possiblePlate)

#     print(f"\n{len(listOfPossiblePlates)} possible plates found")

#     if Main.showSteps:
#         for i, possiblePlate in enumerate(listOfPossiblePlates):
#             p2fRectPoints = cv2.boxPoints(possiblePlate.rrLocationOfPlateInScene)
#             for j in range(4):
#                 cv2.line(imgContours, tuple(p2fRectPoints[j]), tuple(p2fRectPoints[(j+1) % 4]), Main.SCALAR_RED, 2)

#             cv2.imshow("4a", imgContours)
#             cv2.imshow("4b", possiblePlate.imgPlate)
#             cv2.waitKey(0)

#         print("\nplate detection complete, click on any image and press a key to begin char recognition.\n")
#         cv2.waitKey(0)

#     return listOfPossiblePlates

# # Video Stream Processing for ESP32-CAM
# def processESP32CamStream(stream_url):
#     cap = cv2.VideoCapture(stream_url)

#     if not cap.isOpened():
#         print("Error: Unable to open the video stream.")
#         return

#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             print("Failed to grab frame.")
#             break

#         possiblePlates = detectPlatesInScene(frame)

#         for plate in possiblePlates:
#             cv2.imshow('Detected Plate', plate.imgPlate)

#         # Press 'q' to exit video processing
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # Example ESP32-CAM video stream URL (adjust the IP address to match your ESP32-CAM)
# esp32_cam_url = "http://192.168.1.100:81/stream"
# processESP32CamStream(esp32_cam_url)









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

# DetectChars.py










# import os

# import cv2
# import numpy as np
# import math
# import random

# import Main
# import Preprocess
# import PossibleChar

# # DetectChars.py
# import os

# import cv2
# import numpy as np
# import math
# import random

# import Main
# import Preprocess
# import PossibleChar
# import DetectPlates
# import DetectChars

# # module level variables ##########################################################################

# kNearest = cv2.ml.KNearest_create()

#         # constants for checkIfPossibleChar, this checks one possible char only (does not compare to another char)
# MIN_PIXEL_WIDTH = 2
# MIN_PIXEL_HEIGHT = 8

# MIN_ASPECT_RATIO = 0.25
# MAX_ASPECT_RATIO = 1.0

# MIN_PIXEL_AREA = 80

#         # constants for comparing two chars
# MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
# MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

# MAX_CHANGE_IN_AREA = 0.5

# MAX_CHANGE_IN_WIDTH = 0.8
# MAX_CHANGE_IN_HEIGHT = 0.2

# MAX_ANGLE_BETWEEN_CHARS = 12.0

#         # other constants
# MIN_NUMBER_OF_MATCHING_CHARS = 3

# RESIZED_CHAR_IMAGE_WIDTH = 20
# RESIZED_CHAR_IMAGE_HEIGHT = 30

# MIN_CONTOUR_AREA = 100

# ###################################################################################################
# def loadKNNDataAndTrainKNN():
#     allContoursWithData = []                # declare empty lists,
#     validContoursWithData = []              # we will fill these shortly

#     try:
#         npaClassifications = np.loadtxt("classifications.txt", np.float32)                  # read in training classifications
#     except:                                                                                 # if file could not be opened
#         # print("error, unable to open classifications.txt, exiting program\n")  # show error message
#         os.system("pause")
#         return False                                                                        # and return False
#     # end try

#     try:
#         npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)                 # read in training images
#     except:                                                                                 # if file could not be opened
#         # print("error, unable to open flattened_images.txt, exiting program\n")  # show error message
#         os.system("pause")
#         return False                                                                        # and return False
#     # end try

#     npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # reshape numpy array to 1d, necessary to pass to call to train

#     kNearest.setDefaultK(1)                                                             # set default K to 1

#     kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)           # train KNN object

#     return True                             # if we got here training was successful so return true
# # end function

# ###################################################################################################

# def detect_Plates_In_Scene(imgOriginalScene):
#     listOfPossiblePlates = []                   # this will be the return value

#     height, width, numChannels = imgOriginalScene.shape

#     imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
#     imgThreshScene = np.zeros((height, width, 1), np.uint8)
#     imgContours = np.zeros((height, width, 3), np.uint8)

#     imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)         # preprocess to get grayscale and threshold images

#     listOfPossibleCharsInScene = DetectPlates.findPossibleCharsInScene(imgThreshScene)
#     listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)
#     for listOfMatchingChars in listOfListsOfMatchingCharsInScene:                   # for each group of matching chars
#         possiblePlate = DetectPlates.extractPlate(imgOriginalScene, listOfMatchingChars)         # attempt to extract plate

#         if possiblePlate.imgPlate is not None:                          # if plate was found
#             listOfPossiblePlates.append(possiblePlate)                  # add to list of possible plates
#         # end if
#     # end for
    
#     return listOfPossiblePlates

# def detect_Chars_In_Plates(possiblePlate):
#     intPlateCounter = 0
#     imgcontours = None
#     contours = []

#     possiblePlate.imgGrayscale, possiblePlate.imgThresh = Preprocess.preprocess(possiblePlate.imgPlate)     # preprocess to get grayscale and threshold images

#     possiblePlate.imgThresh = cv2.resize(possiblePlate.imgThresh, (0, 0), fx = 1.6, fy = 1.6)
#     thresholdValue, possiblePlate.imgThresh = cv2.threshold(possiblePlate.imgThresh, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#     listOfPossibleCharsInPlate = DetectPlates.findPossibleCharsInPlate(possiblePlate.imgGrayscale, possiblePlate.imgThresh)
#     listOfListsOfMatchingCharsInPlate = DetectPlates.findListOfListsOfMatchingChars(listOfPossibleCharsInPlate)
#     if (len(listOfListsOfMatchingCharsInPlate) == 0):			# if no groups of matching chars were found in the plate
#         possiblePlate.strChars = ""
#         # continue
#     for i in range(0, len(listOfListsOfMatchingCharsInPlate)):                              # within each list of matching chars
#         listOfListsOfMatchingCharsInPlate[i].sort(key = lambda matchingChar: matchingChar.intCenterX)        # sort chars from left to right
#         listOfListsOfMatchingCharsInPlate[i] = DetectPlates.removeInnerOverlappingChars(listOfListsOfMatchingCharsInPlate[i])              # and remove inner overlapping chars
#         # end for
#     intLenOfLongestListOfChars = 0
#     intIndexOfLongestListOfChars = 0

#     # loop through all the vectors of matching chars, get the index of the one with the most chars
#     for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
#         if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfLongestListOfChars:
#             intLenOfLongestListOfChars = len(listOfListsOfMatchingCharsInPlate[i])
#             intIndexOfLongestListOfChars = i
#         # end if
#     # end for
#     # suppose that the longest list of matching chars within the plate is the actual list of chars
#     longestListOfMatchingCharsInPlate = listOfListsOfMatchingCharsInPlate[intIndexOfLongestListOfChars]

#     possiblePlate.strChars = DetectPlates.recognizeCharsInPlate(possiblePlate.imgThresh, longestListOfMatchingCharsInPlate)
    
#     return possiblePlate






# import threading
# import time
# import tkinter as tk

# import cv2
# import numpy as np
# import qrcode
# import requests
# from PIL import Image, ImageTk

# import DetectChars
# import DetectPlates

# # ESP32-CAM URL and Control URLs
# url_or = 'http://192.168.3.61'

# url_cam = url_or + '/cam'
# url1 = url_or + '/left'
# url2 = url_or + '/right'
# url3 = url_or + '/up'
# url4 = url_or + '/down'

# def generate_qr(data):
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr.add_data(data)
#     qr.make(fit=True)
#     img = qr.make_image(fill='black', back_color='white')
#     return ImageTk.PhotoImage(img)


# class ESP32CamApp:
#     def __init__(self, root):
#         self.status_label_1 = None
#         self.status_label_2 = None
#         self.video_label = None
#         self.root = root
#         self.root.title("ESP32-CAM Setup")
#         self.root.geometry("1280x720")

#         # ESP32-CAM URLs
#         self.url_Original = 'http://192.168.1.100'
#         self.url_cam = self.url_Original + '/cam'
#         self.url1 = self.url_Original + '/left'
#         self.url2 = self.url_Original + '/right'
#         self.url3 = self.url_Original + '/up'
#         self.url4 = self.url_Original + '/down'

#         # Initialize scenes
#         self.scene_1_frame = tk.Frame(self.root)
#         self.scene_2_frame = tk.Frame(self.root)

#         self.create_scene_1()  # Create the first scene
#         self.create_scene_2()  # Pre-create the second scene, but keep it hidden

#         # Start checking for connection
#         threading.Thread(target=self.check_connection, daemon=True).start()

#     # Scene 1: Connection instructions
#     def create_scene_1(self):
#         self.scene_1_frame.pack(fill="both", expand=True)

#         self.status_label_1 = tk.Label(self.scene_1_frame, text="Chưa kết nối với ESP32-CAM", font=("Arial", 16))
#         self.status_label_1.pack(pady=20)

#         ssid_label = tk.Label(self.scene_1_frame, text="SSID: ESP32-CAM", font=("Arial", 14))
#         ssid_label.pack()

#         password_label = tk.Label(self.scene_1_frame, text="Password: 123456789", font=("Arial", 14))
#         password_label.pack()

#         qr_label = tk.Label(self.scene_1_frame)
#         qr_label.pack(pady=10)
#         qr_img = generate_qr('http://192.168.4.1')
#         qr_label.config(image=qr_img)
#         qr_label.image = qr_img  # Keep a reference to avoid garbage collection

#         access_point_label = tk.Label(self.scene_1_frame, text="Kết nối vào http://192.168.4.1", font=("Arial", 14))
#         access_point_label.pack(pady=20)

#     # Scene 2: Video stream and controls
#     def create_scene_2(self):
#         video_label = tk.Label(self.scene_2_frame)
#         video_label.pack(fill="both", expand=True)

#         self.status_label_2 = tk.Label(self.scene_2_frame, text="Status: ", font=("Arial", 12))
#         self.status_label_2.pack(side="bottom", fill="x")

#         button_frame = tk.Frame(self.scene_2_frame)
#         button_frame.pack(side="bottom", pady=10)

#         tk.Button(button_frame, text="Left", command=lambda: self.send_command(self.url1)).grid(row=0, column=0)
#         tk.Button(button_frame, text="Right", command=lambda: self.send_command(self.url2)).grid(row=0, column=2)
#         tk.Button(button_frame, text="Up", command=lambda: self.send_command(self.url3)).grid(row=0, column=1)
#         tk.Button(button_frame, text="Down", command=lambda: self.send_command(self.url4)).grid(row=1, column=1)

#         self.video_label = video_label

#     # Function to switch to Scene 2
#     def switch_to_scene_2(self):
#         self.scene_1_frame.pack_forget()  # Hide Scene 1
#         self.scene_2_frame.pack(fill="both", expand=True)  # Show Scene 2
#         self.update_video()  # Start video stream update

#     # Check ESP32-CAM connection
#     def check_connection(self):
#         while True:
#             try:
#                 response = requests.get(url_or, timeout=1)
#                 if response.status_code == 200:
#                     self.status_label_1.config(text="Kết nối thành công với ESP32-CAM!")
#                     self.switch_to_scene_2()
#                     break
#             except requests.exceptions.RequestException:
#                 self.status_label_1.config(text="Chưa kết nối được với ESP32-CAM...")
#             time.sleep(2)

#     # Generate QR Code

#     # Send control commands to ESP32-CAM
#     def send_command(self, url):
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 self.status_label_2.config(text=f"Command successful: {url}")
#             else:
#                 self.status_label_2.config(text=f"Error: {response.status_code}")
#         except requests.exceptions.RequestException as e:
#             self.status_label_2.config(text=f"Connection error: {e}")

#     # Update video stream from ESP32-CAM
#     def update_video(self):
#         try:
#             img_resp = requests.get(self.url_cam)
#             img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
#             frame = cv2.imdecode(img_arr, -1)
#             img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(img)
#             imgtk = ImageTk.PhotoImage(image=img)
#             self.video_label.imgtk = imgtk
#             self.video_label.config(image=imgtk)
#         except Exception as e:
#             self.status_label_2.config(text=f"Video stream error: {e}")
#         self.root.after(30, self.update_video)

#     def anpr(self):
#         while True:
#             try:
#                 imgOriginalScene = requests.get(self.url_cam)
#                 listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates
#                 DetectChars.detectCharsInPlates(listOfPossiblePlates)

#             except Exception as e:
#                 print(f"Error: {e}")
