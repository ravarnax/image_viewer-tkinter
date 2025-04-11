# importing modules
from tkinter import *
from PIL import Image, ImageTk
import os
# create main window
root = Tk()
root.title("Image Viewer using Tkinter")
# root.geometry("800x500")
root.resizable(False, False)

# Image display size
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 500

# Path to the "images" folder(relative path)
IMAGE_FOLDER = "GUI IN PYTHON\Image Viewer\images"

# Get all images files in current directory
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
image_files.sort()  # sort files alphabetically

# Full path to images
image_paths = [os.path.join(IMAGE_FOLDER, f) for f in image_files]

# load images using PIL
images = [ImageTk.PhotoImage(Image.open(path).resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS))
          for path in image_paths]

# Display first image
image_index = 0
image_label = Label(image=images[image_index])
image_label.grid(row=0, column=0, columnspan=3)

# Status Label
status = Label(root, text=f'Image 1 of {len(images)}', bd=1, relief=SUNKEN, anchor=E)
status.grid(row=2, column=0, columnspan=3, sticky=W+E)

# Functions for navigation
def forward():
    global image_index
    image_index += 1
    if image_index >= len(images):
        image_index = len(images) - 1
    update_viewer()
    
def back():
    global image_index
    image_index -= 1
    if image_index < 0:
        image_index = 0
    update_viewer()
    
def update_viewer():
    image_label.config(image=images[image_index])
    status.config(text=f'Image {image_index+1} of {len(images)}')
    update_buttons()
    
def update_buttons():
    if image_index == 0:
        back_button.config(state=DISABLED)
    else:
        back_button.config(state=NORMAL)
        
    if image_index == len(images) - 1:
        forward_button.config(state=DISABLED)
    else:
        forward_button.config(state=NORMAL)
        
# Navigation Buttons
back_button = Button(root, text='<<', command=back)
forward_button = Button(root, text='>>', command=forward)
exit_button = Button(root, text='Exit', command=root.quit)

back_button.grid(row=1, column=0)
exit_button.grid(row=1, column=1)
forward_button.grid(row=1, column=2)

update_buttons() # To disable 'back on first image

root.mainloop()