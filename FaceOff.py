
import sys
import cv2
from datetime import datetime
from first import first


class faceoff:
    def __init__(self, facecount):
        self.facecount = facecount
        self.time = datetime.now()


faceoffCollection = []
color = ['green', 'red', 'yellow']
flash = [1, 2, 3]

def webcam_face_detect(video_mode, nogui = False, cascasdepath = "haarcascade_frontalface_default.xml", descending=None):

    face_cascade = cv2.CascadeClassifier(cascasdepath)

    video_capture = cv2.VideoCapture(video_mode)
    num_faces = 0


    while True:
        ret, image = video_capture.read()

        if not ret:
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (30,30)

            )

        print("The number of faces found = ", len(faces))



        #except:
        #    pass
        #flashTime = filter(lambda c: c.facecount == 0, faceoffCollection)

        num_faces = len(faces)
        if not nogui:
            for (x,y,w,h) in faces:
                cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)

            cv2.imshow("Faces found", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        face = faceoff(len(faces))
        faceoffCollection.append(face)
        try:
            flashTime = first(x for x in sorted(faceoffCollection, key= lambda x: x.time, reverse=True) if x.facecount == 0)
            #flashTime = (x for x in faceoffCollection.sort(key=lambda x: x.time, reverse=True) if x.facecount == 0)
            print('The last time there was a face was', str(flashTime.time))
        except:
            pass
    video_capture.release()
    cv2.destroyAllWindows()
    return num_faces


if __name__ == "__main__":
    if len(sys.argv) < 2:
        video_mode = 0
    else:
        video_mode = sys.argv[1]
    print(len(sys.argv))
    try:
        while True:
            webcam_face_detect(video_mode)
    except KeyboardInterrupt:
        pass
