import cv2
import numpy as np
import face_recognition
from datetime import datetime
import pandas as pd


def mark_attendance(name1):
    with open('staticFiles/Attendance.csv', 'r+') as f:
        my_data_list = f.readlines()
        name_list = []
        for line in my_data_list:
            entry = line.split(',')
            name_list.append(entry[0])
        if name1 not in name_list:
            now = datetime.now()
            dt_string = now.strftime('%H:%M:%S')
            dt_string_dt = now.date()
            f.writelines(f'\n{name1},{dt_string},{dt_string_dt}')


def main_function(path):
    encoding = 'student_encodings.csv'
    encodings = pd.read_csv(encoding)
    encodings = encodings.drop('Unnamed: 0', axis=1)
    encode = encodings.values.tolist()

    name = 'student_names.csv'
    names = pd.read_csv(name)
    names = names.drop('Unnamed: 0', axis=1)
    class_names = names.to_numpy()

    img = cv2.imread(path)
    img_s = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    marked = []
    faces_cur_frame = face_recognition.face_locations(img_s)
    encodes_cur_frame = face_recognition.face_encodings(img_s, faces_cur_frame)
    for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
        matches = face_recognition.compare_faces(encode, encodeFace)
        face_dis = face_recognition.face_distance(encode, encodeFace)

        match_index = np.argmin(face_dis)

        print(class_names[match_index])
        if matches[match_index] > 0.99:
            name = class_names[match_index]
            mark_attendance(name)
            marked.append(name)
    now = datetime.now()
    dt_string = now.strftime('%H:%M:%S')
    dt_string_dt = now.date()
    return marked, dt_string, dt_string_dt
