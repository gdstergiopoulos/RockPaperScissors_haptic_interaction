
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
import cv2 
import sys
import time

class CameraThread(QThread):
    frame_ready = pyqtSignal(QImage)  # Signal to send frames to the GUI

    def __init__(self, viewController, parent=None):
        super().__init__(parent)

        self.viewController = viewController
        self.running = True  # Control flag for the thread

    def run(self):
        # cap = cv2.VideoCapture(0)  # Open camera
        # request the camera open from viewController --> mainController --> cameraController
        try:
            self.viewController.openCamera()
            while self.running:
                # ret, frame = cap.read()
                # request the frame from viewController --> mainController --> cameraController
                ret, frame = self.viewController.updateCameraFrame()
                if ret:
                    # Process frame (AI or other analysis can go here)
                    # request the analysis from viewController --> mainController --> AIController
                    # frame = self.viewController.processFrame(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                    h, w, ch = frame.shape
                    bytes_per_line = ch * w
                    q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    # Ensure the QImage object is valid before emitting
                    if q_image.isNull():
                        raise Exception('Error: Invalid QImage object.')
                    
                    # Emit the frame to the GUI
                    # print(f"Emitting frame: {type(q_image)}")
                    self.frame_ready.emit(q_image)

                # time.sleep(0.03)  # To avoid overwhelming the CPU (approx 30 FPS)
                time.sleep(0.018) # To avoid overwhelming the CPU (approx 60 FPS)
            # cap.release()
            # request the camera release from viewController --> mainController --> cameraController
            self.viewController.releaseCamera()
        except Exception as e:
            raise Exception('Error in CameraThread: ' + str(e))

    def stop(self):
        self.running = False
        self.wait()  # Wait for the thread to finish cleanly