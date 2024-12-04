import cv2
import mediapipe as mp
import random
import requests

# Import necessary components from MediaPipe Tasks
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult

# Game choices
choices = ["rock", "paper", "scissors"]

# Function to determine the result of the game
def decide_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Draw"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        return "User Wins!"
    elif user_choice == "none":
        return "Try again pal!"
    else:
        return "Computer Wins!"

# Callback function to handle gesture recognition results
def get_user_gesture(result: GestureRecognizerResult):
    if result.gestures and len(result.gestures) > 0:
        gesture = result.gestures[0][0]  # Get the top gesture
        return gesture.category_name
    else:
        return None

# Initialize MediaPipe Hands for hand landmarks
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Gesture Recognizer options
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=r'./gesture_recognizer.task')
)

# Initialize the Gesture Recognizer
with GestureRecognizer.create_from_options(options) as recognizer, mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    print("Press 'g' to capture a gesture or 'q' to quit.")

    # Variables to hold current visuals
    user_gesture = None
    computer_choice = None
    result = None
    display_text = False

    user_score=0
    computer_score=0
    winning_score=3
    winner=None
    started=False
    while True:
        
        # Capture a frame
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        # Flip and process the frame
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_hands = hands.process(frame_rgb)

        # Draw hand landmarks if detected
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show previously captured results until a new gesture is captured
        if display_text:
            if user_gesture:
                if(winner is None):
                    cv2.putText(frame, f"User: {user_gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.putText(frame, f"Computer: {computer_choice}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.putText(frame, f"Result: {result}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    cv2.putText(frame, f"User Score: {user_score}", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, f"Computer Score: {computer_score}", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                else:
                    if(winner=='User'):
                        cv2.putText(frame, "You won!", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                        cv2.putText(frame, "Press SPACE to continue", (190, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    elif(winner=='Computer'):
                        cv2.putText(frame, "Game Over, you lost :(", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                        cv2.putText(frame, "Press SPACE to continue", (190, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "No gesture detected. Try again", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Press G to start the game", (190, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
       
            

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            print("Game ended")
            if(winner=="User"):
                print("User won")
            elif(winner=="Computer"):
                print("Computer won")
            break
        if key == ord('g'):  # 'g' key to capture a gesture
            print("Capturing gesture...")
            display_text = True  # Reset display
            if (user_score==0 and computer_score==0):
                winner=None
            # Use MediaPipe Gesture Recognizer for user gesture
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            gesture_result = recognizer.recognize(mp_image)
            user_gesture = get_user_gesture(gesture_result)

            if user_gesture:
                # Computer generates a random choice
                computer_choice = random.choice(choices)
                result = decide_winner(user_gesture, computer_choice)
                if result == "User Wins!":
                    user_score+=1
                elif result == "Computer Wins!":
                    computer_score+=1
                elif result == "Draw":
                    pass
                if user_score==winning_score:
                    print("User Wins the Game!")
                    requests.get("https://maker.ifttt.com/trigger/win/with/key/pM1ozEUO5xiOUE5_g0RXgILQN8aLT3kw2KpVtTp-LRg")
                    user_score=0
                    computer_score=0
                    winner='User'
                elif computer_score==winning_score:
                    print("Computer Wins the Game!")
                    requests.get("https://maker.ifttt.com/trigger/loss/with/key/pM1ozEUO5xiOUE5_g0RXgILQN8aLT3kw2KpVtTp-LRg")
                    user_score=0
                    computer_score=0
                    winner='Computer'

                display_text = True  # Enable display of results

                print(f"User: {user_gesture}, Computer: {computer_choice}, Result: {result}")

        elif key == ord('q'):  # 'q' key to quit the program
            print("Exiting...")
            break

        # Show the frame with landmarks and results
        cv2.imshow('Gesture Recognition Game', frame)

    cap.release()
    cv2.destroyAllWindows()
