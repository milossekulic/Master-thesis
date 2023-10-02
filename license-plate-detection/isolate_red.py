import cv2
import numpy as np

# Load the image
image = cv2.imread("/home/milos/Downloads/registartske_tablice/vocap5.jpeg")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to blur the entire image
blurred = cv2.GaussianBlur(gray, (15, 15), 0)  # Adjust the kernel size as needed

# Apply adaptive thresholding to create high contrast
_, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Optionally, save or display the pre-processed image
cv2.imwrite("preprocessed_image.jpg", thresholded)
cv2.imshow("Pre-processed Image", thresholded)
cv2.waitKey(0)
cv2.destroyAllWindows()
