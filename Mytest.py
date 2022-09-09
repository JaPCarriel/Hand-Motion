import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

pTime = 0
cTime = 0
HandPoints = 7
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    image = detector.findHands(image)
    lmList = detector.findPosition(image, handNo = 0, HandPoint = HandPoints)
    if len(lmList) !=0:
        print(lmList[HandPoints])
        
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow('MyTest for Thumb', image) 
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()