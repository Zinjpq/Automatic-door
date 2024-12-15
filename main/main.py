from pathlib import Path
from tkinter import Tk, Canvas, Frame, Label
import numpy as np
import requests
from PIL import ImageTk
import Library
import cv2

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
        Library.add_image("image_Livestream.png", x=300, y=88)
        Library.add_image("image_livestream2.png", x=268, y=88)

        Library.create_time_and_date_labels(
            parent=root,
            time_coords=(750, 92),  # Vị trí hiển thị thời gian
            date_coords=(826, 92),  # Vị trí hiển thị ngày
            font=("SegoeUI", 17 * -1),  # Font chữ
            color="#000000"  # Màu chữ
        )

        Library.add_image("image_Cameraerror.png", x=268, y=136)

        # Tạo khung livestream
        self.livestream_canvas = Canvas(self, bg="#000000", width=640, height=480, highlightthickness=0)
        self.livestream_canvas.place(x=268, y=136)

        # Tạo nhãn báo lỗi kết nối
        self.camera_error_label = Label(self, bg="#F2F4F8")
        self.error_image = ImageTk.PhotoImage(file=Library.relative_to_assets("image_Cameraerror.png"))
        self.camera_error_label.config(image=self.error_image)
        self.camera_error_label.place(x=268, y=136)
        self.camera_error_label.lower()  # Ẩn ban đầu

        response = requests.get(url)
        # Bắt đầu kiểm tra trạng thái kết nối
        self.check_camera_connection(response)

    def check_camera_connection(self, response):
        if response.status_code == 200:
            self.camera_error_label.lower()  # Ẩn nhãn lỗi
            self.show_livestream_frame()  # Hiển thị video
        else:
            self.camera_error_label.lift()  # Hiển thị nhãn lỗi
            self.livestream_canvas.delete("all")  # Xóa nội dung livestream

        # Lặp lại kiểm tra mỗi 1 giây
        self.after(1000, self.check_camera_connection)

    def show_livestream_frame(self):
        """Hiển thị livestream từ ESP32-CAM (giả lập hoặc cập nhật frame)."""
        # Bạn cần thêm mã xử lý nhận frame từ ESP32-CAM qua HTTP hoặc socket.
        # Đây là một ví dụ giả lập:
        # Fetch the frame from ESP32-CAM

        img_resp = requests.get(CAMERA_URL)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        # Convert the frame to a format compatible with Tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_detected = Library.detect_license_plate(img)
        photo = ImageTk.PhotoImage(img_detected)

        self.livestream_canvas.create_image(0, 0, anchor="nw", image=photo)
        self.livestream_canvas.image = photo  # Lưu tham chiếu để không bị garbage collected


    # def check_connection_to_esp32(self):
    #     try:
    #         response = requests.get(url)
    #         if response.status_code == 200:
    #             print(f"Command sent successfully: {url}")
    #         else:
    #             print(f"Error: {response.status_code}")
    #     except requests.exceptions.RequestException as e:
    #         print(f"Connection error: {e}")


class PlateArchiveScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent, bg="#F2F4F8")  # Màu nền cho màn hình Home
        self.configure(width=1024, height=720)

        # Thêm các thành phần cho Home (ví dụ: Tiêu đề, danh sách, nút,...)
        label = Label(self, text="Plate Archive", font=("Arial", 24), bg="#FFFFFF")
        label.pack(pady=20)

        # Thêm các widget khác vào đây

class CamControlScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent, bg="#F2F4F8")  # Màu nền cho màn hình Home
        self.configure(width=1024, height=720)

        # Thêm các thành phần cho Home (ví dụ: Tiêu đề, danh sách, nút,...)
        label = Label(self, text="Cam Control", font=("Arial", 24), bg="#FFFFFF")
        label.pack(pady=20)

        # Thêm các widget khác vào đây

class SettingsScene(BaseScene):
    def __init__(self, parent):
        super().__init__(parent, bg="#F2F4F8")  # Màu nền cho màn hình Settings
        self.configure(width=1024, height=720)

        # Thêm các thành phần cho Settings (ví dụ: Điều chỉnh, nút lưu,...)
        label = Label(self, text="Settings Screen", font=("Arial", 24), bg="#EFEFEF")
        label.pack(pady=20)

        # Thêm các widget khác vào đây

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg="#F2F4F8")
        self.root.resizable(False, False)

        # Canvas setup
        self.canvas = Canvas(root, bg="#F2F4F8", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Initialize sidebar with default screen set to 3
        self.sidebar = Sidebar(self.root, self.switch_screen)
        self.sidebar.place(x=0, y=0)

        # Initialize screens
        self.home_scene = HomeScene(self.root)
        self.platearchive_scene = PlateArchiveScene(self.root)
        self.camcontrol_scene = CamControlScene(self.root)
        self.settings_scene = SettingsScene(self.root)

        # Show the default screen (Home)
        self.switch_screen(1)

        # Library.Detect_License_Plate()

    def switch_screen(self, screen_id):
        """Chuyển đổi màn hình dựa trên `screen_id`."""
        # Hide all screens
        self.home_scene.place_forget()
        self.platearchive_scene.place_forget()
        self.camcontrol_scene.place_forget()
        self.settings_scene.place_forget()

        # Show the selected screen
        if screen_id == 1:  # Home
            self.home_scene.place(x=256, y=0)
        elif screen_id == 2:  # Settings
            self.platearchive_scene.place(x=256, y=0)
        elif screen_id == 3:  # Settings
            self.camcontrol_scene.place(x=256, y=0)
        elif screen_id == 4:  # Settings
            self.settings_scene.place(x=256, y=0)


def on_button_1_clicked():
    print("button_1 clicked")

def on_button_2_clicked():
    print("button_2 clicked")

def on_button_7_clicked():
    print("button_7 clicked")

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
