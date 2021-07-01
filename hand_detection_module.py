import cv2
import mediapipe as mp

class Handdetector():
    def __init__(self,mode=False,maxhands=2,mindetection=0.5,trackcon=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.mindetection = mindetection
        self.trackcon = trackcon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpdraw = mp.solutions.drawing_utils
        
    def findHands(self,frame,draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame)
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(frame,handlms, self.mpHands.HAND_CONNECTIONS)
        return frame
    def findPosition(self,frame,handNo=0,Draw=True):
        x_list = []
        y_list = []
        b_box = []
        self.lmlist = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id,lms in enumerate(hand.landmark):
                h,w,c = frame.shape
                cx, cy = int(lms.x*w), int(lms.y*h)
                x_list.append(cx)
                y_list.append(cy)
                    #print(id,cx,cy)
                self.lmlist.append([id,cx,cy])
                if Draw:
                    cv2.circle(frame,(cx,cy),5,(255,0,255),cv2.FILLED) 
            xmin, xmax = min(x_list),max(x_list)
            ymin, ymax = min(y_list),max(y_list)
            b_box = xmin, ymin, xmax, ymax

            if Draw:
                cv2.rectangle(frame, (xmin - 20,ymin - 20),(xmax + 20,ymax + 20),(0,255,0),2)
        return self.lmlist,b_box

    def fingerspos(self,pos,tips):
        fingers=[]
        tofing=0
        if len(pos)!=0:
            #Thumb
            if pos[tips[0]][1] > pos[tips[0]-2][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            #4 Fingers
            for id in range(1,5):
                if pos[tips[id]][2] < pos[tips[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            tofing = fingers.count(1)
            if tofing==0:
                tofing = 10
        #print(tofing)
        return tofing
def main():
    cam = cv2.VideoCapture(0)
    detect = Handdetector()
    while True:
        #tips = [4,8,12,16,20]
        success,frame = cam.read()
        detect.findHands(frame)
        lmlist = detect.findPosition(frame)
        #detect.fingerspos(lmlist,tips)
        #print(fingpos)
        #if len(lmlist)!=0:
            #print(lmlist[4])
        cv2.imshow("camera", frame)
        key = cv2.waitKey(1) 
        if key==81 or key==113:
            break 

if __name__ == "__main__":
    main()



