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
    
    def setup(self):
        ''' Setup the GUI '''
        self.updateRecordedAttemptsList()
        self.updateAllPlayersList()

    # ================== BUTTON CLICK HANDLERS ==================
    def onStartButtonClicked(self):
        ''' Handle the Start Camera button click '''
        self.mainController.showImages()
        self.gui.showCameraImageFrames()

    def onSignInButtonClicked(self):
        ''' Handle the Sign In button click '''
        # get the username and password from the GUI
        username = self.gui.getSignInUsername()
        password = self.gui.getSignInPassword()
        if not username or not password:
            self.gui.showErrorMessage('Please enter a username and password')
            return

        # sign in the user
        try:
            self.mainController.signIn(username, password)
            self.gui.showSuccessMessage('Signed in successfully!')
            # name = self.mainController.getCurrentUser().name # not strictly necessary, we use the given username
            self.gui.setCurrentUser(username)
            self.gui.setToolboxIndex(0)
        except Exception as e:
            errorMessage = 'Error signing in: ' + str(e)
            self.gui.showErrorMessage(errorMessage)
        
        # update the recorded attempts list
        self.updateRecordedAttemptsList()
    # ===========================================================

    # ================== LIST WIDGET SELECTION HANDLERS ==================
    def updateRecordedAttemptsList(self):
        ''' Update the recorded attempts list '''
        # request the recorded attempts from the main controller
        # for current user
        try:
            recordedAttempts = self.mainController.getRecordedAttempts()
            self.gui.updateRecordedAttemptsList(recordedAttempts)
        except Exception as e:
            errorMessage = 'Error getting recorded attempts: ' + str(e)
            self.gui.showErrorMessage(errorMessage)
    
    def updateAllPlayersList(self):
        ''' Update the all players list '''
        # request all players from the main controller
        try:
            allPlayers = self.mainController.getAllPlayers()
            self.gui.updateAllPlayersList(allPlayers)
        except Exception as e:
            errorMessage = 'Error getting all players: ' + str(e)
            self.gui.showErrorMessage(errorMessage)
    # =====================================================================
    
    # ================== CAMERA/GAMEPLAY FRAME HANDLERS ==================
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
    # =================================================================

    # ================== GENERAL METHODS ==================
    def startMainLoop(self):
        ''' Start the main loop '''
        self.gui.startMainLoop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q or event.key() == Qt.Key_Escape:
            self.gui.window.close()

if __name__ == '__main__':
    controller = ViewController(None)
    controller.startMainLoop()