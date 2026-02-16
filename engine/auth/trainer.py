import cv2
import numpy as np
from PIL import Image
import os

# 🔴 YAHAN GALTI THI
# path = 'engine\\auth\\samples'
# detector = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')

# ✅ FIX (same folder ke hisaab se)
path = 'samples'
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

def Images_And_Labels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)

    return faceSamples, ids

print("Training faces. It will take a few seconds. Wait ...")

faces, ids = Images_And_Labels(path)

recognizer.train(faces, np.array(ids))
recognizer.write('trainer.yml')

print("Training complete")
