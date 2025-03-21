import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wiz_api import api
import time

n_windows = api.count_windows()
print(f"{n_windows} windows detected")

player = api.Client().register_window()

while not player.is_active():
    print("window not focused, focusing")
    player.set_active()
    if player.is_active():
        print("focused")
        break

rect = player.get_window_rect()
color = (252,146,206)
pos = (152, 559)

while True:
    if player.pixel_matches_color(pos, color):
        print("not in combat")
    else:
        print("in combat")
    time.sleep(3)