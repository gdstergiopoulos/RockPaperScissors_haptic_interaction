import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QStackedWidget
from PyQt5.QtWidgets import (
    QListWidget, QSpinBox, QFormLayout, QFrame, QToolBox,
    QLineEdit, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

import View.QtStyling as qstyle

class GUI:
    def __init__(self, viewController):
        self.viewController = viewController

        # Initialize the GUI
        self.app = QApplication(sys.argv)
        # self.app.setStyleSheet(qstyle.dark_theme_stylesheet)  # apply the dark theme

        self.window = QWidget()
        self.window.setWindowTitle('Camera with Gestures')
        self.window.setFixedSize(1100, 700)  # fixed size of the window
        self.window.setStyleSheet(qstyle.window_stylesheet)  # apply the dark theme

        # Initialize the GUI
        self.initUI()

    def initUI(self):
        # Create the main menu
        self.createMainMenu()

        # Create the camera view
        self.createCameraView()

        # stacked widget to switch between the main menu and the camera view
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.camera_view)

        # Set the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.window.setLayout(main_layout)
        self.window.show()
    
    # ================== MAIN MENU PAGE ==================
    def createMainMenu(self):
        ''' Create the main menu '''
        self.main_menu = QWidget()
        
        # Main Layout (Horizontal Split: Left and Right)
        main_layout = QHBoxLayout()
        
        # -------- Left Side --------
        left_layout = QVBoxLayout()
        
        # Title
        self.title_label = QLabel("Rock Paper Scissors with Gestures")
        self.title_label.setStyleSheet(qstyle.header_stylesheet)   
        
        # Start Game Button
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.viewController.onStartButtonClicked)
        self.start_button.setFixedSize(200, 50)  # Set a fixed size for the button
        self.start_button.setStyleSheet(qstyle.blue_button_stylesheet)
        # self.start_button.setStyleSheet(qstyle.orange_button_stylesheet)   

        # horizontal layout to center the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()
        
        # Number of wins required to decide the victor
        self.wins_needed_label = QLabel("First to:")
        # self.wins_needed_label.setStyleSheet(qstyle.label_stylesheet) 
        self.wins_needed_spinbox = QSpinBox()
        self.wins_needed_spinbox.setRange(1, 10)  # range of acceptable values
        self.wins_needed_spinbox.setValue(3)  # default value of 3
        self.wins_needed_spinbox.setFixedSize(100, 30)  # fixed size for the spinbox
        self.wins_needed_spinbox.setStyleSheet(qstyle.spinbox_stylesheet)

        # horizontal layout for the wins needed label and spinbox
        wins_needed_layout = QFormLayout()
        wins_needed_layout.addRow(self.wins_needed_label, self.wins_needed_spinbox)

        # horizontal layout to center the wins needed layout
        centered_wins_needed_layout = QHBoxLayout()
        centered_wins_needed_layout.addStretch()
        centered_wins_needed_layout.addLayout(wins_needed_layout)
        centered_wins_needed_layout.addStretch()

        # Add widgets to left layout
        left_layout.addWidget(self.title_label)
        left_layout.addSpacing(50)  # some space between the title and the button
        left_layout.addLayout(button_layout)
        left_layout.addSpacing(50)  # some space between the button and the wins needed label
        left_layout.addLayout(centered_wins_needed_layout)  
        left_layout.addStretch()
        
        # -------- Right Side --------
        right_widget = QWidget()  # Wrap right_layout in a QWidget
        right_layout = QVBoxLayout(right_widget)

        # background color to right_widget
        # right_widget.setStyleSheet("background-color: #CFCFCF;")  # 
        
        # Current Username
        self.username_label = QLabel("Current User: User123")
        self.username_label.setStyleSheet(qstyle.label_stylesheet)
        
        # QToolBox for collapsible sections
        self.toolbox = QToolBox()

        # Recorded Attempts List
        self.recorded_attempts_list = QListWidget()
        self.recorded_attempts_list.addItems(["Attempt 1", "Attempt 2", "Attempt 3"])  # TODO
        self.recorded_attempts_list.setStyleSheet(qstyle.list_stylesheet)
        self.toolbox.addItem(self.recorded_attempts_list, "Recorded Attempts")

        # All Players List
        self.all_players_list = QListWidget()
        self.all_players_list.addItems(["Player 1", "Player 2", "Player 3"])  # TODO
        self.all_players_list.setStyleSheet(qstyle.list_stylesheet)
        self.toolbox.addItem(self.all_players_list, "All Players")

        # -------- Sign In Section --------
        sign_in_layout = QVBoxLayout()
        
        # Username Input
        self.username_input_label = QLabel("Username:")
        # self.username_input_label.setStyleSheet(qstyle.label_stylesheet)
        self.username_input = QLineEdit()
        self.username_input.setFixedSize(200, 30)
        self.username_input.setStyleSheet(qstyle.text_input_stylesheet)
        
        # Password Input
        self.password_input_label = QLabel("Password:")
        # self.password_input_label.setStyleSheet(qstyle.label_stylesheet)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(200, 30)
        self.password_input.setStyleSheet(qstyle.text_input_stylesheet)
        
        # Sign In Button
        self.sign_in_button = QPushButton("Sign In")
        self.sign_in_button.setFixedSize(200, 50)
        self.sign_in_button.setStyleSheet(qstyle.orange_button_stylesheet)
        self.sign_in_button.clicked.connect(self.viewController.onSignInButtonClicked)
        
        # Add widgets to sign in layout
        sign_in_layout.addWidget(self.username_input_label)
        sign_in_layout.addWidget(self.username_input)
        sign_in_layout.addWidget(self.password_input_label)
        sign_in_layout.addWidget(self.password_input)
        sign_in_layout.addWidget(self.sign_in_button)
        sign_in_layout.addStretch()
        
        # QWidget for the sign-in section and set its layout
        sign_in_widget = QWidget()
        sign_in_widget.setLayout(sign_in_layout)

        # Add the sign-in widget to the toolbox
        self.toolbox.addItem(sign_in_widget, "Sign In")

        # -------- New User Section --------
        new_user_layout = QVBoxLayout()

        # Username Input
        self.new_username_input_label = QLabel("Username:")
        # self.new_username_input_label.setStyleSheet(qstyle.label_stylesheet)
        self.new_username_input = QLineEdit()
        self.new_username_input.setFixedSize(200, 30)
        self.new_username_input.setStyleSheet(qstyle.text_input_stylesheet)

        # Password Input
        self.new_password_input_label = QLabel("Password:")
        # self.new_password_input_label.setStyleSheet(qstyle.label_stylesheet)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setFixedSize(200, 30)
        self.new_password_input.setStyleSheet(qstyle.text_input_stylesheet)

        # Confirm Password Input
        self.confirm_password_input_label = QLabel("Confirm Password:")
        # self.confirm_password_input_label.setStyleSheet(qstyle.label_stylesheet)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setFixedSize(200, 30)
        self.confirm_password_input.setStyleSheet(qstyle.text_input_stylesheet)

        # Register Button
        self.register_button = QPushButton("Register")
        self.register_button.setFixedSize(200, 50)
        self.register_button.setStyleSheet(qstyle.orange_button_stylesheet)
        # self.register_button.clicked.connect(self.viewController.onRegisterButtonClicked)

        # Add widgets to new user layout
        new_user_layout.addWidget(self.new_username_input_label)
        new_user_layout.addWidget(self.new_username_input)
        new_user_layout.addWidget(self.new_password_input_label)
        new_user_layout.addWidget(self.new_password_input)
        new_user_layout.addWidget(self.confirm_password_input_label)
        new_user_layout.addWidget(self.confirm_password_input)
        new_user_layout.addWidget(self.register_button)
        new_user_layout.addStretch()

        # QWidget for the new user section and set its layout
        new_user_widget = QWidget()
        new_user_widget.setLayout(new_user_layout)

        # Add the new user widget to the toolbox
        self.toolbox.addItem(new_user_widget, "New User")

        # Add widgets to right layout
        right_layout.addWidget(self.username_label)
        right_layout.addWidget(self.toolbox)
        # right_layout.addLayout(sign_in_layout)
        right_layout.addStretch()  # Push items to the top

        # -------- Add Divider Line --------
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(qstyle.divider_stylesheet)
        
        # -------- Combine Layouts --------
        main_layout.addLayout(left_layout, 3)  # Weight: Left takes more space
        main_layout.addWidget(line)  # Add the line between left and right layouts
        main_layout.addWidget(right_widget, 1)  # Weight: Right takes less space
        
        # Set the layout for the main menu
        self.main_menu.setLayout(main_layout)

    # ------------------ Main Menu Page Methods ------------------
    def showMainMenu(self):
        ''' Show the main menu '''
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def updateRecordedAttemptsList(self, attempts):
        ''' Update the recorded attempts list '''
        self.recorded_attempts_list.clear()
        self.recorded_attempts_list.addItems(attempts)

    def updateAllPlayersList(self, players):
        ''' Update the all players list '''
        self.all_players_list.clear()
        self.all_players_list.addItems(players)

    # ------------------ Getters ------------------
    def getSignInUsername(self):
        ''' Get the sign-in username '''
        return self.username_input.text()
    
    def getSignInPassword(self):
        ''' Get the sign-in password '''
        return self.password_input.text()
    
    # ------------------ Setters ------------------
    def setToolboxIndex(self, index):
        ''' Set the toolbox index '''
        self.toolbox.setCurrentIndex(index)
    
    def setCurrentUser(self, username):
        ''' Set the current user '''
        self.username_label.setText("Current User: " + username)
    # ===========================================================

    # ================== CAMERA VIEW PAGE ==================
    def createCameraView(self):
        ''' Create the camera view '''
        self.camera_view = QWidget()
        camera_view_layout = QHBoxLayout()

        # label to display the camera feed
        self.camera_label = QLabel(self.camera_view)
        self.camera_label.setFixedSize(640, 480)

        # label to display random images
        self.image_label = QLabel(self.camera_view)
        self.image_label.setFixedSize(640, 480)
        self.image_label.setScaledContents(True)  # Scale the image to fit the label

        camera_view_layout.addWidget(self.camera_label)
        camera_view_layout.addWidget(self.image_label)
        self.camera_view.setLayout(camera_view_layout)

    # ------------------ Camera View Page Methods ------------------
    def showCameraImageFrames(self):
        ''' Show the camera and image frames '''
        self.stacked_widget.setCurrentWidget(self.camera_view)

    def updateGUIFrames(self, cameraFrame, imageFrame):
        ''' Update the GUI frames '''
        self.camera_label.setPixmap(QPixmap.fromImage(cameraFrame))
        self.image_label.setPixmap(QPixmap.fromImage(imageFrame))
        self.app.processEvents()
    # ===========================================================

    # ================== GENERAL METHODS ==================
    def showSuccessMessage(self, msg):
        ''' Show a success message '''
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(msg)
        msg_box.exec_()

    def showErrorMessage(self, msg):
        ''' Show an error message '''
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(msg)
        msg_box.exec_()

    def startMainLoop(self):
        ''' Start the main loop '''
        sys.exit(self.app.exec_())