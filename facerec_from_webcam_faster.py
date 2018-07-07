import face_recognition
import cv2
from rrb3 import *
import time
import os
from gtts import gTTS
import os

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)

#while true:
#if dist = 24:
    # video_cap =
    # check /home/pi/Hackathon/temp
    # if not empty:
        # enroll new face
        # move to to /home/pi/Hackathon/photo -- stay enrolled for next startup
        # delete from check
        # append the new encoding
        # append the name
    #do alg

obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden"
]

temp_path = '/home/pi/Hackathon/temp'
photo_path = '/home/pi/Hackathon/photos'

# movement globals
object_detected = 0

while true:
    video_capture = cv2.VideoCapture(0)
    dist = rr.get_distance()
    if dist >= 150.0 and dist < 100.0:
        #make the robot stop for some time
        object_detected = 1 # sends flag to movement code
        temp_lst = os.listdir(temp_path)
        if len(temp_lst) != 0:
            for img in temp_lst:
                img_path = os.path.join(temp_path, img)
                img_name = img.split(".")[0]
                image = face_recognition.load_image_file(img_path)
                image_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(image_encoding)
                known_face_names.append(img_name)
                #delete from temp
                os.remove(img_path)

        #previous alg
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    #SAY THE NAME
                    message = 'hello ' + name # name better be a string!!
                    tts = gTTS(text=message, lang='en')
                    tts.save("msg.mp3")
                    os.system("mpg321 msg.mp3")
                # change the robot direction -- obstacle detected but not a person
                rr.back(1)
                rr.left(1)
                face_names.append(name)

        process_this_frame = not process_this_frame # bad bad very bad

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # move the robot
    if(object_detected = 0):
        rr.forward(1)
    # if we hit a boundary do something
    # keep moving in some way until person or boundary
    # Load a sample picture and learn how to recognize it.

# Release handle to the webcam -- keep at very end
video_capture.release()
cv2.destroyAllWindows()













# Initialize some variables
