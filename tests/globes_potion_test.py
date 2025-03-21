import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wiz_api import api
import time

player = api.Client().register_window()
player.set_active()
print(f"mana low: {player.is_mana_low()}")
print(f"has potion: {player.has_potion()}")

if player.is_mana_low():
    if player.has_potion():
        player.consume_potion()
    else:
        player.teleport_to_commons()
