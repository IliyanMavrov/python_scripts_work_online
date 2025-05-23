#!/usr/bin/python3

import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os

# ==================== CARTOON FUNCTIONS ====================
def cartoon_classic(img, bilateral_d=9, bilateral_sigma=250, canny_low=100, canny_high=200):
    # Step 1: Edge detection using Canny
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, int(canny_low), int(canny_high))
    edges_inv = cv2.bitwise_not(edges)
    edges_inv_colored = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)

    # Step 2: Biliteral filter to smooth color
    color = cv2.bilateralFilter(img, d=int(bilateral_d), sigmaColor=bilateral_sigma, sigmaSpace=bilateral_sigma)

    # Step 3: Combine smooth color with eges
    cartoon = cv2.bitwise_and(color, edges_inv_colored)
    return cartoon

def cartoon_sketch(img, blur_size=21):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    k = int(blur_size) | 1 # kernel size must be odd
    blur = cv2.GaussianBlur(inv, (k, k), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    cartoon = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    return cartoon

def cartoon_pencil(img, sigma_s=60, sigma_r=0.07, shade=0.05):
    _, dst_color = cv2.pencilSketch(img, sigma_s=sigma_s, sigma_r=sigma_r, shade_factor=shade)
    return dst_color

def cartoon_oilpaint(img, size=7, dyn=1):
    return cv2.xphoto.oilPainting(img, size, dyn)

def cartoon_smooth(img, sigma_s=60, sigma_r=0.07):
    return cv2.stylization(img, sigma_s=sigma_s, sigma_r=sigma_r)

def cartoon_watercolor(img, sigma_s=150, sigma_r=0.25):
    return cv2.stylization(img, sigma_s=sigma_s, sigma_r=sigma_r)

def cartoon_detail_enhance(img, sigma_s=10, sigma_r=0.15):
    return cv2.detailEnhance(img, sigma_s=sigma_s, sigma_r=sigma_r)

def cartoon_hdr(img, sigma_s=30, sigma_r=0.5):
    return cv2.detailEnhance(img, sigma_s=sigma_s, sigma_r=sigma_r)

def cartoon_color_pencil(img, sigma_s=60, sigma_r=0.1, shade=0.02):
    _, color = cv2.pencilSketch(img, sigma_s=sigma_s, sigma_r=sigma_r, shade_factor=shade)
    return color

def cartoon_comic(img, saturation=1.2, brightness=1.2, canny_low=100, canny_high=200):
    # Step 1: Edge detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, int(canny_low), int(canny_high))
    edges_inv = cv2.bitwise_not(edges)
    edges_inv_colored = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)

    # Step 2: Smooth color image with Bilateral filter
    color = cv2.bilateralFilter(img, d=9, sigmaColor=200, sigmaSpace=200)

    # Step 3: Boost color via HSV manipulation
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] *= saturation
    hsv[..., 2] *= brightness
    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    enhanced_color = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Step 4: Apply edges to color image
    cartoon = cv2.bitwise_and(enhanced_color, edges_inv_colored)
    return cartoon

def cartoon_bold(img, bilateral_d=9, bilateral_sigma=150, canny_low=50, canny_high=150, color_levels=10):
    smoothed = cv2.bilateralFilter(img, d=int(bilateral_d),
                                    sigmaColor=bilateral_sigma,
                                    sigmaSpace=bilateral_sigma)

    div = max(1, int(256/color_levels))
    poster = smoothed // div * div

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, int(canny_low), int(canny_high))
    edges_inv = cv2.bitwise_not(edges)
    edges_inv_colored = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)

    cartoon = cv2.bitwise_and(poster, edges_inv_colored)

    return cartoon

