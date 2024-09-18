import requests
import cv2  # Nếu bạn vẫn muốn sử dụng cv2

# Địa chỉ IP của ESP32-CAM (thay đổi thành IP thực của ESP32 sau khi kết nối WiFi)
url1 = 'http://192.168.0.103/open'
url2 = 'http://192.168.0.103/close'

# Hiển thị hướng dẫn sử dụng
print("Nhấn 1 để mở cửa, 2 để đóng cửa, q để thoát")

# Tạo một cửa sổ trống nếu bạn cần sử dụng cv2.waitKey()
cv2.namedWindow("ESP32 Control", cv2.WINDOW_NORMAL)
cv2.imshow("ESP32 Control", 255 * (1))  # Hiển thị cửa sổ trống

while True:
    key = cv2.waitKey(1)  # Thời gian chờ ngắn hơn
    if key == ord('1'):  # Nhấn phím '1' để gửi tín hiệu mở cửa
        try:
            response1 = requests.get(url1)
            if response1.status_code == 200:
                print("Tín hiệu đã gửi thành công!")
                print("Phản hồi từ ESP32:", response1.text)  # In ra phản hồi từ ESP32-CAM
            else:
                print(f"Lỗi: {response1.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối: {e}")

    elif key == ord('2'):  # Nhấn phím '2' để gửi tín hiệu đóng cửa
        try:
            response2 = requests.get(url2)
            if response2.status_code == 200:
                print("Tín hiệu đã gửi thành công!")
                print("Phản hồi từ ESP32:", response2.text)  # In ra phản hồi từ ESP32-CAM
            else:
                print(f"Lỗi: {response2.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối: {e}")

    elif key == ord('q'):  # Nhấn phím 'q' để thoát
        print("Thoát chương trình")
        break

# Đóng cửa sổ OpenCV nếu có
cv2.destroyAllWindows()
