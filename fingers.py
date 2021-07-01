

def main(pos,tips):
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


if __name__ == "__main__":
    main(pos,tips)