import re
import os
import time
import cv2

from src.DetectPlateImage import DetectPlates, DetectChars
from src.Communication.http_esp32 import sent_door_state

# Biến lưu trữ biển số và thời gian lưu
last_saved_plates = {}


def Detect_License_Plate(imgOriginalScene):
    # Tải và huấn luyện KNN nếu chưa làm
    DetectChars.loadKNNDataAndTrainKNN()

    # Phát hiện biển số trong ảnh
    listOfPossiblePlates, imgGrayscaleScene, imgThreshScene = DetectPlates.detectPlatesInScene(imgOriginalScene)

    # Phát hiện ký tự trong biển số
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    # Kiểm tra nếu có biển số khả thi
    if len(listOfPossiblePlates) != 0:
        # Sắp xếp các biển số khả thi theo số lượng ký tự nhận diện được (từ dài nhất đến ngắn nhất)
        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

        # Giả sử biển số có nhiều ký tự nhất là biển số thực sự
        licPlate = listOfPossiblePlates[0]

        # Kiểm tra nếu chuỗi biển số khớp với mẫu (2 số + 1 chữ cái + 5 số)
        pattern = r"^\d{2}[A-Z]\d{5}$"  # 2 chữ số đầu + 1 chữ cái + 5 chữ số
        if re.match(pattern, licPlate.strChars):
            print(licPlate.strChars)  # In biển số ra console

            # Đọc danh sách biển số từ file plate.txt
            with open('plate.txt', 'r') as file:
                valid_plates = file.read().splitlines()  # Đọc tất cả các biển số trong file plate.txt

            # Kiểm tra xem biển số nhận diện có khớp với biển số trong file không
            if licPlate.strChars in valid_plates:
                sent_door_state(1)
                print(f"Plate {licPlate.strChars} is valid. Checking for recent save...")

                current_time = time.time()  # Lấy thời gian hiện tại (theo giây)

                # Kiểm tra xem biển số này có được lưu trong vòng 10 giây qua không
                if licPlate.strChars in last_saved_plates:
                    last_save_time = last_saved_plates[licPlate.strChars]
                    time_difference = current_time - last_save_time

                    if time_difference <= 10:
                        print(f"Plate {licPlate.strChars} was saved recently. Skipping save.")
                        return  # Dừng lại và không lưu nếu thời gian giữa các lần lưu không quá 10 giây

                # Lấy ảnh biển số từ đối tượng licPlate
                imgPlate = licPlate.imgPlate

                # Tạo thư mục nếu chưa tồn tại
                output_dir = 'Detectedplate'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Lấy thời gian hiện tại để đặt tên file
                current_time_str = time.strftime("%d%m%Y_%H%M%S")

                # Tạo tên file là biển số + giờ
                file_name = os.path.join(output_dir, f"{current_time_str}_{licPlate.strChars}.png")

                # Lưu ảnh biển số vào thư mục
                cv2.imwrite(file_name, imgPlate)
                print(f"Saved detected plate image as {file_name}")

                # Cập nhật thời gian lưu của biển số này
                last_saved_plates[licPlate.strChars] = current_time

            else:
                print(f"Plate {licPlate.strChars} is not valid. Not saving image.")
