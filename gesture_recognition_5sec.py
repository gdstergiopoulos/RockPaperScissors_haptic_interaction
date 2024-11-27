import cv2
import mediapipe as mp
import time

# Import necessary components from MediaPipe Tasks
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Callback function to handle the gesture recognition results
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if result.gestures:
        print('Gesture recognized:')
        for gesture in result.gestures[0]:  # Top gestures
            print(f'{gesture.category_name}: {gesture.score:.2f}')
    else:
        print('No gesture detected.')

# Set up the options for the Gesture Recognizer
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='./gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result
)

# Initialize the gesture recognizer with the options
with GestureRecognizer.create_from_options(options) as recognizer:

    # Open the webcam feed
    cap = cv2.VideoCapture(0)
    last_recognition_time = 0
    recognition_interval = 5  # seconds

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        # Flip the frame horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert frame to RGB (MediaPipe requires RGB format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Wrap the frame into a MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        current_time = time.time()
        if current_time - last_recognition_time >= recognition_interval:
            # Send the image to the gesture recognizer
            recognizer.recognize_async(mp_image, int(cap.get(cv2.CAP_PROP_POS_MSEC)))
            last_recognition_time = current_time

        # Display the frame in an OpenCV window
        cv2.imshow('Gesture Recognition', frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
