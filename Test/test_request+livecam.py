import requests
import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import time
import numpy as np

# ESP32-CAM URL and Control URLs
url_or = 'http://192.168.3.61'
url_cam = url_or + '/cam'
url1 = url_or + '/left'
url2 = url_or + '/right'
url3 = url_or + '/up'
url4 = url_or + '/down'


# Function to send control signals to ESP32
def send_command(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command sent successfully: {url}")
            status_label.config(text=f"Command successful: {url}")
        else:
            print(f"Error: {response.status_code}")
            status_label.config(text=f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        status_label.config(text=f"Connection error: {e}")


# Function to display video stream from ESP32-CAM
def update_video():
    try:
        # Fetch the frame from ESP32-CAM
        img_resp = requests.get(url_cam)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        # Convert the frame to a format compatible with Tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the video label
        video_label.imgtk = imgtk
        video_label.config(image=imgtk)
    except Exception as e:
        print(f"Error in video stream: {e}")
        status_label.config(text=f"Video stream error: {e}")

    # Update the video every 30ms
    root.after(30, update_video)


# Function to update the license plate information
def update_plate_info():
    # Simulate license plate recognition (replace with actual logic)
    license_plate = "30E-12345"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    plate_label.config(text=f"License Plate: {license_plate}")
    time_label.config(text=f"Timestamp: {timestamp}")

    # Update license plate info every 5 seconds
    root.after(5000, update_plate_info)


# Initialize Tkinter window
root = tk.Tk()
root.title("ESP32-CAM Control & Video Stream")
root.geometry("800x600")

# Create a label for the video stream
video_label = Label(root)
video_label.pack(side="top", fill="both", expand=True)

# Create status label for command responses
status_label = Label(root, text="Status: ", font=("Arial", 12))
status_label.pack(side="bottom", fill="x")

# Create license plate and timestamp labels
plate_label = Label(root, text="License Plate: ", font=("Arial", 20))
plate_label.pack(side="left", padx=10, pady=10)

time_label = Label(root, text="Timestamp: ", font=("Arial", 20))
time_label.pack(side="right", padx=10, pady=10)

# Add buttons to control ESP32-CAM
button_frame = tk.Frame(root)
button_frame.pack(side="bottom", pady=10)

# Direction control buttons
Button(button_frame, text="Left", command=lambda: send_command(url1)).grid(row=0, column=0)
Button(button_frame, text="Right", command=lambda: send_command(url2)).grid(row=0, column=2)
Button(button_frame, text="Up", command=lambda: send_command(url3)).grid(row=0, column=1)
Button(button_frame, text="Down", command=lambda: send_command(url4)).grid(row=1, column=1)

# Start updating video and license plate info
update_video()
update_plate_info()

# Start the Tkinter main loop
root.mainloop()

# import requests
# import cv2  # Nếu bạn vẫn muốn sử dụng cv2
#
# # Địa chỉ IP của ESP32-CAM (thay đổi thành IP thực của ESP32 sau khi kết nối WiFi)
# url1 = 'http://192.168.3.56/left'
# url2 = 'http://192.168.3.56/right'
# url3 = 'http://192.168.3.56/up'
# url4 = 'http://192.168.3.56/down'
# url_cam = 'http://192.168.0.103/cam'
#
#
# # Hiển thị hướng dẫn sử dụng
# print("Nhấn 1 để mở cửa, 2 để đóng cửa, q để thoát")
#
# # Tạo một cửa sổ trống nếu bạn cần sử dụng cv2.waitKey()
# cv2.namedWindow("ESP32 Control", cv2.WINDOW_NORMAL)
# cv2.imshow("ESP32 Control", 255 * 1)  # Hiển thị cửa sổ trống
#
# while True:
#     key = cv2.waitKey(1)  # Thời gian chờ ngắn hơn
#     if key == ord('1'):  # Nhấn phím '1' để gửi tín hiệu mở cửa
#         try:
#             response1 = requests.get(url1)
#             if response1.status_code == 200:
#                 print("Tín hiệu đã gửi thành công!")
#                 print("Phản hồi từ ESP32:", response1.text)  # In ra phản hồi từ ESP32-CAM
#             else:
#                 print(f"Lỗi: {response1.status_code}")
#         except requests.exceptions.RequestException as e:
#             print(f"Lỗi kết nối: {e}")
#
#     elif key == ord('2'):  # Nhấn phím '2' để gửi tín hiệu đóng cửa
#         try:
#             response2 = requests.get(url2)
#             if response2.status_code == 200:
#                 print("Tín hiệu đã gửi thành công!")
#                 print("Phản hồi từ ESP32:", response2.text)  # In ra phản hồi từ ESP32-CAM
#             else:
#                 print(f"Lỗi: {response2.status_code}")
#         except requests.exceptions.RequestException as e:
#             print(f"Lỗi kết nối: {e}")
#     elif key == ord('3'):  # Nhấn phím '2' để gửi tín hiệu đóng cửa
#         try:
#             response2 = requests.get(url3)
#             if response2.status_code == 200:
#                 print("Tín hiệu đã gửi thành công!")
#                 print("Phản hồi từ ESP32:", response2.text)  # In ra phản hồi từ ESP32-CAM
#             else:
#                 print(f"Lỗi: {response2.status_code}")
#         except requests.exceptions.RequestException as e:
#             print(f"Lỗi kết nối: {e}")
#
#     elif key == ord('4'):  # Nhấn phím '2' để gửi tín hiệu đóng cửa
#         try:
#             response2 = requests.get(url4)
#             if response2.status_code == 200:
#                 print("Tín hiệu đã gửi thành công!")
#                 print("Phản hồi từ ESP32:", response2.text)  # In ra phản hồi từ ESP32-CAM
#             else:
#                 print(f"Lỗi: {response2.status_code}")
#         except requests.exceptions.RequestException as e:
#             print(f"Lỗi kết nối: {e}")
#
#     elif key == ord('q'):  # Nhấn phím 'q' để thoát
#         print("Thoát chương trình")
#         break
#
# # Đóng cửa sổ OpenCV nếu có
# cv2.destroyAllWindows()
