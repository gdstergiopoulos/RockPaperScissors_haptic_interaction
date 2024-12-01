import cv2
import mediapipe as mp
import random

# Initialize MediaPipe Hands and Drawing tools
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Game choices
choices = ["Rock", "Paper", "Scissors"]

def get_user_choice(hand_landmarks):
    # Determine gesture based on finger positions
    # Example logic (simplified):
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:  # Index finger up
        if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y:  # Middle finger up
            return "Scissors"
        else:
            return "Rock"
    else:
        return "Paper"

def decide_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Draw"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Scissors" and computer_choice == "Paper") or \
         (user_choice == "Paper" and computer_choice == "Rock"):
        return "User Wins!"
    else:
        return "Computer Wins!"


cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        user_choice = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                user_choice = get_user_choice(hand_landmarks)
        
       
        if user_choice:
            computer_choice = random.choice(choices)
            result = decide_winner(user_choice, computer_choice)
            cv2.putText(frame, f"User: {user_choice}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f"Computer: {computer_choice}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f"Result: {result}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        
        cv2.imshow("Rock Paper Scissors", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
