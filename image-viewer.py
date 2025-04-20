from tkinter import *
from PIL import Image, ImageTk
import os

# === MAIN WINDOW ===
root = Tk()
root.title("Image Viewer")
root.resizable(False, False)

# === CONFIG ===
IMAGE_FOLDER = "GUI IN PYTHON\Image Viewer\images"
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 500

# === THEME SETTINGS ===
themes = {
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

current_theme = "dark"  # Start with dark mode

# === LOAD IMAGES ===
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
image_files.sort()
image_paths = [os.path.join(IMAGE_FOLDER, f) for f in image_files]

images = [
    ImageTk.PhotoImage(Image.open(path).resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS))
    for path in image_paths
]


# === IMAGE DISPLAY ===
image_index = 0
image_label = Label(image=images[image_index])
image_label.grid(row=0, column=0, columnspan=3)

# === STATUS BAR ===
status = Label(root, text=f"Image 1 of {len(images)}", bd=1, relief=SUNKEN, anchor=E)
status.grid(row=2, column=0, columnspan=3, sticky=W+E)

# === FUNCTIONS ===
def forward():
    global image_index
    if image_index < len(images) - 1:
        image_index += 1
        update_viewer()

def back():
    global image_index
    if image_index > 0:
        image_index -= 1
        update_viewer()

def update_viewer():
    image_label.config(image=images[image_index])
    status.config(text=f"Image {image_index + 1} of {len(images)}")
    update_buttons()

def update_buttons():
    back_button.config(state=NORMAL if image_index > 0 else DISABLED)
    forward_button.config(state=NORMAL if image_index < len(images) - 1 else DISABLED)

def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    apply_theme()

def apply_theme():
    theme = themes[current_theme]
    root.configure(bg=theme["bg"])
    image_label.config(bg=theme["bg"])
    status.config(bg=theme["bg"], fg=theme["status_fg"])
    back_button.config(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_active"])
    forward_button.config(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_active"])
    exit_button.config(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_active"])
    toggle_button.config(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_active"])
    root.title("Image Viewer - Dark Mode" if current_theme == "dark" else "Image Viewer - Light Mode")

# === BUTTONS ===
back_button = Button(root, text="<<", command=back)
exit_button = Button(root, text="Exit", command=root.quit)
forward_button = Button(root, text=">>", command=forward)
toggle_button = Button(root, text="Toggle Theme", command=toggle_theme)

back_button.grid(row=1, column=0)
exit_button.grid(row=1, column=1)
forward_button.grid(row=1, column=2)
toggle_button.grid(row=3, column=0, columnspan=3, pady=10)

update_buttons()
apply_theme()
root.mainloop()
