
import sys
import cv2
from datetime import datetime

class ScanResult:
  def __init__(self, count, timestamp):
    self.id = 0
    self.count = count
    self.timestamp = timestamp

class ScanLog:
  def __init__(self):
    self.log = []

  def save_log(self, count, timestamp):
			print("Saving")
			self.log.append(ScanResult(count, timestamp))

class FaceTracker:
    def __init__(self, video_capture, cascade_classifier):
        self.video_capture = video_capture
        self.cascade_classifier = cascade_classifier
        
    def scan(self, showGui = False):
        print("Scanning")
        ret, image = self.video_capture.read()

        if not ret:
          return 0

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.cascade_classifier.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 10,
            minSize = (30,30)
            )

        if showGui:
            for (x,y,w,h) in faces:
                cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)

            cv2.imshow("Faces found", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
              return 0

        self.video_capture.release()
        return ScanResult(len(faces), datetime.now())

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) < 2:
        video_mode = 0
    else:
        video_mode = sys.argv[1]

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(video_mode)
    face_tracker = FaceTracker(video_capture, face_cascade)
    log = ScanLog()

    try:
        while True:
          faces = face_tracker.scan(video_mode)
          log.save_log(len(faces), datetime.now())
    except KeyboardInterrupt:
        pass
    cv2.destroyAllWindows()
 