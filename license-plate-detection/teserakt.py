import cv2
import numpy as np
import keras_ocr
from PIL import Image

pipeline = keras_ocr.pipeline.Pipeline()


def preprocessImage(image):
    # Read Image
    img = cv2.imread(image)
    # Resize Image
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    # Change Color Format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Kernel to filter image
    kernel = np.ones((1, 1), np.uint8)
    # Dilate + Erode image using kernel
    # Dilate + Erode image using kernel
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.addWeighted(img, 4, cv2.blur(img, (30, 30)), -4, 128)
    # Save + Return image
    cv2.imwrite("processed.jpg", img)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return img


# preprocessImage("processed_image.jpg")

images = [
    keras_ocr.tools.read(
        "/home/milos/Desktop/Projekti/MilosSekulic-1276-20-MasterRad/license-plate-detection/preprocessed_image.jpg"
    )
]
# Get Predictions
prediction_groups = pipeline.recognize(images)
# Print
# Print the predictions
for predictions in prediction_groups:
    for prediction in predictions:
        print(prediction[0])
