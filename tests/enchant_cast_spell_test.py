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

found_epic = player.find_spell("epic")
found_scarecrow = player.find_spell("scarecrow")

if not found_epic:
    print("couldn't find epic")

if not found_scarecrow:
    print("couldn't find scarecrow")

if found_epic and found_scarecrow:
    player.enchant("scarecrow", "epic")
    player.cast_spell("enchanted_scarecrow")