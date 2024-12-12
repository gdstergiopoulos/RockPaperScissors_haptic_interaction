
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
import cv2 
import sys
import time

class CameraThread(QThread):
    frame_ready = pyqtSignal(QImage)  # Signal to send frames to the GUI
    text_ready = pyqtSignal(dict)

    def __init__(self, viewController, parent=None):
        super().__init__(parent)

        self.viewController = viewController
        self.running = True  # Control flag for the thread
        self.round_delay = 3  # Delay time in seconds


    # def run(self):
    #     try:
    #         self.viewController.openCamera()
    #         while self.running:
    #             ret, frame = self.viewController.updateCameraFrame()
    #             if ret:
    #                 # Initiate the game round
    #                 frame, user_gesture, computer_choice, result = self.viewController.playRound(frame)
    #                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    #                 self.viewController.handleScore(result)
    #                 haveWinner, winnerName = self.viewController.checkGameWinner()

    #                 # Collect text information for GUI display
    #                 text_info = {
    #                     "User Gesture": user_gesture,
    #                     "Computer Choice": computer_choice,
    #                     "Result": result,
    #                     "User Score": self.viewController.getUserScore(),
    #                     "Computer Score": self.viewController.getComputerScore(),
    #                     "Winner": winnerName if haveWinner else None
    #                 }

    #                 # Emit the text information
    #                 self.text_ready.emit(text_info)

    #                 # if haveWinner:
    #                 #     # self.viewController.resetGame()
    #                 #     self.viewController.showWinner(winnerName)

    #                 # Convert frame to QImage and emit it                    
    #                 h, w, ch = frame.shape
    #                 bytes_per_line = ch * w
    #                 q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

    #                 if q_image.isNull():
    #                     raise Exception('Error: Invalid QImage object.')

    #                 self.frame_ready.emit(q_image)

    #             time.sleep(0.018)  # ~60 FPS

    #         self.viewController.releaseCamera()
    #     except Exception as e:
    #         raise Exception('Error in CameraThread: ' + str(e))

    def run(self): 
        try:
            self.viewController.openCamera()
            winner_found = False  # Track if a winner has been determined
            round = 0
            while self.running:
                # Wait for the user to make a choice
                start_time = time.time()
                while time.time() - start_time < self.round_delay:
                    ret, frame = self.viewController.updateCameraFrame()
                    if ret:
                        # Show the frame without playing a round
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        h, w, ch = frame.shape
                        bytes_per_line = ch * w
                        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

                        if q_image.isNull():
                            raise Exception('Error: Invalid QImage object.')

                        self.frame_ready.emit(q_image)

                    time.sleep(0.018)  # Maintain the frame rate (~60 FPS)

                if winner_found:
                    # If there's already a winner, skip the game logic but keep the feed running
                    continue

                # if winner_found:
                #     # If there's already a winner, skip the game logic but keep the feed running
                #     # continue
                #     winner_found = False
                #     round = 1
                #     self.viewController.resetGame()

                # Start a round after the delay
                ret, frame = self.viewController.updateCameraFrame()
                if ret:
                    frame, user_gesture, computer_choice, result = self.viewController.playRound(frame)
                    self.viewController.handleScore(result)
                    haveWinner, winnerName = self.viewController.checkGameWinner()
                    round += 1
                    if haveWinner:
                        winner_found = True  # Stop the game logic for future rounds
                        text_info = {
                            "User Gesture": user_gesture,
                            "Computer Choice": computer_choice,
                            "Result": result,
                            "User Score": self.viewController.getUserScore(),
                            "Computer Score": self.viewController.getComputerScore(),
                            "Winner": winnerName,
                            "Round" : round
                        }
                    else:
                        text_info = {
                            "User Gesture": user_gesture,
                            "Computer Choice": computer_choice,
                            "Result": result,
                            "User Score": self.viewController.getUserScore(),
                            "Computer Score": self.viewController.getComputerScore(),
                            "Winner": None,
                            "Round" : round
                        }

                    # Emit the text information only if there's no winner
                    self.text_ready.emit(text_info)

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = frame.shape
                    bytes_per_line = ch * w
                    q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

                    if q_image.isNull():
                        raise Exception('Error: Invalid QImage object.')

                    self.frame_ready.emit(q_image)

                time.sleep(0.018)  # Maintain the frame rate (~60 FPS)

            self.viewController.releaseCamera()
        except Exception as e:
            raise Exception('Error in CameraThread: ' + str(e))


    def stop(self):
        self.running = False
        self.wait()  # Wait for the thread to finish cleanly