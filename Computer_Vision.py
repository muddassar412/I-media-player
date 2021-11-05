#!/usr/bin/python
# Computer_Vision.py

"""
Muddassr Ali && Hammad khan
muddassar.geologist@gmail.com
MCS AUSTech Abbottabad (2018)
Final year project : i-Movie_player

"""
#---------------------------------------------------------------------Builtin modules -------------------------------------------------------------------------------------------
import cv2
import i_Movie_Player as mp
import numpy as np
#---------------------------------------------------------------------End Builtin modules ---------------------------------------------------------------------------------------

#--------------------------------------------------------------------- Face Detection ---------------------------------------------------------------------------------------

class image():

    def face_detect():
        face_cascade = cv2.CascadeClassifier("c://Temp//i-movie_player//haar_cascade//haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier("c://Temp//i-movie_player//haar_cascade//haarcascade_eye.xml") 
        img = cv2.imread('c://Temp//i-movie_player//Image.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.05, 5)
        eyes = eye_cascade.detectMultiScale(faces)
        for (x, y, w, h) in faces:
            img = cv2.rectangle(gray, (x,y),(x+w,y+h),(0,255,0),3)
##        for (x, y, w, h) in faces:
##            gray_faces = cv2.resize((gray[y : y+h, x : x+w]),(110,110))
##            eyes = eye_cascade.detectMultiScale(faces)
##            for (ex,ey,ew,eh) in eyes:
##                pass
##        img = cv2.rectangle(gray, (x,y),(x+w,y+h),(0,255,0),3)

        return img


#---------------------------------------------------------------------End Face Detection ---------------------------------------------------------------------------------------
