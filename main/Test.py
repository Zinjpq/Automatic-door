from datetime import datetime
import random
import tkinter as tk
from tkinter import Frame, ttk

from PIL import Image, ImageTk

class ShowPlateImage(Frame):
    def __init__(self, parent, mode="small"):
        # Xác định kích thước và font chữ dựa trên mode
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

        super().__init__(parent, width=self.width, height=self.height, bg="lightgray", relief="solid", bd=1)
        self.place(x=(1280 - self.width) // 2, y=(720 - self.height) // 2)  # Căn giữa màn hình

        # Tiêu đề phía trên
        self.title_label = tk.Label(self, text="Lịch sử Biển Số", bg="lightgray", font=self.title_font)
        self.title_label.pack(pady=10)

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

        # Nút tạo ngẫu nhiên ảnh để test
        self.test_frame = tk.Frame(self, bg="lightgray")
        self.test_frame.pack(pady=10)

        self.test_button = tk.Button(self.test_frame, text="Tạo ngẫu nhiên", command=self.add_random_entry, font=("Arial", 12))
        self.test_button.pack(padx=5)

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
