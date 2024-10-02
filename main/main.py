# Main.py
import library
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = library.ESP32CamApp(root)
    root.mainloop()