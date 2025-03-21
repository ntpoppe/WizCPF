import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wiz_api import api
import time

player = api.Client().register_window()
player.set_active()
print(f"mana low: {player.is_mana_low()}")
print(f"has potion: {player.has_potion()}")

num = player.count_enemies()
print(num)

player.pass_turn()