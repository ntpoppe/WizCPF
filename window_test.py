import wiz_api.api as api
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
print(f"left x-coord: {rect[0]}, top y-coord: {rect[1]}, width: {rect[2]} height: {rect[3]}")
