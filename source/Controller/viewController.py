import cv2
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt

from View.GUI import GUI
from View.CameraThread import CameraThread
from PyQt5.QtCore import pyqtSlot

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
        self.updateRecordedGamesList()
        self.updateAllPlayersList()
        self.updateCurrentPlayer()

    # ================== BUTTON CLICK HANDLERS ==================
    def onStartButtonClicked(self):
        ''' Handle the Start Camera button click '''
        # self.mainController.showImages()

        # Capture the number of wins required from the GUI
        self.wins_required = self.gui.wins_needed_spinbox.value()  # Get the value from the SpinBox
        
        # Pass the value to the camera view to update the "First to #" label
        self.gui.updateFirstToLabel(self.wins_required)  # This method will update the label in the camera view
        
        # Set up the camera thread and show the camera view
        self.setupThread()
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
        
        # update the recorded Games list
        self.updateRecordedGamesList()


    def onRegisterButtonClicked(self):
        ''' Handle the Register button click '''
        # get the username and password from the GUI
        username = self.gui.getRegisterUsername()
        password = self.gui.getRegisterPassword()
        confirm_password = self.gui.getRegisterConfirmPassword()
        if not username or not password or not confirm_password:
            self.gui.showErrorMessage('Please enter a username and password')
            return
        
        # check if the passwords match
        if password != confirm_password:
            self.gui.showErrorMessage('Passwords do not match')
            return
        
        # register the user
        try:
            self.mainController.registerNewPlayer(username, password)
            self.gui.showSuccessMessage('Registered successfully!')
            self.gui.setCurrentUser(username)
            self.gui.setToolboxIndex(0)
        except Exception as e:
            errorMessage = 'Error registering: ' + str(e)
            self.gui.showErrorMessage(errorMessage)
        
        # update the recorded Games list
        self.updateRecordedGamesList()
        # update the all players list
        self.updateAllPlayersList()

    def onSignOutButtonClicked(self):
        ''' Handle the Sign Out button click '''
        if self.mainController.signed_in == True:    
            self.mainController.signOut()
            self.setup() # reset the GUI
            self.gui.showSuccessMessage('Signed out successfully!')
        else:
            self.gui.showErrorMessage('No user is signed in')   
    
    def onBackButtonClicked(self):
        ''' Handle the Back button click '''
        self.gui.showMainMenu()

    
    # ===========================================================

    # ================== LIST WIDGET HANDLERS ==================
    def updateRecordedGamesList(self):
        ''' Update the recorded Games list '''
        # request the recorded Games from the main controller
        # for current user
        try:
            recordedGames = self.mainController.getRecordedGames()
            self.gui.updateRecordedGamesList(recordedGames)
        except Exception as e:
            errorMessage = 'Error getting recorded Games: ' + str(e)
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
    
    def updateCurrentPlayer(self):
        ''' Update the current player '''
        # get the current user from the main controller
        current_user = self.mainController.getCurrentUsername()
        self.gui.setCurrentUser(current_user)
    # =====================================================================
    
    # ================== CAMERA/GAMEPLAY FRAME HANDLERS ==================
    def frameToQImage(self, frame):
        '''Convert the frame to an image format that PyQt can handle'''
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        frame = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        return frame

    # ------------------ CAMERA METHODS ------------------
    def setupThread(self):
        ''' Setup the camera thread '''
        self.cameraThread = CameraThread(self)
        self.cameraThread.frame_ready.connect(self.gui.updateCameraFrame)
        self.cameraThread.text_ready.connect(self.gui.update_text_areas)
        # self.cameraThread.frame_ready.connect(lambda frame: print(f"Received frame: {type(frame)}"))
        self.cameraThread.start()

    def openCamera(self):
        ''' Request from the main controller to open the camera '''
        return self.mainController.openCamera()

    def updateCameraFrame(self):
        ''' Request the frame from the main controller '''
        return self.mainController.updateCameraFrame()
    
    def releaseCamera(self):
        ''' Request the main controller to release the camera '''
        return self.mainController.releaseCamera()

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

    def showWinner(self, winner):
        ''' Show the winner '''
        self.gui.showWinner(winner)


    # ------------------ GAMEPLAY METHODS ------------------
    def playRound(self, frame):
        ''' Pass the frame to the main controller to play a round '''
        return self.mainController.playRound(frame)
    
    def handleScore(self, result):
        ''' Ask the main controller to handle the score '''
        return self.mainController.handleScore(result)
    
    def checkGameWinner(self):
        ''' Ask the main controller to check the game winner '''
        return self.mainController.checkGameWinner()
    
    def resetGame(self):
        ''' Ask the main controller to reset the game '''
        self.gui.setComputerChoiceImage("question_mark")
        return self.mainController.resetGame()
    
    def getUserScore(self):
        ''' Get the user score '''
        return self.mainController.getUserScore()
    
    def getComputerScore(self):
        ''' Get the computer score '''
        return self.mainController.getComputerScore()
    
    # Save the game
    def saveGame(self, winning_score, winner ):
        '''Pass the game's parameters to the mainController'''
        return self.mainController.saveGame(winning_score, winner)
        
        
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