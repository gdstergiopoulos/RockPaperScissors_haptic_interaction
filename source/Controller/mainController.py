import random

from Controller.viewController import ViewController
from Controller.modelController import ModelController

from Controller.cameraController import CameraController
from Controller.AIController import AIController
# from Controller.deviceController import DeviceController


#===================================================================================================
class MainController:
    def __init__(self):
        # Initialize the controllers
        self.initControllers()
        self.signed_in = False
        self.signed_in_user = None

        # gameplay variables
        self.user_score = 0
        self.computer_score = 0
        self.winning_score = 3 # get from GUI
        self.winner = None

        # Setup the controllers
        self.setupControllers()

    def initControllers(self):
        ''' Initialize the controllers '''
        self.cameraController = CameraController()
        self.AIController = AIController("./AI/gesture_recognizer.task")
        # self.deviceController = DeviceController()

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
    def getRecordedGames(self):
        ''' Get the recorded games '''
        current_user_name = self.getCurrentUsername()
        if not current_user_name:
            return ["Sign in to store and\n view recorded games"]
        return self.modelController.getRecordedGames(current_user_name)

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
    
    def getUserScore(self):
        ''' Get the user score '''
        return self.user_score
    
    def getComputerScore(self):
        ''' Get the computer score '''
        return self.computer_score
    
    def getWinningScore(self):
        ''' Get the score required to win '''
        return self.winning_score
    
    def getTimerImages(self):
        ''' Get the timer images '''
        return self.modelController.getTimerImages()
    # ----------------- Setter -----------------

    def setWinningScore(self, winning_score):
        self.winning_score = winning_score
        return self.winning_score
    
    # ----------------- Sign in/Sign out/Register -----------------
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

    # ----------------- Camera-related -----------------
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
    
    def stopCamera(self):
        ''' Request the camera stop from the cameraController '''
        return self.cameraController.stopCamera()

    # ----------------- Gameplay -----------------
    def playRound(self, frame):
        ''' Play a round of the game:
            - Process frame for hand landmarks
            - Detect the user's gesture
            - Decide the winner
        '''
        # Process frame for hand landmarks
        frame_rgb, results_hands = self.AIController.processFrame(frame)
        user_gesture = "none"

        if results_hands.multi_hand_landmarks:
            self.AIController.drawHandLandmarks(frame, results_hands.multi_hand_landmarks)
            gesture_result = self.AIController.detectGesture(frame_rgb)
            user_gesture = self.AIController.extractUserGesture(gesture_result)
        
        # computer_choice = self.AIController.getComputerChoice() # smarter decision-making
        computer_choice = random.choice(["rock", "paper", "scissors"])
        result = self.decideWinner(user_gesture, computer_choice)
    
        
        return frame, user_gesture, computer_choice, result

    def decideWinner(self, user_choice, computer_choice):
        ''' Decide the winner '''
        if user_choice == computer_choice:
            return "Draw"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "scissors" and computer_choice == "paper") or \
             (user_choice == "paper" and computer_choice == "rock"):
            # requests.get("https://maker.ifttt.com/trigger/win/with/key/pM1ozEUO5xiOUE5_g0RXgILQN8aLT3kw2KpVtTp-LRg")
            return "User Wins!"
        elif user_choice == "none" or not user_choice:
            return "No gesture detected. Try again."
        else:
            # requests.get("https://maker.ifttt.com/trigger/loss/with/key/pM1ozEUO5xiOUE5_g0RXgILQN8aLT3kw2KpVtTp-LRg")
            return "Computer Wins!"
        
    def handleScore(self, result):
        ''' Handle the score '''
        if result == "User Wins!":
            self.user_score += 1
        elif result == "Computer Wins!":
            self.computer_score += 1
        return None
    
    def checkGameWinner(self) -> tuple:
        ''' Check the game winner 
        Returns:
            (bool, str): True if there is a winner, False otherwise. The winner's name'''
        if self.user_score >= self.winning_score:
            self.winner = "User"
            # self.deviceController.sendWinnerMessage()
            return (True, self.winner)
        elif self.computer_score >= self.winning_score:
            self.winner = "Computer"
            # self.deviceController.sendLoserMessage()
            return (True, self.winner)
        return (False, None)

    def resetGame(self):
        ''' Reset the game '''
        self.user_score = 0
        self.computer_score = 0
        self.winner = None

    def saveGame(self, winning_score, winner):
        ''' Pass game's parameters to the modelController to Save User's Game'''
        if not self.signed_in_user:
            print("Not signed in user, game not saved")
            return None
        return self.modelController.saveGame(winning_score, winner, self.signed_in_user)

    def showCameraFootage(self):
        ''' Debug: Show the camera feed '''
        self.cameraController._viewCameraLoop()

    def on_exit(self):
        ''' Handle the exit process '''
        self.releaseCamera()
        self.viewController.on_exit()
        print("Exiting the application")

    

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    controller = MainController()
    controller.run()
    
    