
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
import cv2 
import sys
import time

class CameraThread(QThread):
    frame_ready = pyqtSignal(QImage)  # Signal to send frames to the GUI

    def __init__(self, viewController, parent=None):
        super().__init__(parent)

        self.viewController = viewController
        self.running = True  # Control flag for the thread

    def addTextToFrame(self, frame, user_gesture, computer_choice, result, winner):
        # Add text to the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (255, 255, 255)
        line_type = 2
        cv2.putText(frame, f'User: {user_gesture}', (10, 30), font, font_scale, font_color, line_type)
        cv2.putText(frame, f'Computer: {computer_choice}', (10, 60), font, font_scale, font_color, line_type)
        cv2.putText(frame, f'Result: {result}', (10, 90), font, font_scale, font_color, line_type)
        cv2.putText(frame, f'User Score: {self.viewController.getUserScore()}', (10, 120), font, font_scale, font_color, line_type)
        cv2.putText(frame, f'Computer Score: {self.viewController.getComputerScore()}', (10, 150), font, font_scale, font_color, line_type)

        if winner:
            cv2.putText(frame, f'Winner: {winner}', (200, 250), font, font_scale, font_color, line_type)
            cv2.putText(frame, 'Press SPACE to restart.', (200, 300), font, font_scale, font_color, line_type)

    def run(self):
        # cap = cv2.VideoCapture(0)  # Open camera
        # request the camera open from viewController --> mainController --> cameraController
        try:
            self.viewController.openCamera()
            while self.running:
                # ret, frame = cap.read()
                # request the frame from viewController --> mainController --> cameraController
                ret, frame = self.viewController.updateCameraFrame()
                if ret:
                    # initiate the game round
                    frame, user_gesture, computer_choice, result = self.viewController.playRound(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                    self.viewController.handleScore(result)
                    haveWinner, winnerName = self.viewController.checkGameWinner()
                    self.addTextToFrame(frame, user_gesture, computer_choice, result, winnerName)
                    if haveWinner:
                        # self.viewController.showWinner(winnerName)
                        self.viewController.resetGame()
                    h, w, ch = frame.shape
                    bytes_per_line = ch * w
                    q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    # Ensure the QImage object is valid before emitting
                    if q_image.isNull():
                        raise Exception('Error: Invalid QImage object.')
                    
                    # Emit the frame to the GUI
                    # print(f"Emitting frame: {type(q_image)}")
                    self.frame_ready.emit(q_image)

                # time.sleep(0.03)  # To avoid overwhelming the CPU (approx 30 FPS)
                time.sleep(0.018) # To avoid overwhelming the CPU (approx 60 FPS)
            # cap.release()
            # request the camera release from viewController --> mainController --> cameraController
            self.viewController.releaseCamera()
        except Exception as e:
            raise Exception('Error in CameraThread: ' + str(e))

    def stop(self):
        self.running = False
        self.wait()  # Wait for the thread to finish cleanly