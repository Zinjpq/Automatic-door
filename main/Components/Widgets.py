import os
import re
import threading
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import Button, PhotoImage, Label, messagebox, Frame, Canvas, ttk
import cv2
import numpy as np
import requests
from PIL import Image, ImageTk

from main.DetectPlateImage.MainDetectPlate import Detect_License_Plate


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent.parent / "assets"
    return ASSETS_PATH / Path(path)

class LivestreamWidget(Frame):
    def __init__(self, parent, camera_url):
        super().__init__(parent, bg="#000000", width=640, height=480)
        self.camera_url = camera_url
        self.canvas = Canvas(self, bg="#000000", width=640, height=480, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.error_label = Label(self, bg="#F2F4F8")
        self.error_image = ImageTk.PhotoImage(file=relative_to_assets("image_Cameraerror.png"))
        self.error_label.config(image=self.error_image)
        self.error_label.place(x=0, y=0)
        self.error_label.lower()

        self.running = True
        threading.Thread(target=self.stream_video, daemon=True).start()

    def stream_video(self):
        while self.running:
            try:
                start_time = time.time()

                # Tải ảnh từ camera
                img_resp = requests.get(self.camera_url, timeout=2)
                img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

                FrameWithPlates, plate_images  = detect_license_plate(frame)
                Detect_License_Plate(frame)
                FrameWithPlates = cv2.resize(FrameWithPlates, (640,480))

                # Resize để giảm tải hệ thống
                frame = cv2.resize(FrameWithPlates, (640, 480))
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Chuyển ảnh thành PhotoImage
                photo = ImageTk.PhotoImage(image=Image.fromarray(img))

                # Cập nhật Canvas trong main thread
                self.canvas.after(0, self.update_canvas, photo)
                self.error_label.lower()

                # Giới hạn FPS (khoảng 10-15 FPS)
                elapsed = time.time() - start_time
                time.sleep(max(0.1 - elapsed, 0))  # Tối thiểu 100ms giữa các khung hình

            except Exception:
                self.canvas.after(0, self.show_camera_error)

    def update_canvas(self, photo):
        self.canvas.create_image(0, 0, anchor="nw", image=photo)
        self.canvas.image = photo

    def show_camera_error(self):
        self.error_label.lift()
        self.canvas.delete("all")

    def stop(self):
        self.running = False

def detect_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    plate_images = []
    for (x, y, w, h) in plates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        plate_images.append(gray[y:y + h, x:x + w])

    return image, plate_images

def create_button(image_path, parent, command, x, y, width, height):
    button_image = PhotoImage(file=relative_to_assets(image_path))
    button = Button(parent, image=button_image, borderwidth=0, highlightthickness=0, relief="flat",
                            command=command)
    button.image = button_image  # Keep a reference to avoid garbage collection
    button.place(x=x, y=y, width=width, height=height)


def add_image(image_path, parent, x=0, y=0):
    image = PhotoImage(file=relative_to_assets(image_path))
    label = Label(parent, image=image, bg=parent['bg'])
    label.image = image  # Giữ tham chiếu để tránh bị xoá
    label.place(x=x, y=y)


# Function to create time and date labels
def create_time_and_date_labels(parent, time_coords, date_coords, font, color="#000000"):
    # Create labels for time and date
    time_label = Label(parent, text="", font=font, fg=color, bg=parent["bg"])
    time_label.place(x=time_coords[0] - 256, y=time_coords[1])

    date_label = Label(parent, text="", font=font, fg=color, bg=parent["bg"])
    date_label.place(x=date_coords[0] - 256, y=date_coords[1])

    # Function to update time and date
    def update_time_and_date():
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")
        time_label.config(text=current_time)
        date_label.config(text=current_date)
        time_label.after(1000, update_time_and_date)  # Update every second

    update_time_and_date()

def SavePlaceWithTime(image: Image.Image, beach_name: str):
    output_dir = Path(__file__).parent / "images"
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_name = f"{beach_name}_{current_time}.jpg"
    output_dir.mkdir(parents=True, exist_ok=True)
    image_path = output_dir / image_name
    image.save(image_path)
    # print(f"Ảnh đã được lưu tại: {image_path}")


class AddLicensePlateText(Frame):
    def __init__(self, parent,plate_file):
        super().__init__(parent,width=336, height=480)
        self.pack_propagate(False)
        self.plate_file = plate_file
        # Tiêu đề phía trên
        self.title_label = tk.Label(self, text="Tên biển hợp lệ", bg="lightgray", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Frame cuộn
        self.scroll_frame = tk.Frame(self, bg="white")
        self.scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas để hỗ trợ cuộn
        self.canvas = tk.Canvas(self.scroll_frame, bg="white")
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        # Scrollbar dọc
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Vị trí scrollbar và canvas
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Kết nối canvas và frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Danh sách lưu các biển số
        self.labels = []

        # Phần thêm mới biển
        self.add_frame = tk.Frame(self, bg="lightgray")
        self.add_frame.pack(pady=10)

        self.entry = tk.Entry(self.add_frame, font=("Arial", 12), width=20)
        self.entry.grid(row=0, column=0, padx=5)

        self.add_button = tk.Button(self.add_frame, text="Thêm biển", command=self.add_label, font=("Arial", 12))
        self.add_button.grid(row=0, column=1, padx=5)

        # Dữ liệu biển số mặc định
        self.load_plates_from_file()

    def load_plates_from_file(self):
        try:
            with open(self.plate_file, "r") as f:
                plates = f.readlines()
            for plate in plates:
                self.create_label(plate.strip())
        except FileNotFoundError:
            with open(self.plate_file, "w") as f:
                pass  # Tạo file mới nếu chưa tồn tại

    def save_plates_to_file(self):
        plates = [child.winfo_children()[0].cget("text") for child in self.scrollable_frame.winfo_children()]
        with open(self.plate_file, "w") as f:
            f.write("\n".join(plates))

    def create_label(self, text):
        label_container = tk.Frame(self.scrollable_frame, bg="white")
        label_container.pack(fill=tk.X, pady=2)

        tk.Label(label_container, text=text, bg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        tk.Button(
            label_container, text="Xóa", font=("Arial", 10),
            command=lambda: self.delete_label(label_container)
        ).pack(side=tk.RIGHT, padx=5)

    def add_label(self):
        text = self.entry.get().strip()
        pattern = r"^\d{2}[A-Z]\d{4,5}$"
        if re.match(pattern, text):
            self.create_label(text)
            self.save_plates_to_file()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đúng định dạng: 2 số, 1 chữ cái, 4-5 số (VD: 30A12345)!")

    def delete_label(self, label_container):
        label_container.destroy()
        self.save_plates_to_file()

class ShowPlateImage(Frame):
    def __init__(self, parent, mode="small"):
        self.image_size = None
        self.padding = None
        self.time_font = None
        self.plate_font = None
        self.title_font = None
        self.height = None
        self.width = None
        self.set_mode(mode)

        super().__init__(parent, width=self.width, height=self.height, bg="lightgray", relief="solid", bd=1)
        self.pack_propagate(False)

        # Tiêu đề phía trên
        self.title_label = tk.Label(self, text="Lịch sử Biển Số", bg="lightgray", font=self.title_font)
        self.title_label.pack(pady=3)

        # Frame cuộn
        self.scroll_frame = tk.Frame(self, bg="white")
        self.scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(self.scroll_frame, bg="white")
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.entries = []
        self.existing_files = set()  # Để theo dõi các ảnh đã hiển thị

        self.update_data_from_folder()
        self.auto_update()

    def set_mode(self, mode):
        """Cập nhật chế độ (small/large) cho giao diện"""
        if mode == "large":
            self.width = 640
            self.height = 480
            self.title_font = ("Arial", 20, "bold")
            self.plate_font = ("Arial", 16, "bold")
            self.time_font = ("Arial", 14)
            self.padding = {"padx": 10, "pady": 8}
            self.image_size = (300, 150)
        else:  # Mặc định là "small"
            self.width = 336
            self.height = 480
            self.title_font = ("Arial", 16, "bold")
            self.plate_font = ("Arial", 12)
            self.time_font = ("Arial", 12)
            self.padding = {"padx": 5, "pady": 5}
            self.image_size = (200, 100)

    def add_entry(self, plate_number, timestamp, image_path):
        """Thêm một entry mới vào frame"""
        entry_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid", bd=1)
        entry_frame.pack(fill=tk.X, **self.padding)

        # Tạo ảnh từ file
        image = Image.open(image_path)
        image = image.resize(self.image_size)  # Đảm bảo ảnh vừa với kích thước đã xác định
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(entry_frame, image=photo, bg="white")
        image_label.image = photo
        image_label.pack(side=tk.LEFT, padx=10)

        # Thông tin bên cạnh ảnh
        info_frame = tk.Frame(entry_frame, bg="white")
        info_frame.pack(side=tk.LEFT, padx=15, pady=5)

        plate_label = tk.Label(info_frame, text=f"Biển số: {plate_number}", bg="white", font=self.plate_font)
        plate_label.pack(anchor="w")

        time_label = tk.Label(info_frame, text=f"Thời gian: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}", bg="white",
                              font=self.time_font)
        time_label.pack(anchor="w")

        self.entries.append(entry_frame)

    def update_data_from_folder(self, folder_path="Detectedplate"):
        """Cập nhật dữ liệu từ thư mục với các ảnh có tên theo định dạng"""
        # Kiểm tra nếu thư mục tồn tại
        if not os.path.exists(folder_path):
            print(f"Thư mục {folder_path} không tồn tại.")
            return

        # Lấy danh sách các tệp tin trong thư mục
        files = os.listdir(folder_path)

        # Lọc các tệp tin hình ảnh với định dạng đúng
        image_files = [f for f in files if f.endswith(".png") and len(f.split("_")) == 3]

        # Lấy danh sách các ảnh đã hiển thị để tránh hiển thị lại
        current_files = set(image_files)

        # Tìm các file mới, nếu có
        new_files = current_files - self.existing_files

        # Cập nhật các ảnh mới
        for file_name in new_files:
            # Lấy thông tin từ tên tệp
            try:
                date_str, time_str, plate_number_with_extension = file_name.split("_")
                plate_number = plate_number_with_extension.split(".")[0]
                timestamp_str = f"{date_str[:2]}-{date_str[2:4]}-{date_str[4:8]} {time_str[:2]}:{time_str[2:4]}:00"
                timestamp = datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S")
            except ValueError:
                print(f"Không thể phân tích tên tệp: {file_name}")
                continue

            # Thêm entry mới vào giao diện
            image_path = os.path.join(folder_path, file_name)
            self.add_entry(plate_number, timestamp, image_path)

        # Cập nhật danh sách các ảnh đã hiển thị
        self.existing_files.update(new_files)

    def auto_update(self):
        """Automatically check for new images every 3 seconds"""
        self.update_data_from_folder()  # Check for new images
        self.after(1000, self.auto_update)  # Call auto_update again in 3 seconds