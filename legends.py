import random
import json

def create_character():
    name = input("Enter your hero's name: ").strip()

    while name == "":
        print("Please enter a name.")
        name = input("Enter your hero's name: ").strip()

    print("\nChoose your class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer")
    print("4. Assassin")

    classes = {
        "1": {
            "class": "Warrior",
            "hp": 150,
            "mana": 40,
            "attack": 18,
            "defense": 15,
            "crit_chance": 5,
            "max_hp": 150,
            "potions": 2,
            "mana_potions": 2,
            "max_mana": 40
        },
        "2": {
            "class": "Mage",
            "hp": 100,
            "mana": 120,
            "attack": 22,
            "defense": 6,
            "crit_chance": 10,
            "max_hp": 150,
            "potions": 2,
            "mana_potions": 2,
            "max_mana": 120
        },
        "3": {
            "class": "Archer",
            "hp": 115,
            "mana": 70,
            "attack": 15,
            "defense": 9,
            "crit_chance": 20,
            "max_hp": 150,
            "potions": 2,
            "max_mana": 70,
            "mana_potions": 2
        },
        "4": {
            "class": "Assassin",
            "hp": 90,
            "mana": 80,
            "attack": 20,
            "defense": 5,
            "crit_chance": 30,
            "max_hp": 150,
            "potions": 2,
            "mana_potions": 2,
            "max_mana": 80
        }
    }

    while True:
        choice = input("Enter 1, 2, 3, or 4: ").strip()

        if choice in classes:
            character = classes[choice]
            character["name"] = name
            character["level"] = 1
            character["experience"] = 0
            character["experience_to_next_level"] = 100
            character["gold"] = 0
            character["bosses_defeated"] = []

            print(f"\n{name} the {character['class']} is ready!")
            print(character)
            return character

        print("Invalid choice. Please choose 1, 2, 3, or 4.")


def create_enemy(player_level):
    enemies = [
        {"name": "Goblin", "hp": 50, "attack": 10, "defense": 5,
         "experience_reward": 20, "gold_reward": 10},
        {"name": "Wolf", "hp": 40, "attack": 10, "defense": 4,
         "experience_reward": 18, "gold_reward": 8},
        {"name": "Slime", "hp": 35, "attack": 8, "defense": 3,
         "experience_reward": 15, "gold_reward": 5},
        {"name": "Skeleton", "hp": 55, "attack": 9, "defense": 4,
         "experience_reward": 25, "gold_reward": 12},
        {"name": "Zombie", "hp": 65, "attack": 9, "defense": 5,
         "experience_reward": 28, "gold_reward": 15}
    ]

    enemy = random.choice(enemies)

    # Increase enemy stats a little as the player levels up.
    level_bonus = player_level - 1
    enemy["hp"] += level_bonus * 5
    enemy["attack"] += level_bonus
    enemy["defense"] += level_bonus // 2

    print(f"\nA {enemy['name']} appears!")
    print(f"{enemy['name']} HP: {enemy['hp']}  Attack: {enemy['attack']}")
    return enemy


def create_boss(level):
    bosses = {
        10: "Goblin King",
        20: "Forest Guardian",
        30: "Ancient Golem",
        40: "Vampire Lord",
        50: "Dragon Rider",
        60: "Demon General",
        70: "Ice Titan",
        80: "Shadow Emperor",
        90: "Celestial Dragon",
        100: "Ancient Demon King"
    }

    name = bosses[level]

    boss = {
        "name": name,
        "hp": 150 + level * 10,
        "attack": 15 + level,
        "defense": 5 + level // 5,
        "experience_reward": 100 + level * 5,
        "gold_reward": 50 + level * 3
    }

    print(f"\nBOSS BATTLE! {boss['name']} appears!")
    print(f"HP: {boss['hp']} | Attack: {boss['attack']}")
    return boss


def level_up(player):
    if player["level"] >= 100:
        return
    
    player["level"] += 1
    player["max_hp"] += 20
    player["hp"] = min(player["hp"] + 20,player["max_hp"])
    player["max_mana"] += 10
    player["mana"] = min(player["mana"] + 10, player["max_mana"])
    player["attack"] += 2
    player["defense"] += 1
    print(f"\nLevel up! You are now level {player['level']}.")
    print(f"HP: {player['hp']}/{player['max_hp']} | Mana: {player['mana']}/{player['max_mana']}")
    print(f"Attack: {player['attack']} | Defense: {player['defense']}")


bosses = {
    10: "Goblin King",
    20: "Forest Guardian",
    30: "Ancient Golem",
    40: "Vampire Lord",
    50: "Dragon Rider",
    60: "Demon General",
    70: "Ice Titan",
    80: "Shadow Emperor",
    90: "Celestial Dragon",
    100: "Ancient Demon King"
}

class_skills = {
    "Warrior": {"name": "Power Strike", "mana_cost": 10, "damage": 30},
    "Mage": {"name": "Fireball", "mana_cost": 15, "damage": 40},
    "Archer": {"name": "Precise Shot", "mana_cost": 10, "damage": 25},
    "Assassin": {"name": "Backstab", "mana_cost": 12, "damage": 35}
}

def save_game(player):
    with open("save_game.json", "w") as file:
        json.dump(player, file, indent=4)

    print("Game saved.")

