import cv2
import numpy as np
import os

# Hàm để load các ký tự từ thư viện ký tự
def load_char_library(library_path):
    char_dict = {}
    for filename in os.listdir(library_path):
        if filename.endswith(".png"):  # Giả sử ký tự lưu dưới dạng PNG
            char = filename[0]  # Giả định tên file là ký tự, ví dụ 'A.png'
            img = cv2.imread(os.path.join(library_path, filename), 0)  # Load ảnh mức xám
            char_dict[char] = img
    return char_dict

# Hàm để nhận diện ký tự từ ảnh biển số xe
def recognize_license_plate(image_path, char_library):
    # Load ảnh biển số xe
    plate_img = cv2.imread(image_path, 0)
    
    # Tiền xử lý: Chuyển sang ảnh nhị phân
    _, binary_img = cv2.threshold(plate_img, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Tìm các contour (vùng ký tự)
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    recognized_text = ""
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        char_img = binary_img[y:y+h, x:x+w]  # Cắt ký tự
        
        # Tìm ký tự tương ứng từ thư viện
        best_match = None
        best_score = float('inf')
        for char, template in char_library.items():
            resized_char_img = cv2.resize(char_img, (template.shape[1], template.shape[0]))
            score = np.sum((template - resized_char_img) ** 2)  # Tính độ lệch bình phương
            if score < best_score:
                best_score = score
                best_match = char
        
        recognized_text += best_match
    
    return recognized_text

# Sử dụng
char_library_path = "char_library/1"
license_plate_image = 'image/image11.jpg'

# Load thư viện ký tự
char_library = load_char_library(char_library_path)

# Nhận diện biển số xe
recognized_plate = recognize_license_plate(license_plate_image, char_library)
print("Biển số xe:", recognized_plate)
