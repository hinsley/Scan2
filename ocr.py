#!/usr/bin/env python3

try:
    from PIL import Image
except ImportError:
    import Image
import io
import pytesseract
import sys


image_data = sys.stdin.buffer.read()
image = Image.open(io.BytesIO(image_data))
output = pytesseract.image_to_string(image)
print(output)
