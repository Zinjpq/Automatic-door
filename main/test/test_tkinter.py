from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.title('Button tutorial')
root.iconbitmap('klee2.ico')
root.geometry('1280x720')


def hello():
    pass


my_button = customtkinter.CTkButton(root,
                                    text="hello world!",
                                    command=hello,
                                    fg_color="white",
                                    text_color="black",
                                    height=48,
                                    width=224,
                                    corner_radius=16,
                                    border_width=2,
                                    hover_color="White",
                                    compound="top")
my_button.pack(pady=80)


root.mainloop()