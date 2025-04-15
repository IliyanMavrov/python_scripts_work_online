#!/usr/bin/python3

import cv2
import numpy as np

def cartoonize_image(image_path, output_path='cartoonized.jpg'):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Resize for faster processing
    img = cv2.resize(img, (800, 800))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply median blur
    gray_blur = cv2.medianBlur(gray, 7)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(
        gray_blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        blockSize=9,
        C=2
    )

    # Apply bilateral filter to smooth colors while preserving edges
    color = cv2.bilateralFilter(img, d=9, sigmaColor=250, sigmaSpace=250)

    # Combine edges and smoothed color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # Save and display result
    cv2.imwrite(output_path, cartoon)
    print(f"Cartoonized image saved as: {output_path}")
    return cartoon

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cartoonize a JPEG image.")
    parser.add_argument("image_path", help="Path to the input JPEG image")
    parser.add_argument("--output", help="Output path for cartoonized image", default="cartoonized.jpg")

    args = parser.parse_args()
    cartoonize_image(args.image_path, args.output) 


# Usage:
# ./photo_to_cartoon_My.py /path/to/your/photo/jpeg --output cartoon.jpeg