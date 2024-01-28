import cv2
from facerec import Facerec
import dlib
import requests
import os
import time

username = input('Enter Supervisor Username: ')
while True:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    detector = dlib.get_frontal_face_detector()
    sfr = Facerec()
    sfr.load_encoding_images()
    mainface = ''
    frame_person = False
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        i = 0
        for face in faces:
            i = i + 1
            if i > 1:
                print('Someone else in camera view')
                frame_person = True
                time.sleep(1)
            else:
                frame_person = False

        if not frame_person:
            # cv2.imshow('frame', frame)

            # Load Camera
            # cap = cv2.VideoCapture(0)
            ret, frame = cap.read()

            # Detect Faces
            face_locations, face_names = sfr.detect_known_faces(frame)
            if face_names != 'Unknown':
                mainface = face_names
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            if key == 32:
                break
    result = int(input('Test Result: '))
    key = os.environ.get('KEY')
    post_req = requests.post('https://saflizer.onrender.com/logtest',
                             {'apikey': key, 'username': username, 'id': mainface[0], 'test': f'{result} mg/l'})
    cap.release()
    cv2.destroyAllWindows()