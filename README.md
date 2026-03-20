# Vision-Cursor: AI Virtual Mouse

A real-time, gesture-controlled virtual mouse built with Python, computer vision, and deep learning. This project allows users to control their computer's cursor, click, and scroll using hand gestures captured through a standard webcam. It features a lightweight Flask backend and a modern Glassmorphism web UI.

## Features

* **Real-Time Cursor Control**: Move your mouse pointer smoothly by tracking your index finger.
* **Gesture Clicking**: Execute left-clicks by pinching your index and middle fingers together.
* **Vertical Scrolling**: Scroll through web pages and documents by raising three fingers and moving your hand up or down.
* **Background Processing**: The AI tracking runs on a separate background thread, allowing the controller to work seamlessly even when the dashboard is minimized or closed.
* **Modern Dashboard UI**: A sleek, dark-mode web interface to monitor your camera feed and active tracking area.

## Tech Stack

* **Backend**: Python, Flask
* **Computer Vision**: OpenCV, Google MediaPipe (Tasks API)
* **Automation**: PyAutoGUI, NumPy
* **Frontend**: HTML5, CSS3, JavaScript

## Installation

1. Clone the repository:
   git clone https://github.com/Nimalan07/Vision-Cursor.git
   cd Vision-Cursor

2. Install the required dependencies:
   pip install -r requirements.txt

3. Run the application:
   python app.py

4. Open your browser and navigate to `http://127.0.0.1:5000`

## How to Use (Gestures)

The application maps a defined center region of your camera feed to your entire screen resolution for ergonomic control.

* **Move Mouse**: Raise only your **Index Finger**. Move it within the center frame to move the cursor.
* **Left Click**: Raise both your **Index Finger and Middle Finger**. Bring your thumb close to your index finger to trigger a click.
* **Scroll**: Raise your **Index, Middle, and Ring Fingers**. Move your hand vertically to scroll.

## Folder Structure
```
├── app.py                  
├── core/
│   ├── __init__.py
│   ├── hand_tracker.py     
│   └── action_controller.py
├── static/
│   └── css/
│       └── style.css       
├── templates/
│   └── index.html          
├── requirements.txt        
└── .gitignore
```