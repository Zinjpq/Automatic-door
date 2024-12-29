import RPi.GPIO as GPIO
from flask import Flask
import time

# Cấu hình GPIO
GPIO.setmode(GPIO.BCM)
PAN_SERVO_PIN = 17  # Chân GPIO kết nối với servo
GPIO.setup(PAN_SERVO_PIN, GPIO.OUT)

# Khởi tạo PWM với tần số 50Hz (servo thông thường sử dụng tần số này)
pan_pwm = GPIO.PWM(PAN_SERVO_PIN, 50)
pan_pwm.start(0)  # Bắt đầu PWM với chu kỳ ban đầu (0%)

# Hàm điều khiển servo quay tới góc nhất định
def set_servo_angle(pwm, angle):
    duty_cycle = (angle / 18) + 2
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)  # Tắt PWM sau khi điều khiển xong

# Tạo ứng dụng Flask
app = Flask(__name__)

# Định nghĩa các route để điều khiển servo
@app.route('/left', methods=['GET'])
def move_left():
    set_servo_angle(pan_pwm, 0)  # Quay servo sang trái (góc 0 độ)
    return "Servo quay sang trái!"

@app.route('/right', methods=['GET'])
def move_right():
    set_servo_angle(pan_pwm, 180)  # Quay servo sang phải (góc 180 độ)
    return "Servo quay sang phải!"

@app.route('/center', methods=['GET'])
def move_center():
    set_servo_angle(pan_pwm, 90)  # Quay servo về vị trí trung tâm (90 độ)
    return "Servo quay về trung tâm!"

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)  # Chạy Flask server trên Raspberry Pi
    except KeyboardInterrupt:
        pass
    finally:
        pan_pwm.stop()  # Dừng PWM khi kết thúc
        GPIO.cleanup()  # Làm sạch GPIO

###########################################################################################################
# Dừng PWM và làm sạch các cài đặt GPIO
pan_pwm.stop()
tilt_pwm.stop()
GPIO.cleanup()

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
# import time
# from LCD import LCD
# from flask import Flask, request
#
# lcd = LCD(2, 0x27, True)
# # Tạo ứng dụng Flask
# app = Flask(__name__)
#
# @app.route('/display', methods=['POST'])
# def display_message():
#     data = request.json
#     message = data.get('message', '')
#
#     # Hiển thị tin nhắn lên LCD
#     lcd.message(message[:16], 1)  # Dòng đầu tiên
#     lcd.message(message[16:32], 2)  # Dòng thứ hai (nếu có)
#
#     return {"status": "Message displayed"}
#
# # Keep the messages displayed for 5 seconds
# # time.sleep(5)
#
# # Clear the LCD display
# # lcd.clear()
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
