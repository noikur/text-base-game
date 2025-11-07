import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Character:
    def __init__(self, name, hp, attack, defence, crit_dam =2.0, crit_chance =0.2, crit_miss=0.05, miss=0.1, weapon =None):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.max_hp = hp
        self.potion = 2
        self.crit_dam = crit_dam
        self.crit_chance = crit_chance
        self.crit_miss = crit_miss
        self.miss = miss
        self.weapon = weapon
        
        self.base_miss = miss
        self.base_crit_miss = crit_miss
        self.status_effects = []

        
    def is_alive(self):
        return self.hp > 0
    


    def take_damage(self, damage):

        damage_taken = max(0, damage - self.defence)
        self.hp -= damage_taken
        print(f"{self.name} takes {damage_taken} damage! HP left: {self.hp}")


    def heal(self):
        if self.potion > 0:
            heal_amount = random.randint(10, 20)
            self.hp = min(self.max_hp, self.hp + heal_amount)
            self.potion -= 1
            print(f"{self.name} heals for {heal_amount} hp is now: {self.hp}. potion left: {self.potion}")
        else:
            print(f"{self.name} you have no potion left")

    def attack_enemy(self, enemy):
        time.sleep(0.5)


        self.miss = self.base_miss
        self.crit_miss = self.base_crit_miss
        
        for effect in self.status_effects:
            if isinstance(effect, Blind):
                self.miss += effect.extra_miss
                self.crit_miss += effect.extra_crit_miss

        roll = random.random()

        crit_chance = self.weapon.crit_chance if self.weapon else self.crit_chance
        crit_dam = self.weapon.crit_dam if self.weapon else self.crit_dam

        base_damage = self.attack
        if self.weapon:
            base_damage += self.weapon.damage

        if roll < self.crit_miss:
            print(f"{self.name} critically miss")
            return
        
        elif roll < self.crit_miss + self.miss :
            print(f"{self.name} misses")
            return
        
        elif roll < self.crit_miss + self.miss + crit_chance :
            damage = base_damage * crit_dam
            print(f"{self.name} lands a CRITICAL HIT")
        else:
            damage = base_damage

        print(f"{self.name} hits {enemy.name} for {int(damage)} damage")
        enemy.take_damage(damage)


    def equip_weapon(self, weapon):
        self.weapon = weapon
        print (f"{self.name} equips {weapon.name}")

class Weapon:
    def __init__(self, name, damage, crit_chance, crit_dam=2.0, price=0):
        self.name = name
        self.damage = damage
        self.crit_chance = crit_chance
        self.crit_dam = crit_dam
        self.price = price



# stage 1 Enemies
stage1_enemies = [
    Character("gobgob", hp=50, attack=10, defence=5),
    Character("starstar", hp=20, attack=20, defence=10),
    Character("ompilompi", hp=40, attack=20, defence=5),
    Character("ogiogi", hp=30, attack=5, defence=10),
    Character("soultryry", hp=50, attack=10, defence=0)
    ]
# bosses
boss = Character("Dajor Zerker", hp= 100, attack= 30, defence= 20)
# weapons
weapons = [
    Weapon("light saber", 10, 0.2, 2.0, 0),
    Weapon("Highblades", 20, 0.25, 2.0, 100),
    Weapon("Stormfield", 30, 0.3, 2.0, 200),
]

#   Characters
player = Character("Hero", hp=100, attack=30, defence=5, weapon=weapons[0])



#Game start screen
def Game_screen():
    print("           welcome to Lost Tais          ")
    print("   _______________     ______________    ")
    print("   |Start Game(z)|     |Load Game(x)|    ")
    print("   _______________     ______________    ")

def game_start():
    while True:
        Game_screen()
        choice = input("Enter Option: ").lower()
        if choice == "z":
            print("A new adventure begins")
            clear_screen()
            break
        elif choice == "x":
            print("Loading your saved game")
            clear_screen()
            break
        else: 
            print("invalid option Please Try Again.")


#Menu screen
def show_menu():
    print("+----------------------+----------------------+")
    print("| {:<20} | {:<20} |".format("MENU SCREEN", ""))
    print("+----------------------+----------------------+")
    print("| 1. Items             | Party                |")
    print("| 2. Skills            | (placeholder)        |")
    print("| 3. Equipment         | (placeholder)        |")
    print("| 4. Formation         | (placeholder)        |")
    print("| 5. Status            | (placeholder)        |")
    print("| 6. Save              | (placeholder)        |")
    print("| 7. End Game          | (placeholder)        |")
    print("|                      |                      |")
    print("|         5000(G)      |     close menu(x)    |")
    print("+----------------------+----------------------+")

def open_menu():
    while True:
        show_menu()
        choice = input("Enter option:").lower()
        if choice == "x":
            break
        else: 
            print("invalid option")

