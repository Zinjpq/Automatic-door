from tkinter import Frame, Tk

from main.Components import Widgets
from main.Components.Widgets import AddLicensePlateText, ShowPlateImage, ButtonMoveCam
from main.Constants.urls import CAMERA_URL


def AlarmButton():
    print("AlarmButton clicked")


class Sidebar(Frame):
    def __init__(self, parent, switch_screen_callback):
        super().__init__(parent, width=256, height=720)
        self.switch_screen_callback = switch_screen_callback

        # Add an image to the sidebar (e.g., a logo or icon)
        Widgets.add_image("image_sidebar2.png", parent=self, x=0, y=-2)
        Widgets.create_button("button_alarm.png", self, AlarmButton, x=100, y=76, width=48, height=48)

        buttons = [
            ("button_home.png", lambda: self.switch_screen_callback(1), 12, 136),
            ("button_plate archive.png", lambda: self.switch_screen_callback(2), 12, 192),
            ("button_camcontrol.png", lambda: self.switch_screen_callback(3), 12, 248),
            ("button_setting.png", lambda: self.switch_screen_callback(4), 12, 304),
        ]
        for image, command, x, y in buttons:
            Widgets.create_button(image, self, command, x=x, y=y, width=232, height=48)


class RightBar(Frame):
    def __init__(self, parent):
        super().__init__(parent, width=336, height=480)


class BaseScene(Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1024, height=720)


class HomeScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)
        Widgets.add_image("image_Home.png", parent=self, x=268 - 256, y=24)
        Widgets.add_image("image_Livestream.png", parent=self, x=300 - 256, y=88)
        Widgets.add_image("image_livestream2.png", parent=self, x=268 - 256, y=88)

        Widgets.create_time_and_date_labels(
            parent=self,
            time_coords=(750, 92),  # Vị trí hiển thị thời gian
            date_coords=(826, 92),  # Vị trí hiển thị ngày
            font=("SegoeUI", 17 * -1),  # Font chữ
            color="#000000"  # Màu chữ
        )

        self.livestream = Widgets.LivestreamWidget(self, CAMERA_URL)
        self.livestream.place(x=268 - 256, y=136)
        # folder =
        # AutoUpdateLicensePlateScene(self, parent, folder)
        self.AddLicenseText = ShowPlateImage(self, mode="small")
        self.AddLicenseText.place(x=932-256, y=136)


class PlateArchiveScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)
        Widgets.add_image("image_LicensePlateArchive.png", parent=self, x=12, y=24)

        Widgets.create_time_and_date_labels(
            parent=self,
            time_coords=(12+256, 92),  # Vị trí hiển thị thời gian
            date_coords=(88+256, 92),  # Vị trí hiển thị ngày
            font=("SegoeUI", 17 * -1),  # Font chữ
            color="#000000"  # Màu chữ
        )

        self.AddLicenseText = ShowPlateImage(self, mode="large")
        self.AddLicenseText.place(x=12,y=136)

        plate_file = "plate.txt"
        self.AddLicensePlateText =  AddLicensePlateText(self,plate_file)
        self.AddLicensePlateText.place(x=932-256,y=136)
class CamControlScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)
        Widgets.add_image("image_CameraControl.png", parent=self, x=268 - 256, y=24)
        Widgets.add_image("image_Livestream.png", parent=self, x=300 - 256, y=88)
        Widgets.add_image("image_livestream2.png", parent=self, x=268 - 256, y=88)
        Widgets.add_image("image_ControlLabel.png", parent=self, x=920 - 256, y=136)

        Widgets.create_time_and_date_labels(
            parent=self,
            time_coords=(750, 92),  # Vị trí hiển thị thời gian
            date_coords=(826, 92),  # Vị trí hiển thị ngày
            font=("SegoeUI", 17 * -1),  # Font chữ
            color="#000000"  # Màu chữ
        )

        # Library.add_image("image_Cameraerror.png", parent=self, x=268-256, y=136)
        self.livestream = Widgets.LivestreamWidget(self, CAMERA_URL)
        self.livestream.place(x=268 - 256, y=136)
        buttons = [
            ("button_up.png", lambda: ButtonMoveCam("up"), 1045, 196),
            ("button_down.png", lambda: ButtonMoveCam("down"), 1045, 476),
            ("button_left.png",lambda:  ButtonMoveCam("left"), 923, 336),
            ("button_right.png", lambda: ButtonMoveCam("right"), 1170, 336),
            # ("button_zoomin.png", on_click, 923, 196),
            # ("button_zoomout.png", on_click, 923, 476),
            # ("button_ResetZoom.png", on_click, 1170, 476),
            # ("button_ResetRadius.png", on_click, 1170, 196),
        ]
        for image, command, x, y in buttons:
            Widgets.create_button(image, self, command, x=x - 256, y=y, width=110, height=140)


class SettingsScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent)


class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg="#F2F4F8")
        self.root.resizable(False, False)

        self.sidebar = Sidebar(self.root, self.switch_screen)
        self.sidebar.place(x=0, y=0)
        self.Rightbar = RightBar(self.root)
        self.Rightbar.place(x=920, y=0)

        self.scenes = {
            1: HomeScene(self.root),
            2: PlateArchiveScene(self.root),
            3: CamControlScene(self.root),
            4: SettingsScene(self.root),
        }
        self.current_scene = None
        self.switch_screen(3)

    def switch_screen(self, screen_id: int):
        if self.current_scene:
            self.current_scene.place_forget()
        self.current_scene = self.scenes.get(screen_id)
        if self.current_scene:
            self.current_scene.place(x=256, y=0)
