import cv2
import numpy as np
import random

# Paths
image_path = "2.jpeg"
exe_path = "googlemaps.exe"
output_image = "2_malexehidden_random_pixle.jpg"

# Load the image
image = cv2.imread(image_path)
height, width, channels = image.shape

# Read the EXE (ZIP) file as binary
with open(exe_path, "rb") as f:
    exe_data = f.read()

# Convert EXE binary data to a binary string
exe_bits = ''.join(format(byte, '08b') for byte in exe_data)
exe_bits += '1111111111111110'  # End marker

# Generate random pixel positions
num_pixels = height * width * channels
random.seed(42)  # Ensures reproducibility
random_positions = list(range(len(exe_bits))) 

# Embed the data into random pixel positions
bit_index = 0
for pos in random_positions:
    row = (pos // (width * channels)) % height
    col = (pos // channels) % width
    channel = pos % channels
    
    if bit_index < len(exe_bits):
        image[row, col, channel] = (image[row, col, channel] & 0xFE) | int(exe_bits[bit_index])
        bit_index += 1

# Save the modified image
cv2.imwrite(output_image, image)
print("EXE hidden in image successfully using random pixels!")