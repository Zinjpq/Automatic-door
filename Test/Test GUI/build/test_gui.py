import tkinter as tk
from pathlib import Path
from tkinter import Tk, Button, PhotoImage
import cv2
import numpy as np
import requests
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\1.Projects\Automatic door\Test\Test GUI\build\assets\frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def send_command(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command successful: {url}")
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")


class ESP32CamApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg="#F2F4F8")

        # ESP32-CAM URLs
        self.url_cam = 'http://192.168.1.100/cam'
        self.url1 = 'http://192.168.1.100/left'
        self.url2 = 'http://192.168.1.100/right'
        self.url3 = 'http://192.168.1.100/up'
        self.url4 = 'http://192.168.1.100/down'

        # Initialize canvas and elements from Tkinter Designer
        self.canvas = tk.Canvas(
            root,
            bg="#F2F4F8",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            256.0,
            720.0,
            fill="#000000",
            outline="")

        self.canvas.create_text(
            268.0,
            12.0,
            anchor="nw",
            text="Camera control",
            fill="#000000",
            font=("Roboto Bold", 30 * -1)
        )

        self.canvas.create_rectangle(
            268.0,
            66.0,
            908.0,
            142.0,
            fill="#000000",
            outline="")

        # Video display (using placeholder image initially)
        self.video_label = tk.Label(self.canvas)
        self.video_label.place(x=268.0, y=165.0, width=640, height=360)

        # Control buttons
        self.create_buttons()

        # Start video stream
        self.update_video()

    def create_buttons(self):
        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: send_command(self.url1),  # Send command to move left
            relief="flat"
        )
        button_1.place(x=992.0, y=250.0, width=72.0, height=94.0)
        button_1.image = button_image_1

        button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: send_command(self.url2),  # Send command to move right
            relief="flat"
        )
        button_2.place(x=1074.0, y=250.0, width=72.0, height=94.0)
        button_2.image = button_image_2

        button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: send_command(self.url3),  # Send command to move up
            relief="flat"
        )
        button_3.place(x=1156.0, y=250.0, width=72.0, height=94.0)
        button_3.image = button_image_3

        button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        button_4 = Button(
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: send_command(self.url4),  # Send command to move down
            relief="flat"
        )
        button_4.place(x=992.0, y=344.0, width=72.0, height=94.0)
        button_4.image = button_image_4

    def update_video(self):
        try:
            img_resp = requests.get(self.url_cam)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, -1)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)
        except Exception as e:
            print(f"Video stream error: {e}")

        # Update video every 30ms
        self.root.after(30, self.update_video)


# Main function to start the application
if __name__ == "__main__":
    window = Tk()
    app = ESP32CamApp(window)
    window.resizable(False, False)
    window.mainloop()
