import os
from datetime import datetime
import random
import tkinter as tk
from tkinter import Frame, ttk

from PIL import Image, ImageTk


class ShowPlateImage1(Frame):
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

        self.update_data_from_folder()
        self.auto_update()

    def set_mode(self, mode):
        """Cập nhật chế độ (small/large) cho giao diện"""
        if mode == "large":
            self.width = 640
            self.height = 570
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

    def add_random_entry(self):
        plate_number = f"{random.randint(10, 99)}A-{random.randint(1000, 9999)}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid", bd=1)
        entry_frame.pack(fill=tk.X, **self.padding)

        # Tạo ảnh giả ngẫu nhiên
        image = Image.new("RGB", self.image_size, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(entry_frame, image=photo, bg="white")
        image_label.image = photo
        image_label.pack(side=tk.LEFT, padx=10)

        # Thông tin bên cạnh ảnh
        info_frame = tk.Frame(entry_frame, bg="white")
        info_frame.pack(side=tk.LEFT, padx=15, pady=5)

        plate_label = tk.Label(info_frame, text=f"Biển số: {plate_number}", bg="white", font=self.plate_font)
        plate_label.pack(anchor="w")

        time_label = tk.Label(info_frame, text=f"Thời gian: {timestamp}", bg="white", font=self.time_font)
        time_label.pack(anchor="w")

        self.entries.append(entry_frame)

    def update_data_from_folder(self, folder_path="detectedplate"):
        """Cập nhật dữ liệu từ thư mục với các ảnh có tên theo định dạng"""
        # Kiểm tra nếu thư mục tồn tại
        if not os.path.exists(folder_path):
            print(f"Thư mục {folder_path} không tồn tại.")
            return

        # Lấy danh sách các tệp tin trong thư mục
        files = os.listdir(folder_path)

        # Lọc các tệp tin hình ảnh với định dạng đúng
        image_files = [f for f in files if f.endswith(".png") and len(f.split("_")) == 3]

        for file_name in image_files:
            # Lấy thông tin từ tên tệp
            try:
                date_str, time_str, plate_number_with_extension = file_name.split("_")
                plate_number = plate_number_with_extension.split(".")[0]
                timestamp_str = f"{date_str[:2]}-{date_str[2:4]}-{date_str[4:8]} {time_str[:2]}:{time_str[2:4]}:00"
                timestamp = datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S")
            except ValueError:
                print(f"Không thể phân tích tên tệp: {file_name}")
                continue

            entry_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid", bd=1)
            entry_frame.pack(fill=tk.X, **self.padding)

            # Tạo ảnh ngẫu nhiên giả (hoặc thay bằng việc tải ảnh thực tế từ tệp tin)
            image_path = os.path.join(folder_path, file_name)
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

    def auto_update(self):
        """Automatically update the data every 3 seconds"""
        self.update_data_from_folder()
        self.after(3000, self.auto_update)  # Call auto_update again in 3 seconds