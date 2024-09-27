import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Thư viện cần thiết để hiển thị hình ảnh


# Hàm để tạo mục lịch sử
def create_history_item(container, image_path, plate_number, date_time):
    # Khung chính cho mỗi mục
    frame = tk.Frame(container, borderwidth=1, relief="solid", padx=5, pady=5)
    frame.pack(fill="x", pady=5)

    # Ảnh biển số
    img = Image.open(image_path)
    img = img.resize((300, 100), Image.Resampling.LANCZOS)  # Điều chỉnh kích thước ảnh
    photo = ImageTk.PhotoImage(img)
    image_label = tk.Label(frame, image=photo)
    image_label.image = photo  # Lưu tham chiếu để tránh bị xóa bộ nhớ
    image_label.grid(row=0, column=0, rowspan=2)

    # Biển số xe
    plate_label = tk.Label(frame, text=plate_number, font=("Helvetica", 14))
    plate_label.grid(row=0, column=1, padx=10, sticky="w")

    # Thời gian
    time_label = tk.Label(frame, text=date_time, font=("Helvetica", 12))
    time_label.grid(row=1, column=1, padx=10, sticky="w")


# Tạo cửa sổ chính
root = tk.Tk()
root.title("History")

# Tiêu đề chính
title_frame = tk.Frame(root, borderwidth=1, relief="solid")
title_frame.pack(fill="x", pady=10, padx=10)
icon_label = tk.Label(title_frame, text="🚗", font=("Helvetica", 16))
icon_label.pack(side="left", padx=10)
title_label = tk.Label(title_frame, text="History", font=("Helvetica", 16, "bold"))
title_label.pack(side="left")

# Khung cuộn cho các mục lịch sử
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Layout cho khung cuộn và scrollbar
canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar.pack(side="right", fill="y")

# Tạo các mục lịch sử (ví dụ)
create_history_item(scrollable_frame, "Image/image2.jpg", "36A-083.53", "21:58 13/09/2024")
create_history_item(scrollable_frame, "Image/image3.jpg", "36A-083.53", "21:58 13/09/2024")
create_history_item(scrollable_frame, "Image/image4.jpg", "36A-083.53", "21:58 13/09/2024")
create_history_item(scrollable_frame, "Image/image5.jpg", "18A-123.45", "21:58 13/09/2024")

root.mainloop()
