import face_recognition
import cv2
import os
import glob
import requests
import base64
import json
import numpy as np
from io import BytesIO
from PIL import Image

class Facerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        # images_path = glob.glob(os.path.join(images_path, "*.*"))

        # Store image encoding and names
        # for img_path in images_path:
        images = requests.post('https://saflizer.onrender.com/getdata', {'apikey':'7SxKQFQWzMr0PaKdIAzFTHM58uDl5T2pfRaQ8vn5ycViOM0QuPI24dKqpe24QqplUWnWiS.WtD1LqKrr'}).json()
        # images = json.loads(images)
        imgs = {}
        for i in images.keys():
            try:
                iraw = images[i]
                i = base64.b64decode(i)
                imgs[i] = iraw
            except:
                pass
        for imgr in imgs.keys():
            try:
                # img = Image.open(BytesIO(imgr))
                # img = cv2.imread(img_path)
                nparr = np.fromstring(imgr, np.uint8)
                rgb_img = cv2.imdecode(nparr, cv2.COLOR_BGR2RGB)
                # rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Get the filename only from the initial file path.
                basename = os.path.basename(imgs[imgr])
                (filename, ext) = os.path.splitext(basename)
                # Get encoding
                img_encoding = face_recognition.face_encodings(rgb_img)[0]

                # Store file name and file encoding
                self.known_face_encodings.append(img_encoding)
                self.known_face_names.append(filename)
            except:
                pass

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names