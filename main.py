import random

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create black magic
fire = Spell("Fire", 10, 250, "black")
thunder = Spell("Thunder", 25, 500, "black")
blizzard = Spell("Blizzard", 15, 300, "black")
meteor = Spell("Meteor", 20, 1200, "black")
quake = Spell("Quake", 12, 400, "black")
ultimate = Spell("Ultimate", 50, 5000, "black")

# Create white magic
cure = Spell("Cure", 12, 600, "white")
cura = Spell("Cura", 18, 1000, "white")
curaga = Spell("Curaga", 50, 6000, "white")

# Create Some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("MegaElixir", "elixir", "Fully restores party`s HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 100)

player_spell = [fire, thunder, blizzard, meteor, quake, ultimate, cure, cura, curaga]

enemy_spell = [fire, meteor, quake, cure]

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2}, {"item": elixir, "quantity": 1},
                {"item": hielixir, "quantity": 1}, {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Ognikus: ", 3200, 300, 150, 34, player_spell, player_items)
player2 = Person("Eren   : ", 4300, 400, 250, 34, player_spell, player_items)
player3 = Person("Kiborg : ", 6000, 600, 500, 34, player_spell, player_items)

enemy1 = Person("Imp:   ", 1250, 130, 560, 325, enemy_spell, [])
enemy2 = Person("Dragon: ", 12200, 701, 215, 25, enemy_spell, [])
enemy3 = Person("imp:   ", 1250, 130, 560, 325, enemy_spell, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
# Start game
while running:
    print("=" * 20)

    print("\n\n")
    print("NAME                   HP                                    MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        # Standard attack
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name + "for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
        # Magic attack
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("   Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            # Heal player
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBlUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)

            # Damage enemy
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBlUE + "\n" + spell.name + ' deals', str(magic_dmg),
                      "points of damage " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        # Use items
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left...." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + "fully restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "point of damage" + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    print("\n")
    # Enemy attack phase
    for enemy in enemies:

        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Shose attack
            target = random.randrange(0, 2)
            enemy_damage = enemy.generate_damage()

            players[target].take_damage(enemy_damage)
            print(enemy.name.replace(" ", "") + " attack " + players[target].name.replace(" ", "") + " for",
                  enemy_damage)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            # Heal player
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBlUE + spell.name + " heals " + enemy.name + " for", str(magic_dmg),
                      "HP." + bcolors.ENDC)

            # Damage enemy
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBlUE + "\n" + enemy.name.replace(" ", "") + "`s " + spell.name + ' deals',
                      str(magic_dmg),
                      "points of damage " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]

            # print("Enemy chose", spell, "damage is", magic_dmg)

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    # Check if Enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

    print(defeated_enemies)
