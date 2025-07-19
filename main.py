import cv2
import mediapipe as mp
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load piano sounds
white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
black_keys = ['Cb', 'Eb', 'Fb', 'Gb', 'Bb']  # Using flats, but you can rename as needed

all_keys = white_keys + black_keys
sounds = {k: pygame.mixer.Sound(f'sounds/{k}.wav') for k in all_keys}
key_width = 120  # Width of each white key
# Keep track of last key to prevent rapid replay
last_key = None
key_touched = False

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

# Original (Left) Keyboard
white_key_regions_left = [(i * key_width, (i + 1) * key_width) for i in range(7)]
black_key_map = {
    0: 'Cb',
    1: 'Eb',
    3: 'Fb',
    4: 'Gb',
    5: 'Bb',
}
black_key_regions_left = {
    i: ((x2 - 40, x2 + 40)) for i, (x1, x2) in enumerate(white_key_regions_left) if i in black_key_map
}

# Duplicate (Right) Keyboard
keyboard_offset = 7 * key_width  # = 560 if key_width = 80

white_key_regions_right = [(x1 + keyboard_offset, x2 + keyboard_offset) for (x1, x2) in white_key_regions_left]
black_key_regions_right = {
    i: (x1 + keyboard_offset, x2 + keyboard_offset) for i, (x1, x2) in black_key_regions_left.items()
}

# Webcam
cap = cv2.VideoCapture(0)

def draw_piano_keys(frame, white_left, white_right, black_left, black_right, key_width):
    # draw each key

    # Draw white keys - both keyboards
    for regions in [white_key_regions_left, white_key_regions_right]:
        for i, (x1, x2) in enumerate(regions):
            key = white_keys[i]
            cv2.rectangle(frame, (x1, 400), (x2, 600), (255, 255, 255), -1)
            cv2.rectangle(frame, (x1, 400), (x2, 600), (0, 0, 0), 2)
            cv2.putText(frame, key, (x1 + 10, 590), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Draw black keys - both keyboards
    for regions in [black_key_regions_left, black_key_regions_right]:
        for i, (x1, x2) in regions.items():
            key = black_key_map[i]
            cv2.rectangle(frame, (x1, 400), (x2, 530), (0, 0, 0), -1)
            cv2.putText(frame, key, (x1 + 2, 525), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


def detect_finger_press(x, y):
    global last_key, key_touched

    if 400 < y < 600:
        # Try black keys first (left and right)
        for regions in [black_key_regions_left, black_key_regions_right]:
            for i, (x1, x2) in regions.items():
                if x1 < x < x2 and y < 530:
                    key = black_key_map[i]
                    if key != last_key:
                        print(f"🎵 {key} note played (black key)")
                        sounds[key].play()
                        last_key = key
                        key_touched = True
                    return

        # Then white keys (left and right)
        for regions in [white_key_regions_left, white_key_regions_right]:
            for i, (x1, x2) in enumerate(regions):
                if x1 < x < x2:
                    key = white_keys[i]
                    if key != last_key:
                        print(f"🎵 {key} note played (white key)")
                        sounds[key].play()
                        last_key = key
                        key_touched = True
                    return

    



while True:
    success, frame = cap.read()
    key_touched = False
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape  # get actual frame width

    key_width = w // 14  # 14 total white keys (2 keyboards of 7 each)
    keyboard_start_x = (w - (key_width * 14)) // 2

    # Recalculate key regions based on screen width
    white_key_regions_left = [(keyboard_start_x + i * key_width, keyboard_start_x + (i + 1) * key_width) for i in range(7)]
    white_key_regions_right = [(x1 + 7 * key_width, x2 + 7 * key_width) for (x1, x2) in white_key_regions_left]

    black_key_map = {
        0: 'Cb',
        1: 'Eb',
        3: 'Fb',
        4: 'Gb',
        5: 'Bb',
    }
    black_key_regions_left = {
        i: ((x2 - key_width // 3, x2 + key_width // 3)) for i, (x1, x2) in enumerate(white_key_regions_left) if i in black_key_map
    }
    black_key_regions_right = {
        i: (x1 + 7 * key_width, x2 + 7 * key_width) for i, (x1, x2) in black_key_regions_left.items()
    }
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    draw_piano_keys(
    frame,
    white_key_regions_left,
    white_key_regions_right,
    black_key_regions_left,
    black_key_regions_right,
    key_width
)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            
            


            for tip_index in [8, 12, 20]:  # Index, Middle, Pinky fingertips
                finger = hand.landmark[tip_index]
                x = int(finger.x * w)
                y = int(finger.y * h)
                cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
                detect_finger_press(x, y)
    

    cv2.imshow("Virtual Piano - Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
