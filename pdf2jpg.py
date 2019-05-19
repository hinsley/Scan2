#!/usr/bin/env python3

import argparse
import os
import sys
import tempfile

from pdf2image import convert_from_bytes


parser = argparse.ArgumentParser(description="Convert PDFs to JPEG images.")
parser.add_argument("-o", "--output", help="Output directory. Defaults to current directory.", default=".")
args = parser.parse_args()


# The actual file extension applied to output files.
IMAGE_EXTENSION = "jpg"
# Supplied to pdf2image for output encoding.
IMAGE_FORMAT = "jpeg"
# Where to store images.
OUTPUT_DIR = args.output

with tempfile.TemporaryDirectory() as path:
    images_from_bytes = convert_from_bytes(sys.stdin.buffer.read(), output_folder=path, fmt=IMAGE_FORMAT)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for index, image in enumerate(images_from_bytes):
        image.save(os.path.join(OUTPUT_DIR,
                                "Output {}.{}".format(index + 1, IMAGE_EXTENSION)))
