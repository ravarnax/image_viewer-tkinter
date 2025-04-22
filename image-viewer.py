import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer using Tkinter")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # === THEME SETUP ===
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "btn_bg": "#ddd",
                "btn_fg": "#000",
                "btn_active": "#bbb",
                "status_fg": "#000"
            },
            "dark": {
                "bg": "#2e2e2e",
                "btn_bg": "#444",
                "btn_fg": "#fff",
                "btn_active": "#555",
                "status_fg": "#fff"
            }
        }
        self.current_theme = "dark"

        # Load icons
        self.sun_icon = ImageTk.PhotoImage(Image.open("GUI IN PYTHON\\Image Viewer\\sun_icon.png").resize((24, 24)))
        self.moon_icon = ImageTk.PhotoImage(Image.open("GUI IN PYTHON\\Image Viewer\\moon_icon.png").resize((24, 24)))

        # === STATE ===
        self.image_index = 0
        self.fullscreen = False
        self.resize_after_id = None
        self.last_size = (0, 0)
        self.pil_images = []
        self.tk_image = None

        # === UI SETUP ===
        self.image_label = tk.Label(self.root, bg='black')
        self.image_label.pack(expand=True, fill='both')

        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(fill='x')

        self.prev_button = tk.Button(self.controls_frame, text='<<', command=self.show_prev)
        self.exit_button = tk.Button(self.controls_frame, text='Exit', command=self.root.quit)
        self.next_button = tk.Button(self.controls_frame, text='>>', command=self.show_next)
        self.theme_button = tk.Button(self.controls_frame, image=self.moon_icon, command=self.toggle_theme)

        self.theme_button.pack(side='left', padx=4)
        self.prev_button.pack(side='left')
        self.exit_button.pack(side='left', expand=True)
        self.next_button.pack(side='left')

        self.status = tk.Label(self.root, text='', bd=1, relief='sunken', anchor='e')
        self.status.pack(side='bottom', fill='x')

        self.load_images()
        self.update_viewer()
        self.apply_theme()

        self.root.bind_all('<Configure>', self.on_resize)
        self.root.bind_all('<space>', self.toggle_fullscreen)
        self.root.bind_all('<Escape>', lambda e: self.set_fullscreen(False))
        self.root.bind_all('<Left>', lambda e: self.show_prev())
        self.root.bind_all('<Right>', lambda e: self.show_next())

        self.root.after(100, self.force_focus)

    def force_focus(self):
        self.root.focus_force()

    def load_images(self):
        folder_selected = filedialog.askdirectory(title="Select Folder Containing Images")
        if not folder_selected:
            return
        files = os.listdir(folder_selected)
        image_files = [f for f in files if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
        image_files.sort()
        for f in image_files:
            path = os.path.join(folder_selected, f)
            try:
                pil_img = Image.open(path)
                self.pil_images.append(pil_img)
            except Exception as e:
                print(f"Could not load image {path}: {e}")
        self.image_index = 0

    def update_viewer(self):
        if not self.pil_images:
            self.status.config(text='No images found.')
            return
        pil_img = self.pil_images[self.image_index]
        label_w = self.image_label.winfo_width()
        label_h = self.image_label.winfo_height()
        if label_w < 50 or label_h < 50:
            self.root.after(100, self.update_viewer)
            return
        resized = pil_img.copy()
        resized.thumbnail((label_w, label_h), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        self.image_label.config(image=self.tk_image)
        self.status.config(text=f"Image {self.image_index + 1} of {len(self.pil_images)}")

    def show_prev(self):
        if self.image_index > 0:
            self.image_index -= 1
            self.update_viewer()

    def show_next(self):
        if self.image_index < len(self.pil_images) - 1:
            self.image_index += 1
            self.update_viewer()

    def toggle_fullscreen(self, event=None):
        self.set_fullscreen(not self.fullscreen)

    def set_fullscreen(self, value: bool):
        self.fullscreen = value
        self.root.attributes("-fullscreen", self.fullscreen)
        if self.fullscreen:
            self.controls_frame.pack_forget()
            self.status.pack_forget()
        else:
            self.controls_frame.pack(fill='x')
            self.status.pack(side='bottom', fill='x')
        self.update_viewer()

    def on_resize(self, event):
        if self.resize_after_id:
            self.root.after_cancel(self.resize_after_id)
        self.resize_after_id = self.root.after(300, self.delayed_resize)

    def delayed_resize(self):
        width = self.image_label.winfo_width()
        height = self.image_label.winfo_height()
        if (width, height) != self.last_size:
            self.last_size = (width, height)
            self.update_viewer()

    # === THEME FUNCTIONS ===
    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
        self.image_label.config(bg=theme["bg"])
        self.controls_frame.config(bg=theme["bg"])
        self.status.config(bg=theme["bg"], fg=theme["status_fg"])

        for btn in [self.prev_button, self.exit_button, self.next_button]:
            btn.config(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_active"])

        self.theme_button.config(
            image=self.sun_icon if self.current_theme == "dark" else self.moon_icon,
            bg=theme["bg"],
            activebackground=theme["bg"]
        )

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
