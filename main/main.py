from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Frame, Label

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\1.Projects\Automatic-door\main\assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def on_button_1_clicked():
    print("button_1 clicked")


def on_button_2_clicked():
    print("button_2 clicked")


def on_button_7_clicked():
    print("button_7 clicked")


class Sidebar(Frame):
    def __init__(self, parent, switch_screen_callback):
        super().__init__(parent, bg="#F2F4F8")
        self.switch_screen_callback = switch_screen_callback
        self.configure(width=256, height=720)

        # Add an image to the sidebar (e.g., a logo or icon)
        self.add_sidebar_image("image_sidebar.png", x=-1, y=-1)
        self.add_sidebar_image("image_logo.png", x=12, y=24)

        # Sidebar buttons
        self.create_button("button_alarm.png", on_button_1_clicked, x=100, y=76, width=48, height=48)

        # Interface-switching buttons (button 3, 4, 5, and 6)
        self.create_button("button_home.png", lambda: self.switch_screen_callback(3), x=12, y=136, width=232, height=48)
        self.create_button("button_plate archive.png", lambda: self.switch_screen_callback(4), x=12, y=192, width=232, height=48)
        self.create_button("button_camcontrol.png", lambda: self.switch_screen_callback(5), x=12, y=248, width=232, height=48)
        self.create_button("button_setting.png", lambda: self.switch_screen_callback(6), x=12, y=304, width=232, height=48)

        # Extra button (button 7)
        self.create_button("button_....png", on_button_7_clicked, x=12, y=674, width=24, height=24)

    def create_button(self, image_path, command, x, y, width, height):
        button_image = PhotoImage(file=relative_to_assets(image_path))
        button = Button(self, image=button_image, borderwidth=0, highlightthickness=0, relief="flat", command=command)
        button.image = button_image  # Keep a reference to avoid garbage collection
        button.place(x=x, y=y, width=width, height=height)

    def add_sidebar_image(self, image_name, x, y):
        """Add a static image to the sidebar."""
        image = PhotoImage(file=relative_to_assets(image_name))
        label = Label(self, image=image, bg="#F2F4F8")
        label.image = image  # Keep reference to prevent garbage collection
        label.place(x=x, y=y)


def switch_screen(screen_id):
    print(f"Switching to screen {screen_id}")
    # Placeholder for actual screen-switching logic


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg="#F2F4F8")
        self.root.resizable(False, False)

        # Canvas setup
        self.canvas = Canvas(root, bg="#F2F4F8", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # # Adding images to canvas
        # self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        # self.canvas.create_image(128, 360, image=self.image_image_1)
        #
        # self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        # self.canvas.create_image(128, 44, image=self.image_image_2)

        # Initialize sidebar with default screen set to 3
        self.sidebar = Sidebar(self.root, switch_screen)
        self.sidebar.place(x=0, y=0)
        switch_screen(3)


if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
