import pyautogui
import math
import numpy as np

pyautogui.FAILSAFE = False

class ActionController:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.cam_w = 640
        self.cam_h = 480
        
        # Tighter borders so you don't have to stretch to the edges
        self.frame_r_x = 120  
        self.frame_r_y = 140  
        
        # Lowered smoothening for snappier, more aligned response
        self.smoothening = 4  
        
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        self.prev_y = 0

    def move_mouse(self, x1, y1):
        # Map the new, smaller camera box to your full screen resolution
        x3 = np.interp(x1, (self.frame_r_x, self.cam_w - self.frame_r_x), (0, self.screen_w))
        y3 = np.interp(y1, (self.frame_r_y, self.cam_h - self.frame_r_y), (0, self.screen_h))
        
        self.clocX = self.plocX + (x3 - self.plocX) / self.smoothening
        self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening
        
        pyautogui.moveTo(self.clocX, self.clocY)
        self.plocX, self.plocY = self.clocX, self.clocY

    def click(self, x1, y1, x2, y2):
        length = math.hypot(x2 - x1, y2 - y1)
        if length < 40:
            pyautogui.click()
            return True
        return False

    def scroll(self, y_current):
        if self.prev_y == 0:
            self.prev_y = y_current
            return
        
        diff = self.prev_y - y_current
        if abs(diff) > 10:  
            pyautogui.scroll(int(diff) * 25) 
            self.prev_y = y_current