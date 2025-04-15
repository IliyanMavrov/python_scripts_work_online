#!/usr/bin/python3

import cv2
import numpy as np
from tkinter import Tk, filedialog, Button, Label, OptionMenu, StringVar
from PIL import Image, ImageTk
import os

# --- Cartoon Styles ---
def cartoonize_classic(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray_blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 2)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    return cv2.bitwise_and(color, color, mask=edges)

def cartoonize_sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

def cartoonize_pencil(img):
    dst_gray, dst_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    return dst_color

def cartoonize_oilpaint(img):
    return cv2.xphoto.oilPainting(img, 7, 1)

def cartoonize_smooth(img):
    return cv2.stylization(img, sigma_s=60, sigma_r=0.07)

def cartoonize_watercolor(img):
    return cv2.stylization(img, sigma_s=150, sigma_r=0.25)

def cartoonize_detail_enhance(img):
    return cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)

def cartoonize_hdr(img):
    return cv2.detailEnhance(img, sigma_s=30, sigma_r=0.5)

def cartoonize_color_pencil(img):
    gray, color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.1, shade_factor=0.02)
    return color

def cartoonize_comic_book(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 2)
    color = cv2.bilateralFilter(img, 10, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    # Boost contrast like a comic
    hsv = cv2.cvtColor(cartoon, cv2.COLOR_BGR2HSV)
    hsv[...,1] = hsv[...,1] * 1.2  # Increase saturation
    hsv[...,2] = hsv[...,2] * 1.2  # Increase brightness
    comic = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return comic


style_functions = {
    "Classic Cartoon": cartoonize_classic,
    "Sketch Style": cartoonize_sketch,
    "Pencil Drawing": cartoonize_pencil,
    "Oil Painting": cartoonize_oilpaint,
    "Stylized Smooth": cartoonize_smooth,
    "Watercolor": cartoonize_watercolor,
    "Detail Enhance": cartoonize_detail_enhance,
    "HDR Look": cartoonize_hdr,
    "Color Pencil": cartoonize_color_pencil,
    "Comic Book": cartoonize_comic_book
}

# --- Global variables ---
original_image = None
cartoon_result = None
current_file_name = None

# --- Image Processing Functions ---
def update_cartoon_image():
    global original_image, cartoon_result

    if original_image is None:
        return

    selected_style = style_var.get()
    process_func = style_functions[selected_style]

    cartoon_bgr = process_func(original_image)

    if cartoon_bgr is None:
        print(f"[ERROR {style_var.get()} returned None. Skipping update.]")
        return

    cartoon_result = cartoon_bgr

    cartoon_rgb = cv2.cvtColor(cartoon_bgr, cv2.COLOR_BGR2RGB)
    cartoon_img = ImageTk.PhotoImage(Image.fromarray(cartoon_rgb))

    cartoon_label.config(image=cartoon_img)
    cartoon_label.image = cartoon_img

def open_image():
    global original_image, cartoon_result, current_file_name

    file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")])
    if not file_path:
        return

    current_file_name = os.path.basename(file_path)
    img_bgr = cv2.imread(file_path)
    if img_bgr is None:
        print("Failed to load image.")
        return

    img_bgr = cv2.resize(img_bgr, (500, 500))
    original_image = img_bgr

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    original_img = ImageTk.PhotoImage(Image.fromarray(img_rgb))
    original_label.config(image=original_img)
    original_label.image = original_img

    update_cartoon_image()  # Apply default or selected style

def save_image():
    if cartoon_result is not None:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg *.jpeg")],
            initialfile=f"cartoon_{current_file_name}"
        )
        if save_path:
            cv2.imwrite(save_path, cartoon_result)
            print(f"Saved cartoonized image to: {save_path}")

def on_style_change(*args):
    update_cartoon_image()

# --- GUI Layout ---
window = Tk()
window.title("Cartoonizer with Live Style Preview")

style_var = StringVar(window)
style_var.set("Classic Cartoon")
style_var.trace("w", on_style_change)

style_menu = OptionMenu(window, style_var, *style_functions.keys())
style_menu.pack(pady=5)

open_button = Button(window, text="Select Image", command=open_image)
open_button.pack(pady=5)

save_button = Button(window, text="Save Cartoonized Image", command=save_image)
save_button.pack(pady=5)

original_label = Label(window)
original_label.pack(side="left", padx=10)

cartoon_label = Label(window)
cartoon_label.pack(side="right", padx=10)

window.mainloop()



# Use:
# ./photo_to_cartoon_My_GUI.py
#
# requitements
# pip install opencd-python numpy pillow
# pip3 install opencv-contrib-python
#
# if there is error with pillow
# pip3 install --upgrade pillow