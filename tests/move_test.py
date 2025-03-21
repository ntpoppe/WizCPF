import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wiz_api import api
import time

player = api.Client().register_window()
player.set_active()

player.hold_key("W", 1)
time.sleep(0.5)
player.hold_key("S", 1)

