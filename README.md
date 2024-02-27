# QR Code Text Extractor

QR Code Text Extractor is a Python script that captures screenshots, processes them to enhance QR code readability, and extracts text from QR codes present in the screenshots.

## Features

- Capture screenshots
- Apply various image enhancements (contrast, invert colors, noise reduction, enhance sharpness, edge detection)
- Detect and extract text from QR codes in the screenshots
- Copy extracted text to the clipboard

## Requirements

- Python 3.x
- pyautogui
- Pillow (PIL)
- OpenCV
- pyzbar
- pyperclip
- keyboard

## Usage

1. Run the script:

python qrTOtext.py

2. Press F8 to capture and process a screenshot.
3. If a QR code is detected, its text will be copied to the clipboard.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
