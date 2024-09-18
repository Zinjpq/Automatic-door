import requests

# Địa chỉ IP của ESP32 ở chế độ AP (thường là 192.168.4.1 nếu không thay đổi)
esp32_ip = "http://192.168.4.1"


def get_root_page():
    try:
        # Gửi yêu cầu GET để truy cập trang chủ ("/") của ESP32
        response = requests.get(esp32_ip + "/")

        # Kiểm tra nếu phản hồi thành công (status code 200)
        if response.status_code == 200:
            print("Page content:\n")
            print(response.text)  # In nội dung HTML của trang
        else:
            print(f"Failed to load page, status code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")


def send_wifi_credentials(ssid, password):
    try:
        # Gửi yêu cầu POST để gửi thông tin Wi-Fi ("/save")
        data = {
            'ssid': ssid,
            'password': password
        }
        response = requests.post(esp32_ip + "/save", data=data)

        # Kiểm tra nếu phản hồi thành công
        if response.status_code == 200:
            print("Wi-Fi credentials sent successfully")
            print(response.text)  # In nội dung phản hồi từ ESP32
        else:
            print(f"Failed to send credentials, status code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Lấy nội dung trang chủ từ ESP32
    get_root_page()

    # Gửi thông tin Wi-Fi mới đến ESP32
    ssid = input("Enter Wi-Fi SSID: ")
    password = input("Enter Wi-Fi password: ")
    send_wifi_credentials(ssid, password)
