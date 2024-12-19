from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Frame, Label
import requests
import numpy as np
from PIL import Image, ImageTk
import cv2
import Library

# Constants
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\1.Projects\Automatic-door\main\assets")

# ESP32-CAM URLs
ESP32_BASE_URL = 'http://192.168.4.184'
CAMERA_URL = f"{ESP32_BASE_URL}/cam"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Sidebar(Frame):
    def __init__(self, parent, switch_screen_callback):
        super().__init__(parent, bg="#F2F4F8", width=256, height=720)
        self.switch_screen_callback = switch_screen_callback

        Library.add_image("image_sidebar2.png", x=0, y=-2)
        buttons = [
            ("button_alarm.png", on_button_1_clicked, 100, 76),
            ("button_home.png", lambda: self.switch_screen_callback(1), 12, 136),
            ("button_plate archive.png", lambda: self.switch_screen_callback(2), 12, 192),
            ("button_camcontrol.png", lambda: self.switch_screen_callback(3), 12, 248),
            ("button_setting.png", lambda: self.switch_screen_callback(4), 12, 304),
        ]
        for image, command, x, y in buttons:
            Library.create_button(image, command, x=x, y=y, width=232, height=48)


class BaseScene(Frame):
    def __init__(self, parent, bg_color="#F2F4F8"):
        super().__init__(parent, bg=bg_color, width=1024, height=720)


class HomeScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)
        Library.add_image("image_Home.png", x=268, y=24)
        Library.create_time_and_date_labels(
            parent=parent,
            time_coords=(750, 92),
            date_coords=(826, 92),
            font=("SegoeUI", 17 * -1),
            color="#000000",
        )

        self.livestream_canvas = Canvas(self, bg="#000000", width=640, height=480, highlightthickness=0)
        self.livestream_canvas.place(x=268, y=136)

        self.camera_error_label = Label(self, bg="#F2F4F8")
        self.error_image = ImageTk.PhotoImage(file=Library.relative_to_assets("image_Cameraerror.png"))
        self.camera_error_label.config(image=self.error_image)
        self.camera_error_label.place(x=268, y=136)
        self.camera_error_label.lower()

        self.after(1000, self.check_camera_connection)

    def check_camera_connection(self):
        try:
            response = requests.get(CAMERA_URL, timeout=2)
            if response.status_code == 200:
                self.camera_error_label.lower()
                self.show_livestream_frame()
            else:
                self.show_camera_error()
        except requests.exceptions.RequestException:
            self.show_camera_error()

        self.after(1000, self.check_camera_connection)

    def show_camera_error(self):
        self.camera_error_label.lift()
        self.livestream_canvas.delete("all")

    def show_livestream_frame(self):
        try:
            img_resp = requests.get(CAMERA_URL, timeout=2)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_detected = Library.detect_license_plate(img)
            photo = ImageTk.PhotoImage(image=Image.fromarray(img ))
            self.livestream_canvas.create_image(0, 0, anchor="nw", image=photo)
            self.livestream_canvas.image = photo
        except Exception:
            self.show_camera_error()


class PlateArchiveScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)
        # Label(self, text="Plate Archive", font=("Arial", 24), bg="#FFFFFF").pack(pady=20)
        Library.add_image("image_LicensePlateArchive.png", x=268, y=24)


class CamControlScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, text="Cam Control", font=("Arial", 24), bg="#FFFFFF").pack(pady=20)


class SettingsScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent, bg_color="#EFEFEF")
        Label(self, text="Settings Screen", font=("Arial", 24), bg="#EFEFEF").pack(pady=20)


class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg="#F2F4F8")
        self.root.resizable(False, False)

        self.sidebar = Sidebar(self.root, self.switch_screen)
        self.sidebar.place(x=0, y=0)

        self.scenes = {
            1: HomeScene(self.root),
            2: PlateArchiveScene(self.root),
            3: CamControlScene(self.root),
            4: SettingsScene(self.root),
        }
        self.current_scene = None
        self.switch_screen(1)

    def switch_screen(self, screen_id: int):
        if self.current_scene:
            self.current_scene.place_forget()
        self.current_scene = self.scenes.get(screen_id)
        if self.current_scene:
            self.current_scene.place(x=256, y=0)


def on_button_1_clicked():
    print("Button 1 clicked")


if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
