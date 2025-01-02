import RPi.GPIO as GPIO
import time
from flask import Flask

# Thiết lập GPIO
GPIO.setmode(GPIO.BCM)
pan_pin = 17  # Pin điều khiển servo Pan
tilt_pin = 27  # Pin điều khiển servo Tilt
servo_360_pin = 22  # Pin điều khiển servo 360

# Khởi tạo PWM
GPIO.setup(pan_pin, GPIO.OUT)
GPIO.setup(tilt_pin, GPIO.OUT)
GPIO.setup(servo_360_pin, GPIO.OUT)

pan_pwm = GPIO.PWM(pan_pin, 50)  # Tần số 50Hz
tilt_pwm = GPIO.PWM(tilt_pin, 50)
servo_360_pwm = GPIO.PWM(servo_360_pin, 50)

pan_pwm.start(7.5)  # Góc 90 độ
tilt_pwm.start(7.5)
servo_360_pwm.start(0)

# Các biến lưu trạng thái góc
pan_angle = 90
tilt_angle = 90

# Tạo web server với Flask
app = Flask(__name__)

def set_angle(pwm, angle):
    duty_cycle = 2.5 + (angle / 18)  # Tính toán chu kỳ làm việc
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3)  # Đợi servo di chuyển
    pwm.ChangeDutyCycle(0)  # Ngừng gửi tín hiệu để tránh quá nhiệt

@app.route('/left')
def move_left():
    global pan_angle
    pan_angle = max(0, pan_angle - 10)  # Giới hạn góc 0-180
    set_angle(pan_pwm, pan_angle)
    return f"Pan angle: {pan_angle}"

@app.route('/right')
def move_right():
    global pan_angle
    pan_angle = min(180, pan_angle + 10)  # Giới hạn góc 0-180
    set_angle(pan_pwm, pan_angle)
    return f"Pan angle: {pan_angle}"

@app.route('/up')
def move_up():
    global tilt_angle
    tilt_angle = max(0, tilt_angle - 10)  # Giới hạn góc 0-180
    set_angle(tilt_pwm, tilt_angle)
    return f"Tilt angle: {tilt_angle}"

@app.route('/down')
def move_down():
    global tilt_angle
    tilt_angle = min(180, tilt_angle + 10)  # Giới hạn góc 0-180
    set_angle(tilt_pwm, tilt_angle)
    return f"Tilt angle: {tilt_angle}"

@app.route('/open')
def open_servo():
    # Quay phải 3 giây
    servo_360_pwm.ChangeDutyCycle(10)  # Tín hiệu quay phải
    time.sleep(3)
    servo_360_pwm.ChangeDutyCycle(0)  # Dừng

    # Đợi 5 giây và quay trái
    time.sleep(5)
    servo_360_pwm.ChangeDutyCycle(5)  # Tín hiệu quay trái
    time.sleep(3)
    servo_360_pwm.ChangeDutyCycle(0)  # Dừng
    return "Servo 360 activated"

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)  # Chạy server Flask
    except KeyboardInterrupt:
        pan_pwm.stop()
        tilt_pwm.stop()
        servo_360_pwm.stop()
        GPIO.cleanup()

# import RPi.GPIO as GPIO
# from flask import Flask
# import time
# import time
# from flask import Flask, request
#
#
# # Cấu hình GPIO
# PAN_SERVO_PIN = 17  # Chân GPIO kết nối với servo
# GPIO.setup(PAN_SERVO_PIN, GPIO.OUT)
#
# # Khởi tạo PWM với tần số 50Hz (servo thông thường sử dụng tần số này)
# pan_pwm = GPIO.PWM(PAN_SERVO_PIN, 50)
# pan_pwm.start(0)  # Bắt đầu PWM với chu kỳ ban đầu (0%)
#
# # Hàm điều khiển servo quay tới góc nhất định
# def set_servo_angle(pwm, angle):
#     duty_cycle = (angle / 18) + 2
#     pwm.ChangeDutyCycle(duty_cycle)
#     time.sleep(1)
#     pwm.ChangeDutyCycle(0)  # Tắt PWM sau khi điều khiển xong
#

#
# # Định nghĩa các route để điều khiển servo
# @app.route('/left', methods=['GET'])
# def move_left():
#     # set_servo_angle(pan_pwm, 0)  # Quay servo sang trái (góc 0 độ)
#     return "Servo quay sang trái!"
#
# @app.route('/right', methods=['GET'])
# def move_right():
#     # set_servo_angle(pan_pwm, 180)  # Quay servo sang phải (góc 180 độ)
#     return "Servo quay sang phải!"
#
# @app.route('/center', methods=['GET'])
# def move_center():
#     # set_servo_angle(pan_pwm, 90)  # Quay servo về vị trí trung tâm (90 độ)
#     return "Servo quay về trung tâm!"
#

#
# ###########################################################################################################
# # Dừng PWM và làm sạch các cài đặt GPIO
# pan_pwm.stop()
# tilt_pwm.stop()
# GPIO.cleanup()

# import RPi.GPIO as GPIO
# import MFRC522
# import signal
#
# continue_reading = True
#
#
# # Capture SIGINT for cleanup when the script is aborted
# def end_read(signal, frame):
#     global continue_reading
#     print
#     "Ctrl+C captured, ending read."
#     continue_reading = False
#     GPIO.cleanup()
#
#
# # Hook the SIGINT
# signal.signal(signal.SIGINT, end_read)
#
# # Create an object of the class MFRC522
# MIFAREReader = MFRC522.MFRC522()
#
# # Welcome message
# print
# "Welcome to the MFRC522 data read example"
# print
# "Press Ctrl-C to stop."
#
# # This loop keeps checking for chips. If one is near it will get the UID and authenticate
# while continue_reading:
#
#     # Scan for cards
#     (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
#
#     # If a card is found
#     if status == MIFAREReader.MI_OK:
#         print
#         "Card detected"
#
#     # Get the UID of the card
#     (status, uid) = MIFAREReader.MFRC522_Anticoll()
#
#     # If we have the UID, continue
#     if status == MIFAREReader.MI_OK:
#
#         # Print UID
#         print
#         "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
#
#         # This is the default key for authentication
#         key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
#
#         # Select the scanned tag
#         MIFAREReader.MFRC522_SelectTag(uid)
#
#         # Authenticate
#         status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
#
#         # Check if authenticated
#         if status == MIFAREReader.MI_OK:
#             MIFAREReader.MFRC522_Read(8)
#             MIFAREReader.MFRC522_StopCrypto1()
#         else:
#             print
#             "Authentication error"


###########################################################################################################

