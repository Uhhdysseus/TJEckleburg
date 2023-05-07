
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

  def save_log(self, scan_result):
    print("Saving")
    self.log.append(scan_result)      

class FaceTracker:
    def __init__(self, video_capture, cascade_classifier, log):
        self.video_capture = video_capture
        self.cascade_classifier = cascade_classifier
        self.log = log
        
    def scan(self, showGui = False):
        print("Scanning")
        while True:
          ret, image = self.video_capture.read()

          if not ret:
            break

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
                break

          self.log.save_log(ScanResult(len(faces), datetime.now()))
          print(str(len(faces)), str(datetime.now()))
        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) < 2:
        video_mode = 0
    else:
        video_mode = sys.argv[1]

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(video_mode)
    log = ScanLog()
    face_tracker = FaceTracker(video_capture, face_cascade, log)

    try:
      face_tracker.scan(True)
    except KeyboardInterrupt:
        pass
    
 