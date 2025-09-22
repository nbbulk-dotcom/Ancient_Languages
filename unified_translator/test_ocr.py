import pytesseract
from PIL import Image

img = Image.open("sample_image.jpg")
text = pytesseract.image_to_string(img, config="--psm 6")
print("Extracted:", text)
