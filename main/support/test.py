import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import time

# Hàm lấy luồng video từ ESP32-CAM
def update_video():
    ret, frame = cap.read()
    if ret:
        # Chuyển đổi frame từ OpenCV sang định dạng Tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.config(image=imgtk)
    # Gọi lại hàm sau 10ms để cập nhật video
    root.after(10, update_video)

# Hàm cập nhật biển số và thời gian (giả định)
def update_plate_info():
    # Giả lập biển số nhận dạng
    license_plate = "30E-12345"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    plate_label.config(text=f"Biển số: {license_plate}")
    time_label.config(text=f"Thời gian: {timestamp}")
    
    # Cập nhật thông tin biển số sau 5 giây
    root.after(5000, update_plate_info)

# Khởi tạo cửa sổ Tkinter
root = tk.Tk()
root.geometry("1440x1024")

# Tạo label để hiển thị video
video_label = Label(root)
video_label.pack(side="top", fill="both", expand=True)

# Tạo label hiển thị biển số xe
plate_label = Label(root, text="Biển số: ", font=("Arial", 20))
plate_label.pack(side="left", padx=10, pady=10)

# Tạo label hiển thị thời gian
time_label = Label(root, text="Thời gian: ", font=("Arial", 20))
time_label.pack(side="right", padx=10, pady=10)

# Kết nối tới ESP32-CAM (thay bằng địa chỉ IP thực của ESP32-CAM)
# esp32_url = "http://192.168.1.100:81/stream"
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(esp32_url)

# Gọi hàm cập nhật video
update_video()

# Gọi hàm cập nhật thông tin biển số
update_plate_info()

# Chạy giao diện
root.mainloop()

# Giải phóng camera khi tắt ứng dụng
cap.release()
cv2.destroyAllWindows()
