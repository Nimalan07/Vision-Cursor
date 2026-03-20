import os
import logging
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['GLOG_minloglevel'] = '2'
logging.getLogger('tensorflow').setLevel(logging.FATAL)
from flask import Flask, render_template, Response
import cv2
import pyautogui
import threading
import time
from core.hand_tracker import HandTracker
from core.action_controller import ActionController
app = Flask(__name__)
tracker = HandTracker()

screen_w, screen_h = pyautogui.size()
action = ActionController(screen_w, screen_h)

global_frame = None

def background_tracking():
    global global_frame
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    while True:
        success, frame = cap.read()
        if not success:
            continue
        
        frame = cv2.flip(frame, 1)
        frame = tracker.find_hands(frame)
        lm_list = tracker.get_position(frame)
        cv2.rectangle(frame, (action.frame_r_x, action.frame_r_y), 
                      (action.cam_w - action.frame_r_x, action.cam_h - action.frame_r_y), 
                      (255, 0, 255), 2)
        
        if len(lm_list) != 0:
            x1, y1 = lm_list[8][1:]
            x2, y2 = lm_list[12][1:]
            
            fingers = []
            fingers.append(1 if lm_list[8][2] < lm_list[6][2] else 0)
            fingers.append(1 if lm_list[12][2] < lm_list[10][2] else 0)
            fingers.append(1 if lm_list[16][2] < lm_list[14][2] else 0)
            
            if fingers == [1, 0, 0]:
                action.move_mouse(x1, y1)
                action.prev_y = 0
                
            elif fingers == [1, 1, 0]:
                clicked = action.click(x1, y1, x2, y2)
                if clicked:
                    cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                action.prev_y = 0
                    
            elif fingers == [1, 1, 1]:
                action.scroll(y1)
            
        ret, buffer = cv2.imencode('.jpg', frame)
        global_frame = buffer.tobytes()

threading.Thread(target=background_tracking, daemon=True).start()

def generate_frames():
    global global_frame
    while True:
        if global_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n')
        time.sleep(0.03)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=False, threaded=True)