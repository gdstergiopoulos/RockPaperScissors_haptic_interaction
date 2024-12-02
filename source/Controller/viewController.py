import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

class ViewController:
    def __init__(self, mainController):
        # store the main controller
        self.mainController = mainController

        # Initialize the GUI
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle('Camera with Gestures')

        # Received from mainController.py
        self.cameraFrame = None
        self.imageFrame = None

        # Initialize the GUI
        self.initUI()

    def initUI(self):
        # Create the main menu
        self.main_menu = QWidget()
        main_menu_layout = QVBoxLayout()
        self.start_button = QPushButton("Start Camera")
        self.start_button.clicked.connect(self.onStartButtonClicked)
        main_menu_layout.addWidget(self.start_button)
        self.main_menu.setLayout(main_menu_layout)

        # Create the camera view
        self.camera_view = QWidget()
        camera_view_layout = QHBoxLayout()

        # Create a label to display the camera feed
        self.camera_label = QLabel(self.camera_view)
        self.camera_label.setFixedSize(640, 480)

        # Create a label to display random images
        self.image_label = QLabel(self.camera_view)
        self.image_label.setFixedSize(640, 480)
        self.image_label.setScaledContents(True)  # Scale the image to fit the label

        camera_view_layout.addWidget(self.camera_label)
        camera_view_layout.addWidget(self.image_label)
        self.camera_view.setLayout(camera_view_layout)

        # Create a stacked widget to switch between the main menu and the camera view
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.camera_view)

        # Set the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.window.setLayout(main_layout)
        self.window.show()

    def onStartButtonClicked(self):
        ''' Handle the Start Camera button click '''
        self.mainController.showImages()
        self.showCameraImageFrames()

    def showMainMenu(self):
        ''' Show the main menu '''
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def showCameraImageFrames(self):
        ''' Show the camera and image frames '''
        self.stacked_widget.setCurrentWidget(self.camera_view)

    def startMainLoop(self):
        ''' Start the main loop '''
        sys.exit(self.app.exec_())

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
        self.camera_label.setPixmap(QPixmap.fromImage(self.cameraFrame))
        self.image_label.setPixmap(QPixmap.fromImage(self.imageFrame))
        self.app.processEvents()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q or event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    controller = ViewController()
    controller.startMainLoop()