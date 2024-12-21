import threading
import time
from datetime import datetime
from pathlib import Path
from tkinter import Button, PhotoImage, Label
from tkinter import Frame, Canvas
import cv2
import numpy as np
import requests
from PIL import ImageTk, Image

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

def detect_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    plate_images = []
    for (x, y, w, h) in plates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        plate_images.append(gray[y:y + h, x:x + w])

    return image, plate_images
