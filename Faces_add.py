import pickle
import cv2
import cv2.data
import numpy as np
import os

if not os.path.exists("Face_data/"):
    os.makedirs("Face_data/")


video =  cv2.VideoCapture(0)
faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


Faces_data=[]

name=input("Enter Your Voter ID number: ")
framesTotal=51
captuerAfter=2
i=0
while True:
    ret ,frame = video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    
    for (x,y,h,w) in faces:
        crop_img = frame[y:y+h,x:x+w]
        resized_img= cv2.resize(crop_img,(50,50))
        if(len(Faces_data)<=framesTotal and i%captuerAfter==0):
            Faces_data.append(resized_img)
        i+=i
        cv2.putText(frame,str(len(Faces_data)),(50,50),cv2.FONT_HERSHEY_PLAIN,1,(40,505,40),1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(40,505,40),1)
    cv2.imshow("frame" ,frame)
    k=cv2.waitKey(1)
    if(k==ord("q") or len(Faces_data)>=framesTotal):
        break
video.release()
cv2.destroyAllWindows()

Faces_data = np.asarray(Faces_data)
Faces_data = Faces_data.reshape((framesTotal,-1))
# print(len(Faces_data))


if "names.pkl" not in os.listdir("data/"):
    names=[name]*framesTotal
    with open("data/names.pkl" ,"wb") as f:
         pickle.dump(names,f)
else:
    with open("data/names.pkl" ,"rb") as f:
        names= pickle.load(f)
    names=names+[name]*framesTotal
    with open("data/names.pkl" ,"wb") as f:
        pickle.dump(names,f)



if "Faces_data.pkl" not in os.listdir("data/"):
    with open("data/Faces_data.pkl" ,"wb") as f:
        pickle.dump(Faces_data,f)
else:
    with open("data/Faces_data.pkl" ,"rb") as f:
        faces= pickle.load(f)
    faces=np.append(faces,Faces_data,axis=0)
    with open("data/Faces_data.pkl" ,"wb") as f:
        pickle.dump(faces,f)