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
idle_color = (252,146,206) # pig
idle_pos = (152, 559) # pig

while player.pixel_matches_color(idle_pos, idle_color):
    print("not in combat")
    time.sleep(3)

print("now in combat")

player_turn_color = (255, 255, 0)
player_turn_pos = (244, 415)

while True:
    if player.pixel_matches_color(player_turn_pos, player_turn_color):
        print("player's turn")
    else:
        print("idle")
    time.sleep(3)