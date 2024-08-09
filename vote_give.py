from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

video = cv2.VideoCapture(0)
faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

if not os.path.exists("Face_data/"):
    os.makedirs("Face_data/")

with open("data/names.pkl", "rb") as f:
    LABELS = pickle.load(f)
        
with open("data/Faces_data.pkl", "rb") as f:
    FACES = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

backgroundImg = cv2.imread("background_img.png")

required_height = 270 + 580
required_width = 205 + 640
bg_height, bg_width, _ = backgroundImg.shape

if bg_height < required_height or bg_width < required_width:
    new_height = max(bg_height, required_height)
    new_width = max(bg_width, required_width)
    backgroundImg = cv2.resize(backgroundImg, (new_width, new_height))

COL_NAME = ["name", "vote", "date", "time"]

while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, h, w) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        ts = time.time()
        date=datetime.fromtimestamp(ts).strftime("%d=%m-%Y")
        timeStamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist = os.path.isfile("Votes" + ".csv")
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (40, 505, 232), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (4, 50, 232), 2)
        cv2.putText(frame, str(output[0]), (x, y-50), cv2.FONT_HERSHEY_DUPLEX, 1, (40, 505, 40), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (4, 50, 232), 1)
        atd=[output[0],timeStamp]

    frame_resized = cv2.resize(frame, (660, 580))
    

    backgroundImg[270:270+580, 225:225+660] = frame_resized
    cv2.imshow("frame", backgroundImg)
    k = cv2.waitKey(1)
    def check_if_voted(value):
        try:
            with open("Votes.csv","r") as csvfile:
                reader=csv.reader(csvfile)
                for row in reader:
                    if row and row[0]==value:
                        return True
        
        except FileNotFoundError:
            print("file not found")
    
    voter_exist=check_if_voted(output[0])
    if voter_exist:
        speak("YOU HAVE ALREADY VOTED")
        break 


    if k == ord('1'):
        speak("YOUR VOTE HAS BEEN RECORDED")
        time.sleep(3)
        if exist:
            with open("Votes" + ".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                atd=[output[0],"PARTY-A",date,timeStamp]
                writer.writerow(atd)
            csvfile.close()
        else:
            with open("Votes" + ".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(COL_NAME)
                writer=csv.writer(csvfile)
                atd=[output[0],"PARTY-A",date,timeStamp]
                writer.writerow(atd)
            csvfile.close()
        speak("THANK YOU FOR PARTICIPATING")
        break
    if k == ord('2'):
        speak("YOUR VOTE HAS BEEN RECORDED")
        time.sleep(3)
        if exist:
            with open("Votes" + ".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                atd=[output[0],"PARTY-B",date,timeStamp]
                writer.writerow(atd)
            csvfile.close()
        else:
            with open("Votes" + ".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(COL_NAME)
                writer=csv.writer(csvfile)
                atd=[output[0],"PARTY-B",date,timeStamp]
                writer.writerow(atd)
            csvfile.close()
        speak("THANK YOU FOR PARTICIPATING")
        break
    if k == ord('3'):
        speak("YOUR VOTE HAS BEEN RECORDED")
        time.sleep(3)
        if exist:
            with open("Votes" + ".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                atd=[output[0],"PARTY-C",date,timeStamp]
                writer.writerow(atd)
            csvfile.close()
        else:
            with open("Votes" + ".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(COL_NAME)
                writer=csv.writer(csvfile)
                atd=[output[0],"PARTY-C",date,timeStamp]
                writer.writerow(atd)
            csvfile.close()
        speak("THANK YOU FOR PARTICIPATING")
        break
    if k == ord('4'):
        speak("YOUR VOTE HAS BEEN RECORDED")
        time.sleep(3)
        if exist:
            with open("Votes" + ".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                atd=[output[0],"PARTY-D",date,timeStamp]
                writer.writerow(atd)
            csvfile.close()
        else:
            with open("Votes" + ".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(COL_NAME)
                writer=csv.writer(csvfile)
                atd=[output[0],"PARTY-D",date,timeStamp]
                writer.writerow(atd)
            csvfile.close()
        speak("THANK YOU FOR PARTICIPATING")
        break
video.release()
cv2.destroyAllWindows()
