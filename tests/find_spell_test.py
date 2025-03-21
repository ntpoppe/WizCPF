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

if player.find_spell("epic"):
    print("found epic")

if player.find_spell("scarecrow"):
    print("found scarecrow")

if player.find_spell("enchanted_scarecrow"):
    print("found enchanted scarecrow")