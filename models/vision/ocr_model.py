import pytesseract
import cv2

def extract_text(path):

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return pytesseract.image_to_string(gray)
