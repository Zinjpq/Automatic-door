import requests

esp32_ip = "http://192.168.1.xxx"  # IP ESP32
pan_angle = 90
tilt_angle = 45

response = requests.get(f"{esp32_ip}/set_angle", params={"pan": pan_angle, "tilt": tilt_angle})
print(response.text)

# ESP32-CAM URL and Control URLs
ESP32_BASE_URL = 'http://192.168.4.184'
CAMERA_URL = ESP32_BASE_URL + '/cam'
RasPi_Base_URL = "http://192.168.4.2:5000"

from flask import Flask, request

app = Flask(__name__)

@app.route("/door_status", methods=["POST"])
def door_status():
    status = request.json.get("status")
    print(f"Cửa hiện tại: {status}")
    return "OK"





app.run(host="0.0.0.0", port=5000)