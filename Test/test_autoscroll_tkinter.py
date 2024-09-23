import os
import time
import customtkinter as ctk
from tkinter import filedialog


class AutoUpdateGUI(ctk.CTk):
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.title("Biển Số Xe - Tự Động Cập Nhật")
        self.geometry("600x400")

        # Tạo khung cuộn
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=580, height=350)
        self.scroll_frame.grid(row=0, column=0, padx=10, pady=10)

        # Nút cập nhật thủ công (nếu cần)
        self.refresh_button = ctk.CTkButton(self, text="Cập Nhật", command=self.update_file_list)
        self.refresh_button.grid(row=1, column=0, padx=10, pady=10)

        # Lưu danh sách file đã hiện ra để tránh lặp
        self.file_list = []

        # Gọi hàm cập nhật lần đầu
        self.update_file_list()

        # Kiểm tra file mới định kỳ (mỗi 5 giây)
        self.check_new_files()

    def update_file_list(self):
        # Đọc danh sách file từ thư mục
        files = os.listdir(self.folder_path)
        for filename in sorted(files):
            if filename.endswith(".txt") and filename not in self.file_list:
                self.file_list.append(filename)
                # Thêm tên file vào khung scroll
                label = ctk.CTkLabel(self.scroll_frame, text=filename)
                label.pack(pady=5)

    def check_new_files(self):
        # Kiểm tra thư mục cứ 5 giây một lần
        self.update_file_list()
        self.after(5000, self.check_new_files)


def capture_license_plate(folder_path, plate_number):
    current_time = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{plate_number}_{current_time}.txt"
    filepath = os.path.join(folder_path, filename)

    # Mở file với encoding UTF-8
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Biển số: {plate_number}\nThời gian: {current_time}")

    print(f"Lưu file: {filename}")


if __name__ == "__main__":
    # Chọn thư mục để lưu và đọc file
    folder = filedialog.askdirectory(title="Chọn thư mục chứa file biển số xe")

    # Giả lập lưu file biển số
    capture_license_plate(folder, "29A-12345")

    # Chạy GUI
    app = AutoUpdateGUI(folder)
    app.mainloop()
