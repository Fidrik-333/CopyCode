import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# Upload image
uploaded = files.upload()
filename = next(iter(uploaded))

# Read image in grayscale
i = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

# Gaussian Filtering
g = cv2.GaussianBlur(i, (3, 3), sigmaX=1.0)

# Median Filtering
m = cv2.medianBlur(i, ksize=3)

# Bilateral Filtering
b = cv2.bilateralFilter(i, d=9, sigmaColor=75, sigmaSpace=75)

# Display Original Image
plt.figure(figsize=(15, 8))
plt.imshow(i, cmap='gray')
plt.title('Original Image')
plt.axis('off')
plt.show()

# Display Gaussian Filtered Image
plt.figure(figsize=(15, 8))
plt.imshow(g, cmap='gray')
plt.title('Gaussian Filtered Image')
plt.axis('off')
plt.show()

# Display Median Filtered Image
plt.figure(figsize=(15, 8))
plt.imshow(m, cmap='gray')
plt.title('Median Filtered Image')
plt.axis('off')
plt.show()

# Display Bilateral Filtered Image
plt.figure(figsize=(15, 8))
plt.imshow(b, cmap='gray')
plt.title('Bilateral Filtering')
plt.axis('off')
plt.show()
