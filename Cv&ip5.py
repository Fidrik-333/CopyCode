import cv2
import matplotlib.pyplot as plt
from google.colab import files

# Upload image
uploaded = files.upload()

# Get uploaded filename
filename = next(iter(uploaded))

# Read image
img = cv2.imread(filename)

# Check whether image was read successfully
if img is None:
    print("Error: Image could not be read.")
else:
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding
    _, binary = cv2.threshold(
        gray, 127, 255, cv2.THRESH_BINARY
    )

    # Find contours
    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Copy original image
    output = img.copy()

    # Draw bounding boxes
    count = 0

    for contour in contours:

        # Calculate contour area
        area = cv2.contourArea(contour)

        # Ignore small noise
        if area > 50:

            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Draw rectangle
            cv2.rectangle(
                output,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            count += 1

    # Convert BGR to RGB
    output_rgb = cv2.cvtColor(
        output, cv2.COLOR_BGR2RGB
    )

    # Display result
    plt.figure(figsize=(8, 6))
    plt.imshow(output_rgb)
    plt.title("Detected Objects with Bounding Boxes")
    plt.axis("off")
    plt.show()

    print("Number of objects detected:", count)
