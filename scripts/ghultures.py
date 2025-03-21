import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wiz_api import api
import time
import random

def natural_movement(interations: int = 100) -> None:
    """
    Attempts to simulate natural-looking movement by alternating forward/backward and sometime left/right
    Also attempts to ensure net movement is minimal
    """
    last_direction: str = None
    for _ in range(interations):
        if not client.is_player_idle():
            return

        if random.random() < 0.5:
            time.sleep(3)
            continue

        forward_duration = random.uniform(0.8, 1.2)
        client.hold_key("W", forward_duration)

        time.sleep(random.uniform(0.5, 1.2))

        backward_duration = forward_duration * random.uniform(0.9, 1.1)
        client.hold_key("S", backward_duration)

        time.sleep(random.uniform(0.2, 0.5))

        if random.random() < 0.25:
            if last_direction is None:
                lateral_key = random.choice(['A', 'D'])
            else:
                lateral_key = 'A' if last_direction == 'D' else 'D'

            last_direction = lateral_key
            lateral_duration = random.uniform(0.1, 0.2)
            client.hold_key(lateral_key, lateral_duration)
            time.sleep(random.uniform(0.2, 0.5))

def check_mana() -> bool:
    if not client.is_mana_low():
        return True

    if client.has_potion():
        client.consume_potion()
        return True

    client.teleport_to_commons()
    return False


client = api.Client().register_window()
client.set_active()

while True:
    if not check_mana():
        break;

    natural_movement()
    print("entered combat")

    client.wait_for_player_turn()

    print("player's turn")
    frenzy_found = client.find_spell("frenzy")
    if frenzy_found:
        client.cast_spell("frenzy")
    
    client.wait_for_player_turn()

    while client.count_enemies < 2:
        client.pass_turn()
        client.wait_for_player_turn()

    epic = client.find_spell("epic")
    scarecrow = client.find_spell("scarecrow")
    if epic and scarecrow:
        client.enchant("scarecrow", "epic")
        client.cast_spell('enchanted_scarecrow')

    while not client.is_player_idle():
        print("waiting for combat to end")
        time.sleep(3)

print("bot has been terminated (assuming by mana)")


