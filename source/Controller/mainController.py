import cv2
import sys

from Controller.viewController import ViewController
from Controller.modelController import ModelController

from Controller.cameraController import CameraController
from Controller.AIController import AIController
from Controller.deviceController import DeviceController


#===================================================================================================
class MainController:
    def __init__(self):
        # Initialize the controllers
        self.initControllers()

    def initControllers(self):
        ''' Initialize the controllers '''
        self.cameraController = CameraController()
        self.AIController = AIController()
        self.deviceController = DeviceController()

        # MVC architecture
        self.viewController = ViewController(self)
        self.modelController = ModelController()

    def run(self):
        # if Start Camera button is clicked
        self.showImages()

        # start main loop
        self.viewController.startMainLoop()
        

    def showImages(self):
        ''' Show the images '''
        
        images = self.modelController.getImages()
        # get a frame from the camera
        frame = self.cameraController.updateCameraFrame()

        # show the images
        self.viewController.setCameraFrame(frame)
        self.viewController.setImageFrame(images[0])

        # update the GUI
        self.viewController.updateGUIFrames()

    def showCameraFootage(self):
        ''' Debug: Show the camera feed '''
        self.cameraController._viewCameraLoop()

    

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    controller = MainController()
    controller.run()
    