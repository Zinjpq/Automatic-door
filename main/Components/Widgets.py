import threading
from datetime import time
from tkinter import Frame, Canvas, Label, Image
import cv2
import numpy as np
import requests
from PIL import ImageTk

from main.Library import relative_to_assets


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
