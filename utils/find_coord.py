import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pyautogui
import time
from wiz_api import api 

COUNT = 5

for i in range(COUNT):
    print(i)
    time.sleep(1)

player = api.Client().register_window()
rect = player.get_window_rect()

x, y = pyautogui.position()
true_x = x - rect[0]
true_y = y - rect[1]

print(f"Cursor Position: ({true_x}, {true_y})")
