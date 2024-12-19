from pathlib import Path
from tkinter import Tk, Frame

import Library

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\1.Projects\Automatic-door\main\assets")

# ESP32-CAM URL and Control URLs
ESP32_BASE_URL = url = 'http://192.168.4.184'
CAMERA_URL = ESP32_BASE_URL + '/cam'
# url1 = ESP32_BASE_URL + '/left'
# url2 = ESP32_BASE_URL + '/right'
# url3 = ESP32_BASE_URL + '/up'
# url4 = ESP32_BASE_URL + '/down'

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Sidebar(Frame):
    def __init__(self, parent, switch_screen_callback):
        super().__init__(parent, bg="#F2F4F8", width = 256, height=720)
        self.switch_screen_callback = switch_screen_callback

        # Add an image to the sidebar (e.g., a logo or icon)
        Library.add_image("image_sidebar2.png", parent=self, x=0, y=-2)
        Library.create_button("button_alarm.png", root, on_button_1_clicked, x=100, y=76, width=48, height=48)
        
        buttons = [
            ("button_home.png", lambda: self.switch_screen_callback(1), 12, 136),
            ("button_plate archive.png", lambda: self.switch_screen_callback(2), 12, 192),
            ("button_camcontrol.png", lambda: self.switch_screen_callback(3), 12, 248),
            ("button_setting.png", lambda: self.switch_screen_callback(4), 12, 304),
        ]
        for image, command, x, y in buttons:
            Library.create_button(image, root, command, x=x, y=y, width=232, height=48)

class BaseScene(Frame):
    def __init__(self, parent, bg_color="#F2F4F8"):
        super().__init__(parent, bg=bg_color, width=1024, height=720)


class HomeScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)
        Library.add_image("image_Home.png", parent=self, x=268-256, y=24)
        Library.add_image("image_Livestream.png", parent=self, x=300-256, y=88)
        Library.add_image("image_livestream2.png", parent=self, x=268-256, y=88)

        Library.create_time_and_date_labels(
            parent=self,
            time_coords=(750, 92),  # Vị trí hiển thị thời gian
            date_coords=(826, 92),  # Vị trí hiển thị ngày
            font=("SegoeUI", 17 * -1),  # Font chữ
            color="#000000"  # Màu chữ
        )

        # Library.add_image("image_Cameraerror.png", parent=self, x=268-256, y=136)
        self.livestream = Library.LivestreamWidget(self, CAMERA_URL)
        self.livestream.place(x=268-256, y=136)

class PlateArchiveScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)
        Library.add_image("image_LicensePlateArchive.png", parent=self, x=268-256, y=24)

class CamControlScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)
        Library.add_image("image_CameraControl.png", parent=self, x=268-256, y=24)
        Library.add_image("image_Livestream.png", parent=self, x=300-256, y=88)
        Library.add_image("image_livestream2.png", parent=self, x=268-256, y=88)
        Library.add_image("image_control.png", parent=self,x=959-256,y=201)

        Library.create_time_and_date_labels(
            parent=self,
            time_coords=(750, 92),  # Vị trí hiển thị thời gian
            date_coords=(826, 92),  # Vị trí hiển thị ngày
            font=("SegoeUI", 17 * -1),  # Font chữ
            color="#000000"  # Màu chữ
        )

        # Library.add_image("image_Cameraerror.png", parent=self, x=268-256, y=136)
        self.livestream = Library.LivestreamWidget(self, CAMERA_URL)
        self.livestream.place(x=268-256, y=136)
        buttons = [
            ("button_up.png", lambda: on_click, 1065, 245),
            ("button_down.png", lambda: on_click, 1065, 433),
            ("button_left.png", lambda: on_click, 983,339),
            ("button_right.png", lambda: on_click, 1147, 339),
            ("button_zoomin.png", lambda: on_click, 983, 245),
            ("button_zoomout.png", lambda: on_click, 1147, 433),
            ("button_reset.png", lambda: on_click, 1147, 245),
            ("button_reset (2).png", lambda: on_click, 983, 433),
        ]
        for image, command, x, y in buttons:
            Library.create_button(image, self, command, x=x-256, y=y, width=72, height=94)

        
class SettingsScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent) 


class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.configure(bg="#F2F4F8")
        self.root.resizable(True, True)

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
    print("button_1 clicked")

def on_button_2_clicked():
    print("button_2 clicked")

def on_button_7_clicked():
    print("button_7 clicked")
def on_click():
    print("Button clicked!")

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
