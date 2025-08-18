import cv2
import mediapipe as mp
import time
import pyttsx3

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.say(  "HELLO , VIEWERS , HOW ARE YOU, I AM ATHEXRECOX , A SIGN MODEL  MADE BY DEBESH ")
engine.say(  "LOOK STRAIGHT INTO THE CAMERA FOR BETTER CAPTURE ")
engine.runAndWait()
# Setup MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Start webcam
cap = cv2.VideoCapture(0)

# Store the last spoken gesture to avoid repetition
last_gesture = ""
last_spoken_time = time.time()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_finger_status(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]
    finger_pips = [2, 6, 10, 14, 18]

    fingers_up = []

    # Thumb: compare x for right hand
    if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_pips[0]].x:
        fingers_up.append(True)
    else:
        fingers_up.append(False)

    # Other fingers: compare y
    for i in range(1, 5):
        if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_pips[i]].y:
            fingers_up.append(True)
        else:
            fingers_up.append(False)

    return fingers_up

def detect_gesture(fingers_up):
    if  fingers_up ==[False,False,True,False,False]:
        return "fuck off"
    elif fingers_up == [True, False, False, False, False]:
        return "Thumbs Up"
    elif fingers_up == [ False,True,True, False, False ]:
        return "Say Cheese"
    elif fingers_up == [False, True, True, True,True]:
        return "FOUR"
    elif all(fingers_up):
        return "chal chal chal"
    else:
        return None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)
    gesture = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_up = get_finger_status(hand_landmarks)
            gesture = detect_gesture(fingers_up)

            if gesture:
                cv2.putText(frame, f"{gesture}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

                # Speak only if it's a new gesture and enough time has passed
                if gesture != last_gesture or time.time() - last_spoken_time > 3:
                    speak(gesture)
                    last_gesture = gesture
                    last_spoken_time = time.time()

    cv2.imshow("ATHEX RECOX SIGN SIGNALS", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()