def start_adv():          
    for enemy in stage1_enemies:
        print("Long ago, the great kingdom of Nestar stood as a sanctuary of peace and balance.")
        print("Nature and magic lived in harmony, watched over by wise kings and powerful mages.")
        print("But everything changed the day one of those mages lost his mind...")
        print()
        print("Some say it was power that drove him mad.")
        print("Others whisper he uncovered something—something forbidden—deep within the earth.")
        print("All that’s certain is this: the day the Mad Mage was born, a twisted tower burst from the heart of the forest.")
        print("A black spire, clawing at the skies, pouring corruption into the land like poison.")
        print()
        print(f"This is where you come in, {player.name}.")
        print("tThe prince has chosen You to save his father and take down the Mage.")
        print("Your task is simple, yet perilous: enter the cursed woods, face the twisted creatures within, and end the Mad Mage’s reign before the kingdom is lost forever.")
        print()
        print("The deeper you go, the more the mana of the area changes... and the more it changes you.")
        print("Steel your heart.")
        print("Please SAVE the king, no save the WORLD") 
        print(f"A wild {enemy.name} has shown up")
        print("----------NOTIFICATION-------------")
        print(f"{player.name} your resources have been replenished")
        player.potion = 2
# Mobs
        while player.is_alive() and enemy.is_alive():
            print("-----------YOUR TURN-----------")
            print(f"{player.name} hp:{player.hp} | {enemy.name} hp: {enemy.hp}")
            print(f"| 1. Attack | 2. Heal {player.potion} | 3. Run | 4. Menu |")

            choice = input("choose your action:")
            if choice == "1":
                player.attack_enemy(enemy)
            elif choice == "2":
                player.heal()
            elif choice == "3":
                print("You ran away")
                exit()
            elif choice == "4":
                open_menu()
            else:
                print("invalid option")

            time.sleep(2)

            if not enemy.is_alive():
                print(f"{enemy.name} has lost")
                break

            print("--------Enemy Turn--------")
            enemy_choice = random.choice(["attack", "attack", "heal"])
            if enemy_choice == "attack":
                enemy.attack_enemy(player)
            else:
                enemy.heal()
            time.sleep(1)

#Boss1
    if player.is_alive():
        dazed = False

        print(f"you find a tower and decide to open the big door and what you see is somene of legend {boss.name} stand before you")
        print("----------NOTIFICATION-------------")
        print(f"{player.name} your rescources have been replenished")
        player.potion = 2
        print("-------------STORY-------------")
        print(f"{boss.name}: HAHAHAHAHA... I laugh, but I feel sorry for you. It is unfortunate your journey ends here.")

        while player.is_alive() and boss.is_alive():
            if dazed :
                print(f"{boss.name}: day by day forced to wait up becomes down left becomes right")
                print(f"------YOUR DAZED------")
                dazed = False
            else:
                print("---------YOUR TURN---------")
                print(f"{player.name} hp:{player.hp} | {boss.name} hp: {boss.hp}")
                print(f"| 1. Attack | 2. Heal {player.potion} | 3. Run |")

                choice = input("choose your action:")
                if choice == "1":
                    player.attack_enemy(boss)
                    print(f"{boss.name}: There is no point in trying. You are one of many who have failed.")
                elif choice == "2":
                    player.heal()
                    print(f"{boss.name}: No matter the item you use, you will be defeated.")
                elif choice == "3":
                    print(f"{boss.name}: There is no escape. Either you defy fate, or I set things right.")
                else:
                    print("Invalid option.")


            time.sleep(2)

            if not boss.is_alive():
                print(f"{boss.name}: I see you are the one that we have been waiting for i wish i could of seen it through")
                break
                
            print(f"--------{boss.name} Turn--------")
            boss_choice = random.choice(["attack", "attack", "attack", "heal","daze"])
            if boss_choice == "attack":
                boss.attack_enemy(player)
            elif boss_choice == "daze": #daze effect chance to skip turns 
                print(f"{boss.name} uses dazziling time")
                dazed = True
            else:
                boss.heal()
            time.sleep(1)


if __name__ == "__main__":
    game_start()
    start_adv()

#game over

    print("----- Game Over-----")
    if player.is_alive():
        print("onto the next fight")
    else:
        print("HAHAHAHAHA cough cough i see you couldnt make it ")



class Effect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def apply(self, Character):
        pass

    def update(self, character):
        self.duration -= 1

    def is_expired(self):
        return self.duration <=0 
    
class Poison(Effect):
    def __init__(self, duration = 5):
        super().__init__("Poison", duration)
    def apply(self, character):
        print(f"{character.name} has been poisoned for {self.duration} turns")
    def update(self, character):
        character.hp -= 1
        print(f"{character.name} has suffered 1 poison damage {character.name} has {character.hp} hp left")
        super().update(character)
    def expire(self, character):
        print(f"{character.name} is no longer poisoned")

class Regen(Effect):
    def __init__(self, duration = 5):
        super().__init__("Sleep", duration)
    def apply(self, character):
        print(f"{character.name} has been put to sleep for {self.duration} turns")
    def update(self, character):
        character.hp += 1
        print(f"{character.name} has healed 1 hp {character.name} has {character.hp} hp")
    def is_expired(self, character):
        print(f"{character.name} is no longer regenerating")

class Blind(Effect):
    def __init__(self, duration = 5, extra_crit_miss=0.10, extra_miss=0.2):
        super().__init__("Blind", duration )
        self.extra_miss = extra_miss
        self.extra_crit_miss = extra_crit_miss
    def apply(self, character):
        print(f"{character.name} has been Blinded for {self.duration} turns")
    def update(self, character):
        pass
    def is_expired(self, character):
            print(f"{character.name} is no longer Blinded")

        
