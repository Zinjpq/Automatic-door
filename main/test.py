import cv2
import numpy as np
import pytesseract

def detect_license_plate(image_path):
    # Đọc ảnh
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Phát hiện cạnh
    edged = cv2.Canny(blur, 30, 200)
    
    # Tìm các contour
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Lọc các contour có thể là biển số xe
    license_plate = None
    for contour in contours:
        # Tìm hình chữ nhật xung quanh contour
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        
        # Kiểm tra tỷ lệ chiều dài, chiều cao phù hợp với biển số
        if 2 <= aspect_ratio <= 6:  # Giả định tỷ lệ của biển số
            license_plate = image[y:y + h, x:x + w]
            break
    
    # Nếu tìm thấy biển số xe, trả về
    if license_plate is not None:
        return license_plate
    else:
        return None

def extract_characters(license_plate_image):
    # Chuyển đổi biển số thành ảnh grayscale và nhị phân
    gray_plate = cv2.cvtColor(license_plate_image, cv2.COLOR_BGR2GRAY)
    _, binary_plate = cv2.threshold(gray_plate, 128, 255, cv2.THRESH_BINARY_INV)
    
    # Tìm các contour của các ký tự
    contours, _ = cv2.findContours(binary_plate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    characters = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Cắt từng ký tự
        char_image = binary_plate[y:y + h, x:x + w]
        characters.append(char_image)
    
    return characters

def save_characters(characters, output_folder):
    for idx, char_image in enumerate(characters):
        char_path = f"{output_folder}/char_{idx}.png"
        cv2.imwrite(char_path, char_image)

# Sử dụng hàm để phát hiện biển số và tách các ký tự
image_path = 'image4.jpg'
license_plate = detect_license_plate(image_path)

if license_plate is not None:
    cv2.imshow("License Plate", license_plate)
    characters = extract_characters(license_plate)
    
    # Lưu các ký tự
    save_characters(characters, './char_library')
    print("Saved characters to './char_library'")
else:
    print("License plate not found")

cv2.waitKey(0)
cv2.destroyAllWindows()
