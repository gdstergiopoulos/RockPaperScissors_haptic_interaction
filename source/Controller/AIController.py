import cv2
import os
import mediapipe as mp

class AIController:
    def __init__(self, model_path):
        # Initialize the hand landmarks processor
        self.hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

        # self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        # Known issue with mediapipe, https://stackoverflow.com/questions/75985134/mediapipe-runtime-error-whilst-following-the-hand-landmarker-guide-unable-to-in
        #  load the file as bytes and then pass the byte object to the factory method:
        model_file = open(model_path, "rb")
        model_data = model_file.read()
        model_file.close()

        self.options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_buffer=model_data)
        )
        self.recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(self.options)

    def processFrame(self, frame):
        ''' Process the frame for hand landmarks
        Args:
            frame: The frame to process
        Returns:
            frame_rgb: The processed frame
            results_hands: The hand landmarks
        '''
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_hands = self.hands.process(frame_rgb)
        return frame_rgb, results_hands
    
    def drawHandLandmarks(self, frame, hand_landmarks):
        ''' Draw the hand landmarks on the frame.
        meaning the skeleton of the hand for the benefit of the user
        Args:
            frame: The frame to draw the landmarks on
            hand_landmarks: The landmarks to draw
        '''
        for landmarks in hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    def detectGesture(self, frame):
        ''' Detect the gesture from the frame
        Args:
            frame: The frame to detect the gesture from
        Returns:
            The gesture result
        '''
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        result = self.recognizer.recognize(mp_image)
        return result
        
    def extractUserGesture(self, result):
        ''' Extract the user gesture from the result
        Args:
            result: The result to extract the gesture from
        Returns:
            The user gesture
        '''
        if result.gestures and len(result.gestures) > 0:
            gesture = result.gestures[0][0]
            return gesture.category_name
        return "none"