def show_stats(player):
    print("\n--- Character Stats ---")
    print(f"Name: {player['name']}")
    print(f"Class: {player['class']}")
    print(f"Level: {player['level']}")
    print(f"Experience: {player['experience']}")
    print(f"HP: {player['hp']}/{player['max_hp']}")
    print(f"Mana: {player['mana']}/{player['max_mana']}")
    print(f"Attack: {player['attack']}")
    print(f"Defense: {player['defense']}")
    print(f"Critical chance: {player['crit_chance']}%")
    print(f"Gold: {player['gold']}")
    print(f"Health potions: {player['potions']}")
    print(f"Mana potions: {player['mana_potions']}")
    print(f"Bosses defeated: {len(player['bosses_defeated'])}")

def battle(player, enemy):
    print(f"\nBattle started: {player['name']} vs. {enemy['name']}!")

    defending = False

    while player["hp"] > 0 and enemy["hp"] > 0:
        print(f"\nYour HP: {player['hp']}/{player['max_hp']} |  Mana: {player['mana']}/{player['max_mana']} | Health potions: {player['potions']}"
              f"| Mana potions: {player['mana_potions']}  | {enemy['name']} HP: {enemy['hp']}")
        action = input("Choose: (a).attack,(s).skill,(d).defend,(h).heal,(m).mana potion,(v).view stats, or (q).quit: ").strip().lower()
        if action == "q":
            print("You ran away from the  battle.You recieve no rewards!")
            return
        elif action == "d":
            defending = True
            print("You defend. The next enemy attack will be reduced.")
        elif action == "a":  # Player attacks
            damage = max(1, player["attack"] - enemy["defense"])
            if random.randint(1, 100) <= player["crit_chance"]:
                damage *= 2
                print("Critical hit!")

            enemy["hp"] -= damage
            print(f"You hit the {enemy['name']} for {damage} damage!")
        elif action == "s":
            skill = class_skills[player["class"]]

            if player["mana"] < skill["mana_cost"]:
                print("Not enough mana to use this skill.")
                continue

            damage = max(1, skill["damage"] - enemy["defense"])
            enemy["hp"] -= damage
            player["mana"] -= skill["mana_cost"]

            print(f"You used {skill['name']} and dealt {damage} damage!")
        elif action == "h":
            if player["potions"] <= 0:
                print("You have no health potions.")
            elif player["hp"] >= player["max_hp"]:
                print("Your health is already full.")
            else:
                old_hp = player["hp"]
                player["hp"] = min(player["hp"] + 50, player["max_hp"])
                healed = player["hp"] - old_hp
                player["potions"] -= 1
                print(f"You restored {healed} HP.") 
        elif action == "m":
            if player["mana_potions"] == 0:
                print("You have no mana potions.")
            elif player["mana"] == player["max_mana"]:
                print("Your mana is already full.")
            else:
                old_mana = player["mana"]
                player["mana"] = min(player["mana"] + 30,player["max_mana"])
                mana_restored = player["mana"] - old_mana
                player["mana_potions"] -= 1
                print(f"You restored {mana_restored} mana.")
        elif action == "v":
            show_stats(player)
            continue
        else:
            print("Choose a,s,m,d,h or q.")
            continue

        # Stop if the enemy was defeated
        if enemy["hp"] <= 0:
            break

        # Enemy attacks
        damage = max(1, enemy["attack"] - player["defense"])
        if defending:
            damage = max(1, damage // 2)
            defending = False

        player["hp"] -= damage
        print(f"The {enemy['name']} hits you for {damage} damage!")

    if player["hp"] <= 0:
        print("You were defeated.")
    else:
        print(f"You defeated the {enemy['name']}!")
        player["experience"] += enemy["experience_reward"]
        player["gold"] += enemy["gold_reward"]
        mana_restored = 10
        player["mana"] = min( player["mana"] + mana_restored,player["max_mana"])
        print(f"You recovered {mana_restored} mana.")
        print(f"You gained {enemy['experience_reward']} EXP and {enemy['gold_reward']} gold.")
        level_up(player)

def start_adventure(player):
    boss_levels = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)

    while player["hp"] > 0:
        player_level = player["level"]

        is_boss = (
            player_level in boss_levels
            and player_level not in player["bosses_defeated"]
        )

        if is_boss:
            enemy = create_boss(player_level)
        else:
            enemy = create_enemy(player["level"])

        battle(player, enemy)

        if is_boss and player["hp"] > 0 and enemy["hp"] <= 0:
            player["bosses_defeated"].append(player_level)
            print(f"Boss at level {player_level} defeated!")

        if player["hp"] <= 0:
            print("Game over!")
            return

        again = input("Look for another enemy? (yes/no): ").strip().lower()

        if again != "yes":
            save_game(player)
            print("Your progress is saved.")
            return

def load_game():
    try:
        with open("save_game.json", "r") as file:
            player = json.load(file)

        print(f"Welcome back, {player['name']} the {player['class']}!")
        return player

    except FileNotFoundError:
        print("No saved game was found.")
        return None

def main():
    while True:
        print("\nLEGENDS OF THE FORGOTTEN REALM")
        print("1. New Game")
        print("2. Continue")
        print("3. Instructions")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            player = create_character()
            start_adventure(player)

        elif choice == "2":
            player = load_game()

            if player is not None:
                start_adventure(player)

        elif choice == "3":
            print("\nDefeat enemies to gain experience and gold.")
            print("Use skills and potions during battles.")
            print("Defeat bosses every 10 levels to progress.")

        elif choice == "4":
            print("Thanks for playing!")
            break

        else:
            print("Choose 1, 2, 3, or 4.")

main()