import cv2
import mediapipe as mp
import random
import time
import math
from collections import deque

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

class Fruit:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = 30
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        self.alive = True

    def move(self):
        self.y += self.velocity
        if self.y > 480:
            self.alive = False
            return False
        return True

    def draw(self, frame):
        if self.alive:
            cv2.circle(frame, (self.x, self.y), self.radius, self.color, -1)
            cv2.circle(frame, (self.x, self.y), self.radius, (255, 255, 255), 2)  # outline

    def draw_panel(frame, score, missed, max_missed):
        overlay = frame.copy()
        alpha = 0.5  # transparency factor
    
        # rectangle coords: top-left and bottom-right
        cv2.rectangle(overlay, (5, 5), (220, 100), (50, 50, 50), -1)
    
        # blend with original frame
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    
        # Draw text on top of panel
        cv2.putText(frame, f"Score: {score}", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, f"Missed: {missed}/{max_missed}", (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 100, 255), 2)

fruits = []
score = 0
missed = 0
max_missed = 5
last_spawn_time = time.time()
hand_trails = deque(maxlen=15)
paused = False
game_over = False
base_velocity = 5


def reset_game():
    global fruits, score, missed, game_over, base_velocity
    fruits = []
    score = 0
    missed = 0
    game_over = False
    base_velocity = 5
    hand_trails.clear()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows fix
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to capture video")
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if not paused and not game_over:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        curr_x, curr_y = None, None
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                x = int(handLms.landmark[8].x * w)
                y = int(handLms.landmark[8].y * h)
                curr_x, curr_y = x, y
                hand_trails.append((x, y))
                cv2.circle(frame, (x, y), 10, (255, 0, 255), -1)

        # Increase speed after every 10 points
        base_velocity = 5 + (score // 10)

        if time.time() - last_spawn_time > 1.0:
            new_fruit = Fruit(random.randint(50, w - 50), 0, velocity=random.randint(base_velocity, base_velocity + 2))
            fruits.append(new_fruit)
            last_spawn_time = time.time()

        updated_fruits = []
        for fruit in fruits:
            still_on_screen = fruit.move()
            fruit.draw(frame)

            if curr_x is not None and fruit.alive:
                distance = math.hypot(fruit.x - curr_x, fruit.y - curr_y)
                if distance < fruit.radius + 10:
                    fruit.alive = False
                    score += 1
                    cv2.putText(frame, "SLICED!", (fruit.x - 30, fruit.y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 2)

            if fruit.alive:
                updated_fruits.append(fruit)
            elif not still_on_screen:
                missed += 1

        fruits = updated_fruits

        for i in range(1, len(hand_trails)):
            cv2.line(frame, hand_trails[i - 1], hand_trails[i], (255, 255, 0), 2)

        cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, f"Missed: {missed}/{max_missed}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 100, 255), 2)
        cv2.putText(frame, f"Speed: {base_velocity}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 255), 2)

        if missed >= max_missed:
            game_over = True

    elif game_over:
        cv2.putText(frame, "GAME OVER", (180, 200), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 0, 255), 4)
        cv2.putText(frame, f"Final Score: {score}", (200, 260), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(frame, "Press R to Restart or Q to Quit", (120, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    else:
        cv2.putText(frame, "PAUSED", (230, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (200, 200, 0), 3)
        cv2.putText(frame, "Press P to Resume", (180, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Fruit Ninja (Gesture Enhanced)", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('p'):
        paused = not paused
    elif key == ord('r') and game_over:
        reset_game()

hands.close()
cap.release()
cv2.destroyAllWindows()
