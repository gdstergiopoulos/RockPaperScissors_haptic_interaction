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
        current_user_name = self.getCurrentUsername()
        if not current_user_name:
            return ["Sign in to store and\n view recorded attempts"]
        return self.modelController.getRecordedAttempts(current_user_name)

    def getCurrentUsername(self):
        ''' Get the current user '''
        if not self.signed_in:
            return ""
        else:
            return self.signed_in_user
        
    def getCurrentUserPassword(self):
        ''' Get the current user password '''
        if not self.signed_in:
            return ""
        else:
            return self.modelController.getPlayerPassword(self.signed_in_user)

    def getAllPlayers(self):
        ''' Get all players '''
        return self.modelController.getAllPlayers()
    
    def signIn(self, username, password):
        ''' Sign in the user '''
        # sign in the user
        # check if the user exists
        if username not in self.getAllPlayers():
            raise Exception('User does not exist')
        # check if the password is correct
        db_password = self.modelController.getPlayerPassword(username)
        if db_password != password:
            raise Exception('Incorrect password')
        self.signed_in = True
        self.signed_in_user = username
    
    def registerNewPlayer(self, username, password):
        ''' Register a new player '''
        # check if the user already exists
        if username in self.getAllPlayers():
            raise Exception('User already exists')
        # register the new player
        # add the player to the database
        self.modelController.registerNewPlayer(username, password)
        self.signed_in = True
        self.signed_in_user = username

    def signOut(self):
        ''' Sign out the user '''
        self.signed_in = False
        self.signed_in_user = None

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

    def openCamera(self):
        ''' Request the camera open from the cameraController '''
        return self.cameraController.openCamera()

    def updateCameraFrame(self):
        ''' Request the frame from the cameraController '''
        return self.cameraController.updateCameraFrame()
    
    def releaseCamera(self):
        ''' Request the camera release from the cameraController '''
        self.cameraController.releaseCamera()

    def showCameraFootage(self):
        ''' Debug: Show the camera feed '''
        self.cameraController._viewCameraLoop()

    

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    controller = MainController()
    controller.run()
    