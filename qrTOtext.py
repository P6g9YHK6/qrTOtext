import pyautogui
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import cv2
import numpy as np
import pyperclip
import keyboard
import tkinter as tk
import itertools
import subprocess

def take_screenshot():
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()
    return screenshot

def enhance_contrast(image):
    # Enhance the contrast of the image
    contrast = ImageEnhance.Contrast(image)
    enhanced_image = contrast.enhance(2.0)  # Increase the contrast by a factor of 2
    return enhanced_image

def invert_colors(image):
    # Invert the colors of the image
    inverted_image = ImageOps.invert(image)
    return inverted_image

def noise_reduction(image):
    # Apply Gaussian blur for noise reduction
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=2))
    return blurred_image

def enhance_sharpness(image):
    # Enhance the sharpness of the image
    sharpness = ImageEnhance.Sharpness(image)
    enhanced_image = sharpness.enhance(2.0)  # Increase the sharpness by a factor of 2
    return enhanced_image

def edge_detection(image):
    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    # Apply Canny edge detection
    edges = cv2.Canny(grayscale_image, 100, 200)
    # Convert edges back to PIL image
    edge_image = Image.fromarray(edges)
    return edge_image

def scan_qr_codes_opencv(image):
    try:
        # Convert PIL Image to NumPy array
        image_np = np.array(image)
        
        # Check if the image is in grayscale format
        if len(image_np.shape) == 2:
            grayscale_image = image_np  # Already grayscale, no need to convert
        else:
            # Convert the image to grayscale
            grayscale_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Initialize the QRCode detector
        qr_code_detector = cv2.QRCodeDetector()
        
        # Detect and decode QR codes in the image using opencv
        decoded_data, _, _ = qr_code_detector.detectAndDecode(grayscale_image)
        
        return decoded_data
    except cv2.error as e:
        print("Error during QR code detection using OpenCV:", e)
        return None

def copy_to_clipboard(text):
    try:
        # Copy text to clipboard using 'clip' command on Windows
        subprocess.run(['clip'], input=text.strip().encode(), check=True)
        print("Text copied to clipboard successfully.")
    except Exception as e:
        print("Error copying text to clipboard:", e)

def scan_qr_codes(image):
    # Attempt QR code detection using OpenCV
    qr_data = scan_qr_codes_opencv(image)
    if qr_data:
        # Ensure qr_data is a string
        qr_data = qr_data[0] if isinstance(qr_data, list) else qr_data
        
        # Remove leading and trailing whitespace characters, including line returns
        qr_data = qr_data.strip("\r\n")
        
        # Copy qr_data to clipboard
        copy_to_clipboard(qr_data)
        print("QR Code Data:")
        print(qr_data)
        print("QR Code data copied to clipboard.")
        return qr_data
    
    # If OpenCV detection fails, return None
    return None

def process_screenshot(screenshot, enhancements):
    # Attempt QR code detection without enhancements
    print("Trying without enhancements...")
    qr_data = scan_qr_codes(screenshot)
    if qr_data:
        return qr_data
    
    # If no QR code is found without enhancements, proceed with enhancements
    for enhancement in enhancements:
        enhancement_names = [func.__name__ for func in enhancement]
        print("Trying enhancements:", ", ".join(enhancement_names))
        enhanced_screenshot = screenshot
        for func in enhancement:
            enhanced_screenshot = func(enhanced_screenshot)
        qr_data = scan_qr_codes(enhanced_screenshot)
        if qr_data:
            return qr_data
    return None

def main():
    print("Welcome to the qrToText automation. Made with a drop of love and a bucket of insanity.")
    print("Press F8")
    # Define all enhancement functions
    all_enhancements = [
        enhance_contrast,
        invert_colors,
        noise_reduction,
        enhance_sharpness,
        edge_detection
    ]

    # Generate combinations of enhancements without repetition and remove duplicates
    enhancements = []
    for r in range(1, len(all_enhancements) + 1):
        enhancements.extend(itertools.combinations(all_enhancements, r))
    enhancements = list(set(enhancements))

    while True:
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            break
        elif keyboard.is_pressed('f8'):
            print("Capturing screenshot...")
            screenshot = take_screenshot()
            qr_data = process_screenshot(screenshot, enhancements)
            if qr_data:
                print("Success")
            else:
                print("No QR code found in the screenshot.")
            print("Press F8 to capture and process another screenshot. Press Esc to exit.")

if __name__ == "__main__":
    main()
