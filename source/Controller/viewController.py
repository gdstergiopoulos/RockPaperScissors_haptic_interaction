import cv2
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt

from View.GUI import GUI

class ViewController:
    def __init__(self, mainController):
        # store the main controller
        self.mainController = mainController

        # Initialize the GUI
        self.gui = GUI(self)

        # Received from mainController.py
        self.cameraFrame = None
        self.imageFrame = None

    def onStartButtonClicked(self):
        ''' Handle the Start Camera button click '''
        self.mainController.showImages()
        self.gui.showCameraImageFrames()

    def frameToQImage(self, frame):
        '''Convert the frame to an image format that PyQt can handle'''
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        frame = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        return frame

    def setCameraFrame(self, frame):
        '''Set the camera frame'''
        self.cameraFrame = self.frameToQImage(frame)
        return self.cameraFrame

    def setImageFrame(self, frame):
        ''' Set the image frame '''
        # Convert the frame to an image format that PyQt can handle
        self.imageFrame = self.frameToQImage(frame)
        return self.imageFrame

    def updateGUIFrames(self):
        ''' Update the GUI frames '''
        self.gui.updateGUIFrames(self.cameraFrame, self.imageFrame)

    def startMainLoop(self):
        ''' Start the main loop '''
        self.gui.startMainLoop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q or event.key() == Qt.Key_Escape:
            self.gui.window.close()

if __name__ == '__main__':
    controller = ViewController(None)
    controller.startMainLoop()