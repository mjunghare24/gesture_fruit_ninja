# Gesture-Controlled Fruit Ninja Game

This project is a **Fruit Ninja** style game that can be controlled using hand gestures. Using **OpenCV** and **MediaPipe**, the game detects your hand movements in real time via webcam, and allows you to "slice" fruits as they fall from the top of the screen. The faster and more accurate the swipe, the more fruits you can slice!

## Features
- Real-time hand gesture recognition using **MediaPipe**.
- Fruits appear randomly and fall from the top of the screen.
- Slice fruits by making a quick swipe gesture with your hand.
- Game ends when a fruit falls below the screen without being sliced.

## Requirements

To run this game, you need Python and the following Python libraries:

- **OpenCV**: For computer vision and webcam integration.
- **MediaPipe**: For hand tracking and gesture detection.

You can install the dependencies using pip:

```bash
pip install opencv-python mediapipe
How to Play
Run the game by executing the Python script main.py.

The game will open a webcam window that will detect your hand movements.

Swipe your hand across the screen to slice the falling fruits.

The goal is to slice as many fruits as possible before they fall off the screen.

How to Run
Clone or download the repository to your local machine.

Install the necessary dependencies using the following command:

bash
Copy
Edit
pip install opencv-python mediapipe
Run the game using the command:

bash
Copy
Edit
python main.py
The game window will open, and you can start playing!

Troubleshooting
If the game is not detecting your hand gestures correctly, make sure you're in a well-lit environment and your hand is clearly visible to the webcam.

The webcam resolution might affect the performance. Lowering the resolution can help if the game is running slowly.

License
This project is open-source and available under the MIT License.
