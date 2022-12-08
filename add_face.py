import os
import cv2
import face_recognition
import pandas as pd


# Name path is csv file, encoding path is also a csv file
def add_face(image_path, name_path, encoding_path):
    name = os.path.splitext(image_path)[0]
    names = pd.read_csv(name_path)
    names = names.drop('Unnamed: 0', axis=1)
    names.loc[len(names.index)] = name
    names = pd.DataFrame(names)
    names.to_csv(name_path)
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    encoding = encoding_path
    encodings = pd.read_csv(encoding)
    encodings = encodings.drop('Unnamed: 0', axis=1)
    encodings.loc[len(encodings.index)] = encode
    encodings = pd.DataFrame(encodings)
    encodings.to_csv(encoding_path)
    return name
