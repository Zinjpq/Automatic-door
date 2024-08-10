import concurrent.futures  # Thêm thư viện concurrent.futures để xử lý song song
import urllib.request  # Thêm thư viện urllib để gửi yêu cầu HTTP
import cv2  # Thêm thư viện OpenCV
import cvlib as cv  # Thêm thư viện cvlib
import numpy as np  # Thêm thư viện numpy
from cvlib.object_detection import draw_bbox  # Thêm hàm draw_bbox từ cvlib

# URL của hình ảnh từ camera
url = 'http://192.168.49.162/cam-hi.jpg'
im = None


# Hàm hiển thị truyền tải trực tiếp
def run1():
    cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
    while True:
        # Gửi yêu cầu HTTP để lấy hình ảnh từ URL
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)

        # Hiển thị hình ảnh trong cửa sổ
        cv2.imshow('live transmission', im)
        key = cv2.waitKey(5)
        if key == ord('q'):  # Nhấn phím 'q' để thoát
            break

    cv2.destroyAllWindows()


# Hàm phát hiện đối tượng trong hình ảnh
def run2():
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)
    while True:
        # Gửi yêu cầu HTTP để lấy hình ảnh từ URL
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)

        # Phát hiện các đối tượng thông thường trong hình ảnh
        bbox, label, conf = cv.detect_common_objects(im)
        im = draw_bbox(im, bbox, label, conf)

        # Hiển thị hình ảnh với các hộp bao quanh đối tượng
        cv2.imshow('detection', im)
        key = cv2.waitKey(5)
        if key == ord('q'):  # Nhấn phím 'q' để thoát
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("started")
    # Sử dụng ProcessPoolExecutor để chạy hai hàm song song
    with concurrent.futures.ProcessPoolExecutor() as executer:
        f1 = executer.submit(run1)
        f2 = executer.submit(run2)
