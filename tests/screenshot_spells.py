import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pyautogui
import time
from wiz_api import api 

n_windows = api.count_windows()
print(f"{n_windows} windows detected")

player = api.Client().register_window()

while not player.is_active():
    print("window not focused, focusing")
    player.set_active()
    if player.is_active():
        print("focused")
        break

player.screenshot("test_enemy.png", region=player._enemy_area)