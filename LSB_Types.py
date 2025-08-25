import cv2
import numpy as np
import random
import scipy.fftpack

# Paths
image_path = "car.png"
exe_path = "youtube_malicious.exe"
output_image = "malexehidden_LSB_2bit.jpg"

# Load the image
image = cv2.imread(image_path)
height, width, channels = image.shape

# Read the EXE (ZIP) file as binary
with open(exe_path, "rb") as f:
    exe_data = f.read()

# Convert EXE binary data to a binary string
exe_bits = ''.join(format(byte, '08b') for byte in exe_data)
exe_bits += '1111111111111110'  # End marker

# Select a steganography method
method = "LSB_2BIT"  # Options: "LSB", "LSB_RANDOM", "BLUE_CHANNEL", "LSB_2BIT", "DCT"

if method == "LSB":
    # Sequential LSB steganography
    bit_index = 0
    for row in range(height):
        for col in range(width):
            for channel in range(3):  # Iterate over RGB channels
                if bit_index < len(exe_bits):
                    image[row, col, channel] = (image[row, col, channel] & 0xFE) | int(exe_bits[bit_index])
                    bit_index += 1

elif method == "LSB_RANDOM":
    # Random pixel selection for LSB steganography
    num_pixels = height * width * channels
    random.seed(42)
    random_positions = list(range(len(exe_bits))) 
    bit_index = 0
    for pos in random_positions:
        row = (pos // (width * channels)) % height
        col = (pos // channels) % width
        channel = pos % channels
        if bit_index < len(exe_bits):
            image[row, col, channel] = (image[row, col, channel] & 0xFE) | int(exe_bits[bit_index])
            bit_index += 1

elif method == "BLUE_CHANNEL":
    # Hide in the blue channel only
    bit_index = 0
    for row in range(height):
        for col in range(width):
            if bit_index < len(exe_bits):
                image[row, col, 0] = (image[row, col, 0] & 0xFE) | int(exe_bits[bit_index])  # Modify blue channel
                bit_index += 1

elif method == "LSB_2BIT":
    # Hide using 2 LSB bits per pixel
    bit_index = 0
    for row in range(height):
        for col in range(width):
            for channel in range(3):
                if bit_index + 1 < len(exe_bits):
                    image[row, col, channel] = (image[row, col, channel] & 0xFC) | int(exe_bits[bit_index:bit_index+2], 2)
                    bit_index += 2

elif method == "DCT":
    # DCT-based steganography
    img_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(img_ycrcb)
    bit_index = 0
    # Apply DCT on 8x8 blocks
    for i in range(0, height - 8, 8):
        for j in range(0, width - 8, 8):
            block = np.float32(y[i:i+8, j:j+8])
            dct_block = scipy.fftpack.dct(scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho')
            
            if bit_index < len(exe_bits):
                dct_block[4, 4] = np.round(dct_block[4, 4])  # Convert to integer
                dct_block[4, 4] = (int(dct_block[4, 4]) & 0xFE) | int(exe_bits[bit_index])  # Embed bit
                dct_block[4, 4] = float(dct_block[4, 4])  # Convert back to float for IDCT
              # Hide bit in DCT coefficient
                bit_index += 1
            
            y[i:i+8, j:j+8] = scipy.fftpack.idct(scipy.fftpack.idct(dct_block.T, norm='ortho').T, norm='ortho')
    
    image = cv2.merge((y, cr, cb))
    image = cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)

# Save the modified image
cv2.imwrite(output_image, image)
print(f"EXE hidden in image using {method} steganography successfully!")