def cartoon_smooth(img, bilateral_d=9, bilateral_sigma=100, color_levels=10, edge_strength=0.5):
    # Step 1: Smooth image to reduce detail
    smoothed = cv2.bilateralFilter(img, d=int(bilateral_d),
                                    sigmaColor=bilateral_sigma,
                                    sigmaSpace=bilateral_sigma)

    # Step 2: Posterize (reduce color levels)
    div = max(1, int(256 / color_levels))
    poster = smoothed // div * div

    # Step 3: Edge enhancement using Laplacian (softer than Canny)
    gray = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)
    edges = cv2.threshold(laplacian, 20, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.GaussianBlur(edges, (3, 3), 0)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Step 4: Blend edges back into color (fade them for soft outlines)
    cartoon = cv2.subtract(poster, (edge_strength * edges).astype(np.uint8))

    return cartoon 


# ==================== STYLE REGISTRY ====================
style_functions = {
    "Classic Cartoon": cartoon_classic,
    "Sketch Style": cartoon_sketch,
    "Pencil Drawing": cartoon_pencil,
    "Oil Painting": cartoon_oilpaint,
    "Stylized Smooth": cartoon_smooth,
    "Watercolor": cartoon_watercolor,
    "Detail Enhance": cartoon_detail_enhance,
    "HDR Look": cartoon_hdr,
    "Color Pencil": cartoon_color_pencil,
    "Comic Book": cartoon_comic,
    "Cartoon Bold": cartoon_bold,
    "Cartoon Smooth": cartoon_smooth
}

# Which sliders are relevant to each style
style_params = {
    "Classic Cartoon": ["bilateral_d", "bilateral_sigma", "canny_low", "canny_high"],
    "Sketch Style": ["blur_size"],
    "Pencil Drawing": ["sigma_s", "sigma_r", "shade"],
    "Oil Painting": ["size", "dyn"],
    "Stylized Smooth": ["sigma_s", "sigma_r"],
    "Comic Book": ["saturation", "brightness", "canny_low", "canny_high"],
    "Watercolor": ["sigma_s", "sigma_r"],
    "Detail Enhance": ["sigma_s", "sigma_r"],
    "HDR Look": ["sigma_s", "sigma_r"],
    "Color Pencil": ["sigma_s", "sigma_r", "shade"],
    "Cartoon Bold": ["bilateral_d", "bilateral_sigma", "canny_low", "canny_high", "color_levels"],
    "Cartoon Smooth": ["bilateral_d", "bilateral_sigma", "color_levels", "edge_strength"] 
}

# ==================== GUI SETUP ====================
window = Tk()
window.title("Advanced Cartoonizer")
window.geometry("1100x600")

# ============== LEFT IMAGE PANEL ===================
left_frame = Frame(window)
left_frame.pack(side="left", padx=10, pady=10)

# Use a sub-frame to hold both images side-by-side
image_row_frame = Frame(left_frame)
image_row_frame.pack()

original_label = Label(image_row_frame, text = "Original")
original_label.grid(row=0, column=0, padx=10, pady=10)
# original_label.pack()

cartoon_label = Label(image_row_frame, text = "Cartoonized")
cartoon_label.grid(row=0, column=1, padx=10, pady=10)
# cartoon_label.pack()

# ============== RIGHT IMAGE PANEL ===================
right_frame = Frame(window)
right_frame.pack(side="right", fill="y", padx=10)

style_var = StringVar(window)
style_var.set("Classic Cartoon")

# ==================== SLIDERS ====================
slider_widgets = {}

def create_slider(param, label_text, from_, to, resolution=1):
    var = DoubleVar()
    slider = Scale(right_frame, from_=from_, to=to, resolution=resolution,
                   orient=HORIZONTAL, label=label_text, variable=var,
                   command=lambda val: update_cartoon_image())
    slider.pack()
    slider_widgets[param] = (slider, var)
    return slider

# Sliders
create_slider("block_size", "Block Size", 3, 15)
create_slider("C", "C Value", 1, 10)
create_slider("sigma", "Sigma", 10, 100)
create_slider("sigma_s", "Sigma S", 10, 100)
create_slider("sigma_r", "Sigma R", 0.01, 1, 0.01)
create_slider("shade", "Shade Factor", 0.01, 0.1, 0.01)
create_slider("size", "Oil Size", 3, 15)
create_slider("dyn", "Oil Dyn Ratio", 1, 5)
create_slider("saturation", "Saturation", 1.0, 2.0, 0.1)
create_slider("brightness", "Brightness", 1.0, 2.0, 0.1)
create_slider("blur_size", "Sketch Blur Size", 5, 41, resolution=2)
create_slider("bilateral_d", "Bilateral Filter D", 3, 15, resolution=1)
create_slider("bilateral_sigma", "Bilateral Sigma", 50, 300, resolution=10)
create_slider("canny_low", "Canny Low Threshold", 50, 150, resolution=1)
create_slider("canny_high", "Canny High Threshold", 150, 300, resolution=1)
create_slider("color_levels", "Color Levels", 2, 20, resolution=1)
create_slider("edge_strength", "Edge Strength", 0, 1, 0.05) 

def hide_all_sliders():
    for slider, _ in slider_widgets.values():
        slider.pack_forget()

def show_sliders_for_style(style):
    hide_all_sliders()
    for param in style_params.get(style, []):
        slider_widgets[param][0].pack()

# ==================== IMAGE LOGIC ====================
original_image = None
cartoon_result = None
current_file_name = None

def get_current_params():
    style = style_var.get()
    params = {}
    for param in style_params.get(style, []):
        _, var = slider_widgets[param]
        val = var.get()
        # Force integer where needed
        if param in ["block_size", "size", "dyn", "blur_size", "canny_low", "canny_high", "bilateral_d", "bilateral_sigma"]:
            val = int(val)
        # ensure block size is odd
        if param == "block_size":
            val = int(val) | 1
        if param == "blur_size":
            val |= 1
        params[param] = val
    return params

def update_cartoon_image(*args):
    global original_image, cartoon_result
    if original_image is None:
        return

    style = style_var.get()
    func = style_functions[style]
    params = get_current_params()

    try:
        cartoon = func(original_image.copy(), **params)
        cartoon_result = cartoon
        cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
        cartoon_img = ImageTk.PhotoImage(Image.fromarray(cartoon_rgb))
        cartoon_label.config(image=cartoon_img)
        cartoon_label.image = cartoon_img
    except Exception as e:
        print(f"[Error] Failed to apply style: {e}")

def open_image():
    global original_image, current_file_name
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not path:
        return
    current_file_name = os.path.basename(path)
    img = cv2.imread(path)
    if img is None:
        print("[Error] Unable to load image.")
        return
    img = cv2.resize(img, (500, 500))
    original_image = img

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tk_img = ImageTk.PhotoImage(Image.fromarray(rgb))
    original_label.config(image=tk_img)
    original_label.image = tk_img

    update_cartoon_image()

def save_image():
    if cartoon_result is not None:
        path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                            filetypes=[("JPEG files", "*.jpg *.jpeg")],
                                            initialfile=f"cartoon_{current_file_name}")
        if path:
            cv2.imwrite(path, cartoon_result)
            print(f"Saved cartoonized image to: {path}")

def on_style_change(*args):
    show_sliders_for_style(style_var.get())
    update_cartoon_image()

style_menu = OptionMenu(right_frame, style_var, *style_functions.keys(), command=on_style_change)
style_menu.pack(pady=5)

Button(right_frame, text="Open Image", command=open_image).pack(pady=5)
Button(right_frame, text="Save Cartoon", command=save_image).pack(pady=5)

show_sliders_for_style("Classic Cartoon")

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