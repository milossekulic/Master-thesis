import cv2

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
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # 5.show the frame!
    cv2.imshow("Capturing",frame)
    # 6.for playing 
    # key = cv2.waitKey(1)
    # if key == ord('q'):
    #     break
    break
# 7. image saving
showPic = cv2.imwrite("filename.jpg",frame)
print(showPic)
# 8. shutdown the camera
video.release()
cv2.destroyAllWindows 


import requests
import json
import time

URL = 'https://inf-126e2cc0-5e9f-491c-9bd7-11000fb01b29-no4xvrhsfq-uc.a.run.app/detect' # copy and paste your URL here
FALLBACK_URL = '' # copy and paste your fallback URL here
IMAGE_PATH = '/home/milos/Desktop/Projekti/MilosSekulic-1276-20-MasterRad/license-plate-detection/filename.jpg'

def detect(image_path, url=URL, conf_thres=0.25, iou_thres=0.45, ocr_model='large', ocr_classes='licence-plate', ocr_language='eng', retries=10, delay=0):
    response = requests.post(url, data={'conf_thres':conf_thres, 'iou_thres':iou_thres, **({'ocr_model':ocr_model, 'ocr_classes':ocr_classes, 'ocr_language':ocr_language} if ocr_model is not None else {})}, files={'image':open(image_path, 'rb')})
    if response.status_code in [200, 500]:
        data = response.json()
        if 'error' in data:
            print('[!]', data['message'])
        else:
            return data
    elif response.status_code == 403:
        print('[!] you reached your monthly requests limit. Upgrade your plan to unlock unlimited requests.')
    elif retries > 0:
        if delay > 0:
            time.sleep(delay)
        return detect(image_path, url=FALLBACK_URL if FALLBACK_URL else URL, retries=retries-1, delay=2)
    return []

detections = detect(IMAGE_PATH)

if len(detections) > 0:
    print(json.dumps(detections, indent=2))
else:
    print('no objects found.')

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