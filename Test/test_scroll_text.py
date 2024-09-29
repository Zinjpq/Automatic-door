import tkinter as tk
from tkinter import messagebox

# Hàm để lưu nội dung trong Text widget vào file
def save_to_file():
    content = text_widget.get(1.0, tk.END).strip()  # Lấy nội dung từ Text widget và loại bỏ khoảng trắng thừa
    if content:  # Kiểm tra xem có nội dung để lưu không
        with open("bien_so_xe.txt", "w") as file:
            file.write(content)
        messagebox.showinfo("Thông báo", "Đã lưu biển số xe vào file bien_so_xe.txt")
    else:
        messagebox.showwarning("Thông báo", "Không có nội dung để lưu")

# Hàm để xóa nội dung trong Text widget
def clear_text():
    text_widget.delete(1.0, tk.END)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Biển số xe hợp lệ")

# Tạo Label hướng dẫn
label = tk.Label(root, text="Biển số xe hợp lệ: VD: 30A-123.45")
label.pack(pady=10)

# Tạo khung chứa để đặt thanh cuộn và Text widget
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Tạo Text widget để nhập biển số xe
text_widget = tk.Text(frame, wrap="word", height=10, width=50)
text_widget.pack(side="left", fill="both", expand=True)

# Tạo thanh cuộn dọc
scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")

# Liên kết thanh cuộn với Text widget
text_widget.config(yscrollcommand=scrollbar.set)

# Tạo khung chứa các nút điều khiển
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Tạo nút lưu vào file
save_button = tk.Button(button_frame, text="Lưu vào file", command=save_to_file)
save_button.pack(side="left", padx=5)

# Tạo nút xóa nội dung
clear_button = tk.Button(button_frame, text="Xóa", command=clear_text)
clear_button.pack(side="right", padx=5)

# Chạy vòng lặp chính của ứng dụng
root.mainloop()
