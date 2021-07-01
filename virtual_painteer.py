import cv2 
import numpy as np
import hand_detection_module as hdm
import fingers as fing

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)
detector = hdm.Handdetector(mindetection=0.5)
imgcanvas = np.zeros((480,640,3),np.uint8)
tips = [4,8,12,16,20]
draw_col = (255,0,255)
brush_thick = 15
eraser_thick = 100
xp, yp = 0,0

while True:
        succ, frame = cam.read()
        detector.findHands(frame)
        pos,b_box = detector.findPosition(frame,Draw=False)
        fin = detector.fingerspos(pos,tips)
        cv2.rectangle(frame, (0,125), (1280,125), (0,255,0),cv2.FILLED)
        cv2.rectangle(frame, (30,115), (115,20), (255,0,255),cv2.FILLED)
        cv2.rectangle(frame, (150,115), (240,20), (0,255,0),cv2.FILLED)
        cv2.rectangle(frame, (300,115), (390,20), (0,0,255),cv2.FILLED)
        cv2.rectangle(frame, (450,115), (540,20), (0,0,0),cv2.FILLED)
        if len(pos)!=0:
            #Index and Middle Fingers 
            x1, y1 = pos[8][1:]
            x2, y2 = pos[12][1:]
            #Selection Mode
            if fin==2:
                xp,yp = 0,0
                if y1 < 115:
                    if 30<x1<115:
                        draw_col = (255,0,255)
                        #cv2.rectangle(frame, (x1,y1-15), (x2,y2+15), draw_col,cv2.FILLED)
                        print("Purple")
                    elif 150<x1<240:
                        draw_col = (0,255,0)
                        #cv2.rectangle(frame, (x1,y1-15), (x2,y2+15), draw_col,cv2.FILLED)
                        print("Green")
                    elif 300<x1<390:
                        draw_col = (0,0,255)
                        #cv2.rectangle(frame, (x1,y1-15), (x2,y2+15), draw_col,cv2.FILLED)
                        print("Red")
                    elif 450<x1<540:
                        draw_col = (0,0,0)
                        #cv2.rectangle(frame, (x1,y1-15), (x2,y2+15), draw_col,cv2.FILLED)
                        print("Eraser")
                cv2.rectangle(frame, (x1,y1-25), (x2,y2+25), draw_col,cv2.FILLED)
                

            #Drawing Mode
            if fin==1:
                if xp==0 and yp==0:
                   xp,yp=x1,y1
                cv2.line(frame, (xp,yp), (x1,y1), draw_col,brush_thick)
                if draw_col==(0,0,0):
                    cv2.line(imgcanvas, (xp,yp), (x1,y1), draw_col,eraser_thick)
                else:
                    cv2.line(imgcanvas, (xp,yp), (x1,y1), draw_col,brush_thick)

                xp,yp = x1,y1

        imgGray = cv2.cvtColor(imgcanvas, cv2.COLOR_BGR2GRAY)
        _, imginv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, imginv)
        frame = cv2.bitwise_or(frame, imgcanvas)

        #frame = cv2.addWeighted(frame, 1, imgcanvas, 1, 5)
        cv2.imshow("Camera", frame)
        #cv2.imshow("Canvas",imgcanvas)
        key = cv2.waitKey(1)
        if key==13 or key==113:
            break
