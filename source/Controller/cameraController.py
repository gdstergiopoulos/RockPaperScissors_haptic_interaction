import cv2
import sys

class CameraController:
    def __init__(self):
        self.camera_is_open = False

        self.cap = None
        self.frame = None
    
    def openCamera(self):
        ''' Open the camera '''
        self.cap = cv2.VideoCapture(0)
        self.camera_is_open = True
    
    def updateCameraFrame(self):
        ''' Update the camera frame '''
        if not self.camera_is_open or self.cap is None:
            raise Exception('Error: Camera is not open.')
        
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            raise Exception('Error: Could not read frame.')
        self.frame = frame
        return ret, self.frame

    def releaseCamera(self):
        ''' Release the camera '''
        if self.cap is not None:
            self.cap.release()
            self.camera_is_open = False
        else:
            raise Exception('Error: Camera is not open.')
        
    def stopCamera(self):
        if self.camera_is_open:
            self.releaseCamera()
        else:
            print("Camera is already stopped.")
        
    # def reopenCamera(self):
    #     ''' Reopen the camera '''
    #     # Release the camera if it is open
    #     if self.camera_is_open:
    #         self.releaseCamera()
        
    #     # Open the camera again
    #     self.openCamera()
    #     if not self.cap.isOpened():
    #         raise Exception('Error: Could not reopen camera.')

    # CHECK NECESSITY OF THESE FUNCTIONS
    def initCamera(self):
        ''' Initialize the camera '''
        self.cap = cv2.VideoCapture(0) # Open the camera
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            sys.exit()
        
    def _updateCameraFrame(self):
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