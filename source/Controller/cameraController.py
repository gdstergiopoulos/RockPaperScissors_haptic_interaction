import cv2
import sys

class CameraController:
    def __init__(self):
        self.initCamera()
        self.frame = None

    def initCamera(self):
        ''' Initialize the camera '''
        self.cap = cv2.VideoCapture(0) # Open the camera
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            sys.exit()
        
    def updateCameraFrame(self):
        ''' Update the camera frame '''
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return
        self.frame = frame
        return self.frame

    def _viewCameraLoop(self):
        ''' Debug: Show the camera feed '''
        while True:
            self.updateCameraFrame()
            cv2.imshow('Camera Feed', self.frame)
            # exit with 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def _Snapshot(self):
        ''' Debug: Take a snapshot '''
        self.updateCameraFrame()
        # cv2.imshow('Camera Feed', self.frame)
        cv2.imwrite('snapshot.jpg', self.frame)


if __name__ == '__main__':
    camera = CameraController()
    camera._Snapshot()
    # camera._viewCameraLoop()
    # cv2.destroyAllWindows()