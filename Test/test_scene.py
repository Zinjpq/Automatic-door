import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Automatic Door by Zinj")
        self.geometry("900x600")

        # Create the main container (Tab Controller)
        tab_control = ttk.Notebook(self)

        # Home tab
        self.home_frame = tk.Frame(tab_control)
        tab_control.add(self.home_frame, text='Home')
        self.create_home_scene(self.home_frame)

        # Camera Control tab
        self.control_frame = tk.Frame(tab_control)
        tab_control.add(self.control_frame, text='Camera Control')
        self.create_control_scene(self.control_frame)

        # Add the tab controller to the main window
        tab_control.pack(expand=1, fill="both")

    def create_home_scene(self, frame):
        # Left menu panel
        menu_frame = tk.Frame(frame, width=200, bg='gray')
        menu_frame.pack(side='left', fill='y')

        # Buttons for menu navigation
        home_button = tk.Button(menu_frame, text='Home')
        home_button.pack(fill='x')

        license_plate_button = tk.Button(menu_frame, text='License plate image')
        license_plate_button.pack(fill='x')

        store_button = tk.Button(menu_frame, text='Store')
        store_button.pack(fill='x')

        settings_button = tk.Button(menu_frame, text='Settings')
        settings_button.pack(fill='x')

        # Right side for main content (URL input and stream)
        main_frame = tk.Frame(frame, bg='white')
        main_frame.pack(side='right', expand=True, fill='both')

        # URL Input field
        url_label = tk.Label(main_frame, text='Input URL:')
        url_label.pack(pady=10)

        url_entry = tk.Entry(main_frame, width=40)
        url_entry.pack()

        submit_button = tk.Button(main_frame, text='Submit')
        submit_button.pack(pady=10)

        # Live stream placeholder
        stream_label = tk.Label(main_frame, text='Live stream', font=('Arial', 16))
        stream_label.pack(pady=20)

        stream_placeholder = tk.Canvas(main_frame, width=600, height=300, bg='lightblue')
        stream_placeholder.pack(pady=10)

        # History section
        history_label = tk.Label(main_frame, text='History', font=('Arial', 12))
        history_label.pack(pady=10)

        history_list = tk.Listbox(main_frame, height=4)
        history_list.pack()

        # Adding dummy history items
        history_list.insert(0, "36A-083.53 - 21:58 13/09/2024")
        history_list.insert(1, "36A-083.53 - 21:58 13/09/2024")
        history_list.insert(2, "18A-123.45 - 21:58 13/09/2024")

    def create_control_scene(self, frame):
        # Left menu panel similar to the home scene
        menu_frame = tk.Frame(frame, width=200, bg='gray')
        menu_frame.pack(side='left', fill='y')

        home_button = tk.Button(menu_frame, text='Home')
        home_button.pack(fill='x')

        license_plate_button = tk.Button(menu_frame, text='License plate image')
        license_plate_button.pack(fill='x')

        store_button = tk.Button(menu_frame, text='Store')
        store_button.pack(fill='x')

        settings_button = tk.Button(menu_frame, text='Settings')
        settings_button.pack(fill='x')

        # Right side for main content (URL input and stream)
        main_frame = tk.Frame(frame, bg='white')
        main_frame.pack(side='right', expand=True, fill='both')

        # URL Input field
        url_label = tk.Label(main_frame, text='Input URL:')
        url_label.pack(pady=10)

        url_entry = tk.Entry(main_frame, width=40)
        url_entry.pack()

        submit_button = tk.Button(main_frame, text='Submit')
        submit_button.pack(pady=10)

        # Live stream placeholder
        stream_label = tk.Label(main_frame, text='Live stream', font=('Arial', 16))
        stream_label.pack(pady=20)

        stream_placeholder = tk.Canvas(main_frame, width=600, height=300, bg='lightblue')
        stream_placeholder.pack(pady=10)

        # Camera control buttons
        control_frame = tk.Frame(main_frame)
        control_frame.pack(pady=10)

        zoom_in_button = tk.Button(control_frame, text='Zoom In')
        zoom_in_button.grid(row=0, column=1)

        up_button = tk.Button(control_frame, text='Up')
        up_button.grid(row=0, column=2)

        zoom_out_button = tk.Button(control_frame, text='Zoom Out')
        zoom_out_button.grid(row=1, column=1)

        left_button = tk.Button(control_frame, text='Left')
        left_button.grid(row=1, column=0)

        none_button = tk.Button(control_frame, text='None')
        none_button.grid(row=1, column=2)

        right_button = tk.Button(control_frame, text='Right')
        right_button.grid(row=1, column=3)

        reset_button = tk.Button(control_frame, text='Reset')
        reset_button.grid(row=2, column=2)


if __name__ == "__main__":
    app = App()
    app.mainloop()
