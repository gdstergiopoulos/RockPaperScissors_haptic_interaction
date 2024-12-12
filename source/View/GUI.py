import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QStackedWidget
from PyQt5.QtWidgets import (
    QListWidget, QSpinBox, QFormLayout, QFrame, QToolBox,
    QLineEdit, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSlot, QObject, Qt

import View.QtStyling as qstyle

class GUI(QObject):
    def __init__(self, viewController):
        super().__init__() # So that QThread can be used, it requires a QObject
        self.viewController = viewController

        # Initialize the GUI
        self.app = QApplication(sys.argv)
        # self.app.setStyleSheet(qstyle.dark_theme_stylesheet)  # apply the dark theme

        self.window = QWidget()
        self.window.setWindowTitle('Camera with Gestures')
        self.window.setFixedSize(1100, 700)  # fixed size of the window
        self.window.setStyleSheet(qstyle.window_stylesheet)  # apply the dark theme

        self.BASE_IMAGE_PATH = "Model/images"

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

        # Recorded Games List
        self.recorded_games_list = QListWidget()
        self.recorded_games_list.addItems(["Attempt 1", "Attempt 2", "Attempt 3"])  
        self.recorded_games_list.setStyleSheet(qstyle.list_stylesheet)
        self.toolbox.addItem(self.recorded_games_list, "Recorded Games")

        # All Players List
        self.all_players_list = QListWidget()
        self.all_players_list.addItems(["Player 1", "Player 2", "Player 3"])  
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
        self.register_button.clicked.connect(self.viewController.onRegisterButtonClicked)

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

        # -------- Sign Out Button --------
        self.sign_out_button = QPushButton("Sign Out")
        self.sign_out_button.setFixedSize(130, 50)
        self.sign_out_button.setStyleSheet(qstyle.orange_button_stylesheet)
        self.sign_out_button.clicked.connect(self.viewController.onSignOutButtonClicked)

        # Add the sign out button to the toolbox
        self.toolbox.addItem(self.sign_out_button, "Sign Out")

        # Add widgets to right layout
        right_layout.addWidget(self.username_label)
        right_layout.addWidget(self.toolbox)
        # right_layout.addWidget(self.sign_out_button)
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

    def updateRecordedGamesList(self, games):
        ''' Update the recorded games list '''
        self.recorded_games_list.clear()
        self.recorded_games_list.addItems(games)

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
    
    def getRegisterUsername(self):
        ''' Get the register username '''
        return self.new_username_input.text()
    
    def getRegisterPassword(self):
        ''' Get the register password '''
        return self.new_password_input.text()
    
    def getRegisterConfirmPassword(self):
        ''' Get the confirm password '''
        return self.confirm_password_input.text()
    
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
        # create camera view widget
        self.camera_view = QWidget()

        # main layout, that will hold all elements
        self.camera_view_layout = QVBoxLayout()
        
        self.title_label = QLabel("Rock Paper Scissors with Gestures")
        self.title_label.setStyleSheet(qstyle.header_stylesheet) 
        self.camera_view_layout.addWidget(self.title_label)

        #  Shows wins required to win the game
        self.top_label = QLabel("First to")
        self.top_label.setStyleSheet(qstyle.label_stylesheet)
        self.camera_view_layout.addWidget(self.top_label)

        # layout containing the camera footage and the computer image 
        self.user_computer_layout = QHBoxLayout()

        # layout containing the camera footage
        self.user_layout = QVBoxLayout()
        self.camera_label = QLabel(self.camera_view)
        self.camera_label.setFixedSize(490, 300)
        self.user_layout.addWidget(self.camera_label)

        self.user_score = QLabel("User's Score: 0")
        self.user_gesture = QLabel("User's Gesture: None")
        self.user_gesture.setStyleSheet(qstyle.label_stylesheet)
        self.user_score.setStyleSheet(qstyle.label_stylesheet)
        self.user_layout.addWidget(self.user_score)
        self.user_layout.addWidget(self.user_gesture)


        self.user_computer_layout.addLayout(self.user_layout)

        # VS Text layout
        self.vs_layout = QVBoxLayout()
        self.vs_label = QLabel("VS")
        self.vs_layout.addWidget(self.vs_label)
        self.vs_label.setStyleSheet(qstyle.header_stylesheet) 
        self.vs_layout.setAlignment(self.vs_label, Qt.AlignCenter)        
        # self.round_label = QLabel("Round 1")
        # self.vs_layout.addWidget(self.round_label)
        # self.vs_label.setStyleSheet(qstyle.header_stylesheet) 
        # self.vs_layout.setAlignment(self.round_label, Qt.AlignCenter)

        # computer image layout
        self.computer_layout = QVBoxLayout()
        self.image_label = QLabel(self.camera_view)
        self.image_label.setFixedSize(490, 300)
        

        # Set the question mark image as the default image
        self.setComputerChoiceImage("question_mark")
        self.computer_layout.setAlignment(self.camera_view, Qt.AlignCenter)
        self.computer_layout.addWidget(self.image_label)
        

        self.computer_score = QLabel("Computer's Score: 0")
        self.computer_gesture = QLabel("Computer's Gesture: None")
        self.computer_gesture.setStyleSheet(qstyle.label_stylesheet)
        self.computer_score.setStyleSheet(qstyle.label_stylesheet)
        self.computer_layout.addWidget(self.computer_score)
        self.computer_layout.addWidget(self.computer_gesture)

        self.user_computer_layout.addLayout(self.vs_layout)
        self.user_computer_layout.addLayout(self.computer_layout)


        # area containing the results of the game
        self.result_layout = QVBoxLayout()
        self.result_area = QLabel("Round 1")
        self.result_area.setStyleSheet(qstyle.label_stylesheet)
        self.result_layout.addWidget(self.result_area)
        self.result_layout.setAlignment(Qt.AlignCenter)
        self.winner_area = QLabel("")
        self.winner_area.setStyleSheet(qstyle.label_stylesheet)
        self.result_layout.addWidget(self.winner_area)
        self.result_layout.setAlignment(Qt.AlignCenter)
        
        
        # button to go back to the main menu
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.viewController.onBackButtonClicked)
        self.back_button.setFixedSize(100, 50)
        self.back_button.setStyleSheet(qstyle.blue_button_stylesheet)        

        self.camera_view_layout.addLayout(self.user_computer_layout)
        # self.camera_view_layout.addWidget(self.bottom_text)
        self.camera_view_layout.addLayout(self.result_layout)
        self.camera_view_layout.addWidget(self.back_button)

        self.camera_view.setLayout(self.camera_view_layout)


    # ------------------ Camera View Page Methods ------------------

    def update_text_areas(self, text_info):
        """Update individual QLabel widgets based on text_info."""
        if "User Gesture" in text_info:
            self.user_gesture.setText(f"User's Gesture: {text_info['User Gesture']}")
        if "Computer Choice" in text_info:
            self.computer_gesture.setText(f"Computer's Gesture: {text_info['Computer Choice']}")
            print(text_info['Computer Choice'])
            self.updateComputerChoice(text_info['Computer Choice'])
        if "Result" in text_info:
            self.result_area.setText(f"Round {text_info['Round']}: {text_info['Result']}")
        if "User Score" in text_info:
            self.user_score.setText(f"User's Score: {text_info['User Score']}")
        if "Computer Score" in text_info:
            self.computer_score.setText(f"Computer's Score: {text_info['Computer Score']}")
        if "Winner" in text_info and text_info["Winner"] is not None:
            if text_info["Winner"]=="User":
                self.winner_area.setText("You Won!")
                self.winner_area.setStyleSheet("color: green;")
                self.winner_area.setStyleSheet("""
                    font-family: 'Arial';
                    font-size: 32px;
                    color: red;
                    """)
                # save the game in the database
                self.viewController.saveGame(text_info['User Score'], text_info["Winner"])
            if text_info["Winner"]=="Computer":
                self.winner_area.setText("You Lost :(")
                self.winner_area.setStyleSheet("""
                    font-family: 'Arial';
                    font-size: 32px;
                    color: red;
                    """)
                # save the game in the database
                self.viewController.saveGame(text_info['Computer Score'], text_info["Winner"])
        else:
            self.winner_area.setText("")

    def showCameraImageFrames(self):
        ''' Show the camera and image frames '''
        self.stacked_widget.setCurrentWidget(self.camera_view)


    def showLoadingMessage(self, msg):
        self.loading_label = QLabel(msg, self.window)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("font-size: 16px; color: blue;")
        self.loading_label.show()

    def hideLoadingMessage(self):
        if hasattr(self, 'loading_label'):
            self.loading_label.hide()

            
    @pyqtSlot(QImage)
    def updateCameraFrame(self, cameraFrame: QImage):
        ''' Update the camera frame '''
        self.camera_label.setPixmap(QPixmap.fromImage(cameraFrame))
        self.app.processEvents()

    def updateGUIFrames(self, cameraFrame, imageFrame):
        ''' Update the GUI frames '''
        self.camera_label.setPixmap(QPixmap.fromImage(cameraFrame))
        self.image_label.setPixmap(QPixmap.fromImage(imageFrame))
        self.app.processEvents()

    def updateFirstToLabel(self, wins_required):
        """ Update the 'First to #' label in the camera view """
        self.top_label.setText(f"First To {wins_required} Wins!")  # Dynamically set the label

    def showWinner(self, winner):
        ''' Show the winner '''
        self.showSuccessMessage(f"{winner} Wins!")

    def setComputerChoiceImage(self, image_name):
        image_path = f"{self.BASE_IMAGE_PATH}/{image_name}.jpg"
        print(image_path)
        ''' Set the computer choice image, default to question mark initially '''
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectRatioMode=1))  # Scale image to fit the label

    def updateComputerChoice(self, choice_image):
        ''' Update the computer's choice image when it makes its decision '''
        self.setComputerChoiceImage(choice_image)

    
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