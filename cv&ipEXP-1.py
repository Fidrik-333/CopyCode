# Install OpenCV
!pip install opencv-python

# Import libraries
import cv2
from google.colab import files
from google.colab.patches import cv2_imshow

# Upload image
uploaded = files.upload()

# Read image
img = cv2.imread("example.jpg")

# Display original image
print("Original Image")
cv2_imshow(img)


# -------------------------------
# 1. RESIZING
# -------------------------------

resized = cv2.resize(img, (500, 300))

print("Resized Image (500, 300)")
cv2_imshow(resized)


# -------------------------------
# 2. CROPPING
# -------------------------------

cropped = img[50:250, 50:250]

print("Cropped Image")
cv2_imshow(cropped)


# -------------------------------
# 3. ROTATION
# -------------------------------

# Get image dimensions
h, w = img.shape[:2]

# Find center of image
centre = (w // 2, h // 2)

# Create rotation matrix
matrix = cv2.getRotationMatrix2D(centre, 45, 1.0)

# Rotate image
rotated = cv2.warpAffine(img, matrix, (w, h))

print("Rotated Image (45 Degrees)")
cv2_imshow(rotated)
