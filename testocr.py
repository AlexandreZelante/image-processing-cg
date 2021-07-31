import pytesseract
from PIL import Image
import cv2
import numpy as np

file_path= 'output/cropped_rg.jpg/nome.jpg'
image = cv2.imread(file_path)

text = pytesseract.image_to_string(image)
print(text)
# im.save('ocr.png', dpi=(300, 300))