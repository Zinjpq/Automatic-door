from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\1.Projects\Automatic-door\main\assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


import tkinter as tk
from tkinter import Canvas, PhotoImage


class Sidebar(tk.Frame):
    def __init__(self, parent, switch_frame_callback):
        super().__init__(parent, bg="lightgray")
        self.pack(side="left", fill="y")

        # Buttons to switch between frames
        btn_frame1 = tk.Button(self, text="Giao diện 1", command=lambda: switch_frame_callback("frame1"))
        btn_frame2 = tk.Button(self, text="Giao diện 2", command=lambda: switch_frame_callback("frame2"))

        btn_frame1.pack(pady=10)
        btn_frame2.pack(pady=10)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1280x720")
        self.configure(bg="#F2F4F8")

        canvas = Canvas(
            self,
            bg="#F2F4F8",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        image_image_1 = PhotoImage(file=relative_to_assets("image_sidebar.png"))
        canvas.create_image(128.0, 360.0, image=image_image_1)

        image_image_2 = PhotoImage(
            file=relative_to_assets("image_logo.png"))
        image_2 = canvas.create_image(
            128.0,
            44.0,
            image=image_image_2
        )
        # Create Sidebar and main frames
        self.sidebar = Sidebar(self, self.switch_frame)

        # Create frames for each UI
        self.frames = {}
        for F in (Frame1, Frame2):
            frame = F(self)
            self.frames[F.__name__.lower()] = frame
            frame.pack(fill="both", expand=True)

        self.current_frame = None
        self.switch_frame("frame1")  # Default to show frame1

    def switch_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.pack_forget()

        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)
        self.current_frame = frame


class Frame1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Đây là Giao diện 1", font=("Arial", 18)).pack(pady=50)


class Frame2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Đây là Giao diện 2", font=("Arial", 18)).pack(pady=50)


if __name__ == "__main__":
    app = App()
    app.mainloop()


# from pathlib import Path
#
# # from tkinter import *
# # Explicit imports to satisfy Flake8
#
#
# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"D:\1.Projects\Automatic-door\main\assets")
#
#
# def relative_to_assets(path: str) -> Path:
#     return ASSETS_PATH / Path(path)
#
#
# import tkinter as tk
# from tkinter import Tk, Canvas, PhotoImage
#
#
#
# class Sidebar(tk.Frame):
#     def __init__(self, parent, switch_frame_callback):
#         super().__init__(parent, bg="lightgray")
#         self.pack(side="left", fill="y")
#
#         # Button để chuyển giao diện
#         btn_frame1 = tk.Button(self, text="Giao diện 1", command=lambda: switch_frame_callback("frame1"))
#         btn_frame2 = tk.Button(self, text="Giao diện 2", command=lambda: switch_frame_callback("frame2"))
#
#         btn_frame1.pack(pady=10)
#         btn_frame2.pack(pady=10)
#
#
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#
#         window = Tk()
#
#         window.geometry("1280x720")
#         window.configure(bg="#F2F4F8")
#
#         canvas = Canvas(
#             window,
#             bg="#F2F4F8",
#             height=720,
#             width=1280,
#             bd=0,
#             highlightthickness=0,
#             relief="ridge"
#         )
#
#         canvas.place(x=0, y=0)
#         image_image_1 = PhotoImage(
#             file=relative_to_assets("image_sidebar.png"))
#         image_sidebar = canvas.create_image(
#             128.0,
#             360.0,
#             image=image_image_1
#         )
#
#         # Tạo Sidebar và Frame chính
#         self.sidebar = Sidebar(self, self.switch_frame)
#
#         # Tạo Frame cho các giao diện
#         self.frames = {}
#         for F in (Frame1, Frame2):
#             frame = F(self)
#             self.frames[F.__name__.lower()] = frame
#             frame.pack(fill="both", expand=True)
#
#         self.current_frame = None
#         self.switch_frame("frame1")  # Mặc định hiển thị giao diện 1
#
#     def switch_frame(self, frame_name):
#         if self.current_frame:
#             self.current_frame.pack_forget()
#
#         frame = self.frames[frame_name]
#         frame.pack(fill="both", expand=True)
#         self.current_frame = frame
#
#
# class Frame1(tk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent, bg="white")
#         tk.Label(self, text="Đây là Giao diện 1", font=("Arial", 18)).pack(pady=50)
#
#
# class Frame2(tk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent, bg="white")
#         tk.Label(self, text="Đây là Giao diện 2", font=("Arial", 18)).pack(pady=50)
#
#
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
