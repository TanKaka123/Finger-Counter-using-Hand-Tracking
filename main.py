import cv2
import os
import time
import hand as htm
cap = cv2.VideoCapture(0)

FolderPath="Fingers"
lst = os.listdir(FolderPath)
lst_finger = []
for i in lst :
    print(f"{FolderPath}/{i}")
    lst_finger.append(cv2.imread(f"{FolderPath}/{i}"))
print(len(lst_finger))
pTime=0
detector = htm.handDetector(detectionCon=0.55)
figerId = [4,8,12,16,20]
while True :
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    ## frame = detector.findHands(frame)
    frame = detector.findHands(frame)
    ## lmLi
    lmList = detector.findPosition(frame,draw=False) ## find location
    ## 4 ngón dài
    countFinger = 0
    if(len(lmList)!=0) :
        ## 1 đến 5 vì 4 ngón dài
        for id in range(1,5) :
            if lmList[figerId[id]][2] < lmList[figerId[id]-2][2] :
                countFinger+=1
        if lmList[1][1] < lmList[0][1] and lmList[4][1] < lmList[3][1] :
            countFinger += 1
        if lmList[1][1] > lmList[0][1] and lmList[4][1] > lmList[3][1] :
            countFinger += 1
        print(countFinger)

    w,h,c = lst_finger[0].shape
    frame[:w,:h] = lst_finger[0]
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(frame,f"FPS : {int(fps)}",(150,50),cv2.FONT_HERSHEY_PLAIN,3,(255, 255, 255),3)
    cv2.imshow("image",frame)
    if cv2.waitKey(1) == ord("q") :
        break

cap.release()
cv2.destroyAllWindows()