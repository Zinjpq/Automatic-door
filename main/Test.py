import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class LicensePlateManager:
    def __init__(self, root):
        self.root = root
        self.root.title("License Plate Manager")
        self.root.geometry("1280x720")

        # Frame chính
        self.main_frame = tk.Frame(root, width=336, height=480, bg="lightgray", relief="solid", bd=1)
        self.main_frame.place(x=800, y=136)

        # Tiêu đề phía trên
        self.title_label = tk.Label(self.main_frame, text="Tên biển hợp lệ", bg="lightgray", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Frame cuộn
        self.scroll_frame = tk.Frame(self.main_frame, bg="white")
        self.scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas để hỗ trợ cuộn
        self.canvas = tk.Canvas(self.scroll_frame, bg="white")
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        # Scrollbar dọc
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Vị trí scrollbar và canvas
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Kết nối canvas và frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Danh sách lưu các biển số
        self.labels = []

        # Phần thêm mới biển
        self.add_frame = tk.Frame(self.main_frame, bg="lightgray")
        self.add_frame.pack(pady=10)

        self.entry = tk.Entry(self.add_frame, font=("Arial", 12), width=20)
        self.entry.grid(row=0, column=0, padx=5)

        self.add_button = tk.Button(self.add_frame, text="Thêm biển", command=self.add_label, font=("Arial", 12))
        self.add_button.grid(row=0, column=1, padx=5)

    def add_label(self):
        text = self.entry.get().strip()
        if text:
            # Tạo frame cho label và nút xóa
            label_container = tk.Frame(self.scrollable_frame, bg="white")
            label_container.pack(fill=tk.X, padx=5, pady=2)

            label = tk.Label(label_container, text=text, bg="white", font=("Arial", 12))
            label.pack(side=tk.LEFT, padx=5)

            delete_button = tk.Button(
                label_container, text="Xóa", font=("Arial", 10),
                command=lambda: self.delete_label(label_container)
            )
            delete_button.pack(side=tk.RIGHT, padx=5)

            # Lưu label
            self.labels.append(label_container)

            # Xóa nội dung trong ô nhập
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên biển!")

    def delete_label(self, label_container):
        label_container.destroy()
        self.labels.remove(label_container)


if __name__ == "__main__":
    root = tk.Tk()
    app = LicensePlateManager(root)
    root.mainloop()
