import cv2
import mediapipe as mp
import random
import time
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Fruit class
class Fruit:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = 30
        self.alive = True

    def move(self):
        self.y += self.velocity
        if self.y > 480:
            self.alive = False

    def draw(self, frame):
        if self.alive:
            cv2.circle(frame, (self.x, self.y), self.radius, (0, 255, 0), -1)

# Game variables
fruits = []
prev_x, prev_y = None, None
last_spawn_time = time.time()

# Main loop
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    curr_x, curr_y = None, None
    swipe = False

    # Hand tracking
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            x = int(handLms.landmark[8].x * w)
            y = int(handLms.landmark[8].y * h)

            curr_x, curr_y = x, y
            cv2.circle(frame, (x, y), 10, (255, 0, 255), -1)

            # Detect swipe
            if prev_x is not None and prev_y is not None:
                dist = math.hypot(curr_x - prev_x, curr_y - prev_y)
                if dist > 40:
                    swipe = True

    # Spawn new fruit every 1.5 seconds
    if time.time() - last_spawn_time > 1.5:
        new_fruit = Fruit(random.randint(50, w - 50), 0, velocity=5)
        fruits.append(new_fruit)
        last_spawn_time = time.time()

    # Update and draw fruits
    for fruit in fruits:
        fruit.move()
        fruit.draw(frame)

        if swipe and fruit.alive and curr_x is not None:
            if abs(fruit.x - curr_x) < fruit.radius and abs(fruit.y - curr_y) < fruit.radius:
                fruit.alive = False
                cv2.putText(frame, "SLICED!", (fruit.x - 20, fruit.y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Remove dead fruits
    fruits = [fruit for fruit in fruits if fruit.alive]

    prev_x, prev_y = curr_x, curr_y

    cv2.imshow("Fruit Ninja (Gesture)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
