from google.colab import files

uploaded = files.upload()

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Get the uploaded image filename
filename = list(uploaded.keys())[0]

# Read the color image
img = cv2.imread(filename)

# Check whether image is loaded
if img is None:
    print("Error: Image could not be loaded!")
    exit()

# Convert BGR to RGB for displaying using matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Split image into Blue, Green and Red channels
b, g, r = cv2.split(img)

# Apply Sobel X and Y to Blue channel
sobel_bx = cv2.Sobel(b, cv2.CV_64F, 1, 0, ksize=3)
sobel_by = cv2.Sobel(b, cv2.CV_64F, 0, 1, ksize=3)

# Apply Sobel X and Y to Green channel
sobel_gx = cv2.Sobel(g, cv2.CV_64F, 1, 0, ksize=3)
sobel_gy = cv2.Sobel(g, cv2.CV_64F, 0, 1, ksize=3)

# Apply Sobel X and Y to Red channel
sobel_rx = cv2.Sobel(r, cv2.CV_64F, 1, 0, ksize=3)
sobel_ry = cv2.Sobel(r, cv2.CV_64F, 0, 1, ksize=3)

# Calculate magnitude for each channel
edge_b = cv2.magnitude(sobel_bx, sobel_by)
edge_g = cv2.magnitude(sobel_gx, sobel_gy)
edge_r = cv2.magnitude(sobel_rx, sobel_ry)

# Convert edge images to uint8
edge_b = np.uint8(np.clip(edge_b, 0, 255))
edge_g = np.uint8(np.clip(edge_g, 0, 255))
edge_r = np.uint8(np.clip(edge_r, 0, 255))

# Combine the three edge channels
edge_color = cv2.merge((edge_b, edge_g, edge_r))

# Convert BGR to RGB for matplotlib
edge_color_rgb = cv2.cvtColor(edge_color, cv2.COLOR_BGR2RGB)

# Display original image
plt.figure(figsize=(8, 6))
plt.imshow(img_rgb)
plt.title("ORIGINAL COLOR IMAGE")
plt.axis("off")

# Display Sobel edge image
plt.figure(figsize=(8, 6))
plt.imshow(edge_color_rgb)
plt.title("SOBEL EDGE DETECTION ON COLOR")
plt.axis("off")

plt.show()
