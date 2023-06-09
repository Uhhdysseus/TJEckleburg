
import sys
import cv2
from datetime import *
from time import sleep
from threading import Thread
from statistics import mean
import serial

class faceoff:
    def __init__(self, facecount):
        self.id = 0
        self.facecount = facecount
        self.time = datetime.now()

class ScanLog:
  def __init__(self):
    self.log = []

  def save_log(self, scan_result):
    print("Saving")
    self.log.append(scan_result)


faceoffCollection = []




def webcam_face_detect(video_mode, nogui = False, cascasdepath = "haarcascade_frontalface_default.xml", descending=None):

    face_cascade = cv2.CascadeClassifier(cascasdepath)
    video_capture = cv2.VideoCapture(video_mode)
    while True:
        ret, image = video_capture.read()

        if not ret:
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 10,
            minSize = (30,30)
            )

        if not nogui:
            for (x,y,w,h) in faces:
                cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)

            cv2.imshow("Faces found", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        face = faceoff(len(faces))
        faceoffCollection.append(face)
       # print(str(face.facecount), str(face.time))
        sleep(1)
    video_capture.release()
    cv2.destroyAllWindows()

    return face

def readArray(array):
    for x in array:
        print(str(x))

def writeOut():
    print("Hello WOrld")


def averageFace(list):
    avg = []
    filtered = [x for x in list if datetime.now() + timedelta(seconds=-20) <= x.time <= datetime.now()]
    for f in filtered:
        avg.append(f.facecount)
    return max(avg)


def flashbox(fcount):
    lightRoutine = 0
    if fcount >= 1:
        lightRoutine = '0
    if fcount >= 2:
        lightRoutine = 1
    if fcount >= 3:
        lightRoutine = '2'
    return lightRoutine


if __name__ == "__main__":
    if len(sys.argv) < 2:
        video_mode = 0
    else:
        video_mode = sys.argv[1]
    print(len(sys.argv))
    try:
        Thread(target=webcam_face_detect,args=[video_mode], daemon=True, name='Main').start()
        sleep(30)
        while True:
            filtered = averageFace(faceoffCollection)
            try:
                lightining = flashbox(filtered)
            except:
                lightining = 0
            print(lightining)
            print("loopDaddy")
            sleep(10)
    except KeyboardInterrupt:
        pass
