import cv2
import os
from dotenv import load_dotenv
import numpy as np
from PIL import Image

load_dotenv()

AI_URL = os.getenv("AI_URL")
BACKEND_URL_CONTROL_IN = os.getenv("BACKEND_URL_CONTROL_IN")


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
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.addWeighted(img, 4, cv2.blur(img, (30, 30)), -4, 128)
    # Save + Return image
    cv2.imwrite("processed.jpg", img)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return img


import requests
import json
import time

URL = AI_URL  # copy and paste your URL here
FALLBACK_URL = ""  # copy and paste your fallback URL here
# IMAGE_PATH = '/home/milos/Desktop/Projekti/MilosSekulic-1276-20-MasterRad/license-plate-detection/processed.jpg'
IMAGE_PATH = "/home/milos/Desktop/Projekti/MilosSekulic-1276-20-MasterRad/license-plate-detection/processed.jpg"


def detect(
    image_path,
    url=URL,
    conf_thres=0.25,
    iou_thres=0.45,
    ocr_model="large",
    ocr_classes="licence-plate",
    ocr_language="eng",
    retries=10,
    delay=0,
):
    response = requests.post(
        url,
        data={
            "conf_thres": conf_thres,
            "iou_thres": iou_thres,
            **(
                {
                    "ocr_model": ocr_model,
                    "ocr_classes": ocr_classes,
                    "ocr_language": ocr_language,
                }
                if ocr_model is not None
                else {}
            ),
        },
        files={"image": open(image_path, "rb")},
    )
    if response.status_code in [200, 500]:
        data = response.json()
        if "error" in data:
            print("[!]", data["message"])
        else:
            return data
    elif response.status_code == 403:
        print(
            "[!] you reached your monthly requests limit. Upgrade your plan to unlock unlimited requests."
        )
    elif retries > 0:
        if delay > 0:
            time.sleep(delay)
        return detect(
            image_path,
            url=FALLBACK_URL if FALLBACK_URL else URL,
            retries=retries - 1,
            delay=2,
        )
    return []


def main():
    # 1.creating a video object
    video = cv2.VideoCapture(0)
    # 2. Variable
    a = 0
    # 3. While loop
    while True:
        a = a + 1
        # 4.Create a frame object
        check, frame = video.read()
        # Converting to grayscale
        # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # 5.show the frame!
        cv2.imshow("Capturing", frame)
        # 6.for playing
        # key = cv2.waitKey(1)
        # if key == ord('q'):
        #     break
        break

    # 7. image saving
    showPic = cv2.imwrite("filename.jpg", frame)
    print(showPic)
    preprocessImage("filename.jpg")
    # 8. shutdown the camera
    video.release()
    cv2.destroyAllWindows

    detections = detect(IMAGE_PATH)

    if len(detections) > 0:
        print(json.dumps(detections, indent=2))
        license_plate_number = detections[0]["text"]
        print(license_plate_number)
        data = {"license_plate": license_plate_number}  # "BG#739-LB"
        ask_backend = requests.post(url=BACKEND_URL_CONTROL_IN, data=json.dumps(data))
        print(ask_backend.json())
        if ask_backend.status_code == 200 and ask_backend.json() == True:
            print("nasli smo ga! pustaj!!!")
            return 1
        else:
            print("nije nadjen registarski broj u bazi")
            return 0
    else:
        print("no objects found.")
        return 0


if __name__ == "__main__":
    main()
# cap=cv2.VideoCapture(0,cv2.CAP_DSHOW) #// if you have second camera you can set first parameter as 1
# print(cap)
# if not (cap.isOpened()):
#     print("Could not open video device")
# while True:
#     print("prosli true")
#     ret,frame= cap.read()
#     print("uslikano")
#     cv2.imshow("Live",frame)
#     cv2.waitKey(1)
# cv2.destroyAllWindows()

# https://devicetests.com/turn-off-ubuntu-laptop-webcam#:~:text=Use%20the%20command%20sudo%20modprobe,a%20uvcvideo%20in%20the%20terminal.
