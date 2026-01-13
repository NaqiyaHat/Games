#THE LIFT THAT LIES
import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

SAVE_FILE = "save.json"

@dataclass
class Player:
    floor: int = 0
    hp: int = 3
    inventory: List[str] = None
    flags: Dict[str, bool] = None

    def __post_init__(self):
        if self.inventory is None:
            self.inventory = []
        if self.flags is None:
            self.flags = {}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause(msg="Press Enter..."):
    input(msg)

def save_game(p: Player):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(asdict(p), f, indent=2)

def load_game() -> Optional[Player]:
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    p = Player()
    p.floor = data.get("floor", 0)
    p.hp = data.get("hp", 3)
    p.inventory = data.get("inventory", [])
    p.flags = data.get("flags", {})
    return p

def choice(prompt: str, options: Dict[str, str]) -> str:
    while True:
        print(prompt)
        for k, v in options.items():
            print(f"  [{k}] {v}")
        ans = input("> ").strip().lower()
        if ans in options:
            return ans
        print("Invalid choice. Try again.\n")

def header(p: Player):
    print("=" * 54)
    print(f"THE LIFT THAT LIES  |  Floor: {p.floor}  HP: {p.hp}  Inv: {p.inventory}")
    print("=" * 54)

def damage(p: Player, amt: int, reason: str):
    p.hp -= amt
    print(f"\nOuch: -{amt} HP ({reason}).")
    if p.hp <= 0:
        print("\nYour vision fades. The lift hums like it’s satisfied.")
        print("ENDING: The Building Keeps You.\n")
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        pause()
        raise SystemExit

def add_item(p: Player, item: str):
    if item not in p.inventory:
        p.inventory.append(item)
        print(f"\nYou obtained: {item}")

def scene_0(p: Player):
    header(p)
    print("You wake up in a silent lift. No buttons. Only a keypad (0-9).")
    print("A tiny speaker whispers: 'Choose a floor. Choose wrong, repeat.'\n")
    c = choice("What do you do?", {
        "1": "Look for a hidden panel",
        "2": "Punch random floor code (e.g., 7)",
        "3": "Try '0' (ground?)",
        "s": "Save game",
        "q": "Quit"
    })
    if c == "1":
        add_item(p, "small screwdriver")
        p.flags["panel_found"] = True
        p.floor = 1
    elif c == "2":
        damage(p, 1, "The lift jolts and bites your fingers (yes, bites).")
        p.floor = 1
    elif c == "3":
        p.floor = 2
    elif c == "s":
        save_game(p)
        print("\nSaved.")
        pause()
    elif c == "q":
        raise SystemExit

def scene_1(p: Player):
    header(p)
    print("Floor 1: The lights flicker. A note is taped to the mirror:")
    print("'TRUTH OPENS DOORS. LIES OPEN TRAPS.'\n")
    c = choice("The lift door is locked. There’s a voice prompt:", {
        "t": "Say: 'I am afraid.' (truth)",
        "l": "Say: 'I am in control.' (lie)",
        "b": "Break mirror for something sharp",
        "s": "Save",
        "q": "Quit"
    })
    if c == "t":
        print("\nThe lock clicks. The lift seems… disappointed.")
        p.flags["truth_1"] = True
        p.floor = 3
    elif c == "l":
        print("\nThe keypad flashes red. A thin gas hisses out.")
        damage(p, 1, "You inhale panic.")
        p.floor = 1
    elif c == "b":
        add_item(p, "glass shard")
        damage(p, 1, "You cut your hand.")
        p.floor = 3
    elif c == "s":
        save_game(p); print("\nSaved."); pause()
    elif c == "q":
        raise SystemExit

def scene_2(p: Player):
    header(p)
    print("Floor 2: The lift plays a cheerful jingle. Too cheerful.")
    print("A slot opens: 'PAYMENT REQUIRED'.\n")
    if "coin" not in p.inventory:
        print("You notice a loose tile in the corner.")
    c = choice("What now?", {
        "p": "Pry the loose tile",
        "k": "Kick the slot",
        "0": "Try the '0' code again",
        "s": "Save",
        "q": "Quit"
    })
    if c == "p":
        if "small screwdriver" in p.inventory or "glass shard" in p.inventory:
            add_item(p, "coin")
            print("The slot now expects payment.")
        else:
            damage(p, 1, "You strain your fingers pulling the tile.")
    elif c == "k":
        damage(p, 1, "The slot shocks you for disrespect.")
    elif c == "0":
        p.floor = 4
    elif c == "s":
        save_game(p); print("\nSaved."); pause()
    elif c == "q":
        raise SystemExit

def scene_3(p: Player):
    header(p)
    print("Floor 3: A keypad asks a riddle:")
    print("  'I speak without a mouth and hear without ears.'")
    print("  'I have no body, but I come alive with wind.'\n")
    c = choice("Answer?", {
        "e": "echo",
        "f": "fire",
        "s": "save",
        "q": "quit"
    })
    if c == "e":
        print("\nCorrect. The lift purrs. A panel slides open.")
        add_item(p, "keycard")
        p.flags["riddle_ok"] = True
        p.floor = 4
    elif c == "f":
        damage(p, 1, "Wrong. The lift screams (somehow).")
        p.floor = 1
    elif c == "s":
        save_game(p); print("\nSaved."); pause()
    elif c == "q":
        raise SystemExit

def scene_4(p: Player):
    header(p)
    print("Floor 4: A final door. It has a keycard reader and a message:")
    print("'ONLY THOSE WHO PAID MAY LEAVE.'\n")

    can_exit = ("keycard" in p.inventory) and ("coin" in p.inventory or p.flags.get("truth_1", False))
    c = choice("What do you do?", {
        "u": "Use keycard",
        "o": "Offer coin",
        "t": "Tell the truth: 'I don’t know if I deserve to leave.'",
        "s": "Save",
        "q": "Quit"
    })

    if c == "u":
        if "keycard" in p.inventory:
            if can_exit:
                print("\nThe door opens. Cold air. Real air.")
                print("ENDING: You Escape.\n")
                if os.path.exists(SAVE_FILE):
                    os.remove(SAVE_FILE)
                pause()
                raise SystemExit
            else:
                print("\nDenied. The building wants one more thing.")
                damage(p, 1, "The reader burns your thumb.")
        else:
            print("\nYou don’t have a keycard.")
    elif c == "o":
        if "coin" in p.inventory:
            print("\nThe slot accepts it. A green light appears.")
            p.flags["paid"] = True
        else:
            print("\nNo coin to offer.")
    elif c == "t":
        print("\nThe speaker goes quiet. Then: 'Accepted.'")
        print("ENDING: The Building Lets You Go (Barely).\n")
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        pause()
        raise SystemExit
    elif c == "s":
        save_game(p); print("\nSaved."); pause()
    elif c == "q":
        raise SystemExit

def main():
    clear()
    print("THE LIFT THAT LIES\n")
    p = load_game()
    if p:
        ans = input("Found a save. Continue? (y/n): ").strip().lower()
        if ans != "y":
            p = Player()
    else:
        p = Player()

    while True:
        clear()
        if p.floor == 0:
            scene_0(p)
        elif p.floor == 1:
            scene_1(p)
        elif p.floor == 2:
            scene_2(p)
        elif p.floor == 3:
            scene_3(p)
        else:
            scene_4(p)

if __name__ == "__main__":
    main()
