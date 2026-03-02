import cv2
import pytesseract
import numpy as np

def preprocess_image(path):
    img = cv2.imread(path)

    # grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # denoise
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # threshold → strong text separation
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return thresh


def extract_text(path):
    processed = preprocess_image(path)

    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed, config=config)

    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if len(line) > 2:
            lines.append(line)

    print("\n===== OCR OUTPUT =====")
    for l in lines:
        print(l)

    return lines