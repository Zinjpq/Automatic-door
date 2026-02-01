import os
import sqlite3
import cv2
from datetime import datetime

class VehicleLogger:
    def __init__(self, base_dir="data"):
        """
        Khởi tạo logger.
        :param base_dir: Thư mục gốc để lưu dữ liệu (mặc định là 'data')
        """
        self.base_dir = base_dir
        self.images_dir = os.path.join(base_dir, "captured_plates")
        self.db_path = os.path.join(base_dir, "vehicle_logs.db")
        
        # Tạo cấu trúc thư mục cơ bản nếu chưa có
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
            
        # Khởi tạo Database
        self._init_db()

    def _init_db(self):
        """Tạo bảng database nếu chưa tồn tại"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_plate TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                image_path TEXT,
                status TEXT -- Ví dụ: 'ALLOWED', 'DENIED', 'UNKNOWN'
            )
        ''')
        conn.commit()
        conn.close()

    def log_vehicle(self, frame, license_plate_text, status="UNKNOWN"):
        """
        Lưu ảnh và ghi log vào DB.
        
        :param frame: Ảnh gốc (numpy array từ OpenCV)
        :param license_plate_text: Biển số xe đã nhận diện (String)
        :param status: Trạng thái (cho phép mở cửa hay không)
        """
        now = datetime.now()
        
        # 1. Tạo đường dẫn thư mục theo ngày: data/captured_plates/2026/02/01/
        folder_path = os.path.join(
            self.images_dir,
            str(now.year),
            f"{now.month:02d}",
            f"{now.day:02d}"
        )
        os.makedirs(folder_path, exist_ok=True) # Tự tạo thư mục nếu chưa có

        # 2. Tạo tên file ảnh: 14-30-55_60A99999.jpg
        safe_plate_name = license_plate_text.replace(" ", "").replace("-", "")
        file_name = f"{now.strftime('%H-%M-%S')}_{safe_plate_name}.jpg"
        full_image_path = os.path.join(folder_path, file_name)

        # 3. Lưu ảnh xuống đĩa
        try:
            cv2.imwrite(full_image_path, frame)
        except Exception as e:
            print(f"Lỗi khi lưu ảnh: {e}")
            return False

        # 4. Ghi thông tin vào Database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO vehicle_history (license_plate, timestamp, image_path, status)
                VALUES (?, ?, ?, ?)
            ''', (license_plate_text, now.strftime('%Y-%m-%d %H:%M:%S'), full_image_path, status))
            conn.commit()
            conn.close()
            print(f"Đã log xe: {license_plate_text} tại {full_image_path}")
            return True
        except Exception as e:
            print(f"Lỗi khi ghi database: {e}")
            return False

    def get_recent_logs(self, limit=10):
        """Lấy danh sách xe ra vào gần nhất để hiển thị lên UI"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vehicle_history ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows