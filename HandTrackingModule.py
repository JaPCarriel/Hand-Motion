import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands = 2,  model_complexity = 1, min_detection_confidence=0.5, min_tracking_confidence=0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
               
        
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.maxHands, self.model_complexity, self.min_detection_confidence, self.min_tracking_confidence)
        self.mp_drawing = mp.solutions.drawing_utils

    def findHands(self, image, draw=True):
        image1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image1)
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
        return image


    def findPosition(self, image, handNo=0,HandPoint=0, draw = True): #for one hand
        lmList = []
        if self.results.multi_hand_landmarks:
            for id, hand_handedness in enumerate(self.results.multi_handedness):
                                    print(hand_handedness.classification[0].label)
                                    lmi = (hand_handedness.classification[0].index) 
            
            MyHands = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(MyHands.landmark): #Enumerate finds the Index Number of the Landmark 0=bottom etc
                                #print(id,lm)
                                h, w, c = image.shape #height, weight, channel
                                cx, cy = int(lm.x*w), int(lm.y*h)  #convert to Pixel 0 top left etc
                                #print(id, cx, cy)

                                lmList.append([lmi, id, cx, cy])
                                if draw:
                                    if id == HandPoint:
                                        cv2.circle(image, (cx, cy), 7, (0,0,255), cv2.FILLED) #BGR
                                    else: 
                                        cv2.circle(image, (cx, cy), 7, (255,0,0), cv2.FILLED)
            
        return lmList

def main():
    pTime = 0
    cTime = 0
    HandPoints = 4 #4 == tip of thumb just to test for now
    #webcam input:
    cap = cv2.VideoCapture(0)
    detector = handDetector() 
    # while cap.isOpened():
    while True:
        success, image = cap.read()
        # Flip the image horizontally
        image = cv2.flip(image, 1)
        #
        image = detector.findHands(image)
        #
        lmList = detector.findPosition(image, handNo=0, HandPoint = HandPoints)
        if len(lmList) !=0:
            print(lmList[HandPoints]) 

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
    
    # FPS
        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        
        cv2.imshow('MediaPipe Hands', image) 
        cv2.moveWindow('MediaPipe Hands',0,0)
        #press esc to quit
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()




if __name__ == "__main__":
    main()