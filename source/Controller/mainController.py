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
        self.signed_in = False
        self.signed_in_user = None

        # Setup the controllers
        self.setupControllers()

    def initControllers(self):
        ''' Initialize the controllers '''
        self.cameraController = CameraController()
        self.AIController = AIController()
        self.deviceController = DeviceController()

        # MVC architecture
        self.viewController = ViewController(self)
        self.modelController = ModelController()
        print("Initialized all controllers")

    def setupControllers(self):
        ''' Setup the controllers '''
        self.viewController.setup()
        ... # other setup code
        print("Setup all controllers")

    def run(self):
        ''' Run the application '''
        # start main loop
        self.viewController.startMainLoop()
    
    # ----------------- Getters -----------------
    def getRecordedAttempts(self):
        ''' Get the recorded attempts '''
        current_user_name = self.getCurrentUser()["name"]
        if not current_user_name:
            return ["Sign in to store and view recorded attempts"]
        return self.modelController.getRecordedAttempts(current_user_name)

    def getCurrentUser(self):
        ''' Get the current user '''
        if not self.signed_in:
            return {"name": "", "password": None}
        else:
            return self.signed_in_user

    def getAllPlayers(self):
        ''' Get all players '''
        return self.modelController.getAllPlayers()
    
    def signIn(self, username, password):
        ''' Sign in the user '''
        # sign in the user
        # check if the user exists
        if username not in self.getAllPlayers():
            raise Exception('User does not exist')
        self.signed_in = True
        self.signed_in_user = {"name": username, "password": password}
    #
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
    