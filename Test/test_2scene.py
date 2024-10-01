import tkinter as tk
import requests
import cv2
from PIL import Image, ImageTk
import numpy as np
import qrcode
import threading
import time


# Scene Switcher
def switch_to_scene_2():
    scene_1_frame.pack_forget()  # Hide Scene 1
    scene_2_frame.pack(fill="both", expand=True)  # Show Scene 2
    update_video()  # Start video stream update


# Check ESP32-CAM connection
def check_connection():
    while True:
        try:
            response = requests.get('http://192.168.1.100', timeout=1)
            if response.status_code == 200:
                status_label_1.config(text="Kết nối thành công với ESP32-CAM!")
                switch_to_scene_2()
                break
        except requests.exceptions.RequestException:
            status_label_1.config(text="Chưa kết nối được với ESP32-CAM...")
        time.sleep(2)


# Scene 1: Display QR code and connection instructions
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return ImageTk.PhotoImage(img)


# Scene 2: Display video stream and controls
def send_command(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            status_label_2.config(text=f"Command successful: {url}")
        else:
            status_label_2.config(text=f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        status_label_2.config(text=f"Connection error: {e}")


def update_video():
    try:
        img_resp = requests.get(url_cam)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.config(image=imgtk)
    except Exception as e:
        status_label_2.config(text=f"Video stream error: {e}")
    root.after(30, update_video)


# Main window setup
root = tk.Tk()
root.title("ESP32-CAM Setup")
root.geometry("1280x720")

# Scene 1: Connection instructions
scene_1_frame = tk.Frame(root)
scene_1_frame.pack(fill="both", expand=True)

status_label_1 = tk.Label(scene_1_frame, text="Chưa kết nối với ESP32-CAM", font=("Arial", 16))
status_label_1.pack(pady=20)

ssid_label = tk.Label(scene_1_frame, text="SSID: ESP32-CAM", font=("Arial", 14))
ssid_label.pack()

password_label = tk.Label(scene_1_frame, text="Password: 123456789", font=("Arial", 14))
password_label.pack()

qr_label = tk.Label(scene_1_frame)
qr_label.pack(pady=10)
qr_img = generate_qr('http://192.168.4.1')
qr_label.config(image=qr_img)

access_point_label = tk.Label(scene_1_frame, text="Kết nối vào http://192.168.4.1", font=("Arial", 14))
access_point_label.pack(pady=20)

# Start checking for connection in a separate thread
threading.Thread(target=check_connection, daemon=True).start()

# Scene 2: Video stream and controls
scene_2_frame = tk.Frame(root)

video_label = tk.Label(scene_2_frame)
video_label.pack(fill="both", expand=True)

status_label_2 = tk.Label(scene_2_frame, text="Status: ", font=("Arial", 12))
status_label_2.pack(side="bottom", fill="x")

button_frame = tk.Frame(scene_2_frame)
button_frame.pack(side="bottom", pady=10)

tk.Button(button_frame, text="Left", command=lambda: send_command(url1)).grid(row=0, column=0)
tk.Button(button_frame, text="Right", command=lambda: send_command(url2)).grid(row=0, column=2)
tk.Button(button_frame, text="Up", command=lambda: send_command(url3)).grid(row=0, column=1)
tk.Button(button_frame, text="Down", command=lambda: send_command(url4)).grid(row=1, column=1)

# ESP32-CAM URL and Control URLs
url_cam = 'http://192.168.1.100/cam'
url1 = 'http://192.168.1.100/left'
url2 = 'http://192.168.1.100/right'
url3 = 'http://192.168.1.100/up'
url4 = 'http://192.168.1.100/down'

# Start the main loop
root.mainloop()
