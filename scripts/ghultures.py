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

        if random.random() < 0.7:
            time.sleep(3)
            continue

        forward_duration = random.uniform(0.3, 0.7)
        client.hold_key("W", forward_duration)

        time.sleep(random.uniform(0.2, 0.7))

        backward_duration = forward_duration * random.uniform(0.3, 0.7)
        client.hold_key("S", backward_duration)

        time.sleep(random.uniform(0.05, 0.5))

        if random.random() < 0.4:
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
        print("refilling mana")
        client.consume_potion()
        return True

    print("out of potions, teleporting to commons to dc")
    client.teleport_to_commons()
    return False


client = api.Client().register_window()
client.set_active()

while True:
    if not check_mana():
        break;

    print("searching")
    natural_movement()
    print("entered combat")

    client.wait_for_player_turn()

    print("player's turn")
    frenzy_found = client.find_spell("frenzy")
    if frenzy_found:
        client.cast_spell("frenzy")
    
    client.wait_for_player_turn()

    while client.count_enemies() < 2:
        print("waiting for 2nd enemy")
        client.pass_turn()
        client.wait_for_player_turn()

    print("enemy count check passed")

    while not client.find_spell("scarecrow") and client.find_spell("unusable_scarecrow"):
        print("need pip for scarecrow, passing")
        client.pass_turn()
        client.wait_for_player_turn()

    if not client.find_spell("epic") and not client.find_spell("scarecrow"):
        print("somehow, neither epic or scarecrow were found. breaking script")
        break

    client.enchant("scarecrow", "epic")

    while not client.find_spell("enchanted_scarecrow"):
        print("need pip for scarecrow, passing")
        client.pass_turn()
        client.wait_for_player_turn()

    client.cast_spell('enchanted_scarecrow')

    print("waiting for combat to end")
    while not client.is_player_idle():
        time.sleep(3)

print("bot has been terminated (assuming by mana)")


