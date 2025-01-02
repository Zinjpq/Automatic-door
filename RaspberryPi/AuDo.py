from flask import Flask, request, jsonify
from LCD import LCD
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Khởi tạo LCD
lcd = LCD(2, 0x27, True)

# Khởi tạo Flask app
app = Flask(__name__)

@app.route('/display', methods=['POST'])
def display_message():
    data = request.json
    message = data.get('message', '')

    # Hiển thị tin nhắn lên LCD
    lcd.message(message[:16], 1)  # Dòng đầu tiên (tối đa 16 ký tự)
    lcd.message(message[16:32], 2)  # Dòng thứ hai (tối đa 16 ký tự, nếu có)

    return jsonify({"status": "Message displayed"})

if __name__ == '__main__':
    try:
        # Chạy Flask server trên Raspberry Pi
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()  # Làm sạch GPIO


# from flask import Flask, request, jsonify
# from LCD import LCD
# import RPi.GPIO as GPIO
#
# lcd = LCD(2, 0x27, True)
#
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
# if __name__ == '__main__':
#     try:
#         app.run(host='0.0.0.0', port=5000)  # Chạy Flask server trên Raspberry Pi
#     except KeyboardInterrupt:
#         pass
#     finally:
#         GPIO.cleanup()  # Làm sạch GPIO