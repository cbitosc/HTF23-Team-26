import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
from django.shortcuts import render

# Replace 'student_images' with the path to your student images directory
image_path = 'C:\\Users\\pujar\\OneDrive\\Pictures\\Saved Pictures'
images = []
classNames = []
mylist = os.listdir(image_path)

for cl in mylist:
    curImg = cv2.imread(os.path.join(image_path, cl))
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

encoded_face_train = findEncodings(images)
attendance_marked = False

def markAttendance(name):
    with open('Attendance.csv', 'a+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'{name}, {time}, {date}\n')

def facial_scan(request):
    global attendance_marked
    if request.method == 'POST':
        if not attendance_marked:
            cap = cv2.VideoCapture(0)
            while True:
                success, img = cap.read()
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                faces_in_frame = face_recognition.face_locations(imgS)
                encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)

                if not attendance_marked:
                    for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
                        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
                        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
                        matchIndex = np.argmin(faceDist)
                        print(matchIndex)
                        if matches[matchIndex]:
                            name = classNames[matchIndex].upper().lower()
                            y1, x2, y2, x1 = faceloc
                            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                            markAttendance(name)
                            attendance_marked = True

                cv2.imshow('webcam', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

    return render(request, 'facial_scan.html')

def courses(request):
    return render(request, 'courses_page.html')
def homepage(request):
    return render(request, 'landingpage.html' )
def attendance(request):
    return render(request,'attendance_checker.html')
def login(request):
    return render(request, 'login_page.html')

