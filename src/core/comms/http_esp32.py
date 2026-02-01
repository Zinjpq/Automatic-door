import requests

DOOR_STATUS = 0
current_pan = 50
current_tilt = 90

# ESP32-CAM URL and Control URLs
ESP32_BASE_URL = 'http://192.168.4.1'
CAMERA_URL = 'http://192.168.4.184/cam'
# RasPi_Base_URL = "http://192.168.4.2:5000"

def on_key_press(event):
    set_angle(event.keysym)

def set_angle(direction):
    global current_pan, current_tilt, ESP32_IP
    try:
        step = 5  # Mỗi lần điều chỉnh bao nhiêu độ
        if direction in ["up", "w", "Up"]:
            current_pan = max(0, current_pan - step)
        elif direction in ["down", "s", "Down"]:
            current_pan = min(180, current_pan + step)
        elif direction in ["right", "d", "Right"]:
            current_tilt = min(180, current_tilt + step)
        elif direction in ["left", "a", "Left"]:
            current_tilt = max(0, current_tilt - step)

        # Gửi yêu cầu đến ESP32
        response = requests.get(f"{ESP32_BASE_URL}/set_angle", params={
            "pan": current_pan,
            "tilt": current_tilt
        })
        print(f"Sent to ESP32: pan={current_pan}, tilt={current_tilt}")
        print("Response:", response.text)

    except requests.RequestException as e:
        print(f"Error sending request: {e}")

def sent_door_state(state):
    try:
        response = requests.get(f"{ESP32_BASE_URL}/door_state", params={"state": state})
        if response.status_code == 200:
            print("✅ Đã gửi tín hiệu đến ESP32:", response.text)
        else:
            print("❌ Lỗi khi gửi trạng thái:", response.status_code, response.text)
    except Exception as e:
        print("⚠️ Lỗi khi kết nối ESP32:", e)

