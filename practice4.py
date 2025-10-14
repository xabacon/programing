#Imports
import random
import keyboard
import time
import os
import LoreBook
from dataclasses import dataclass
from colorama import Fore, Style

#Upgrades Struct Declaration
@dataclass
class Upgrades:
    name: str
    cost: int
    Dicesides: int
    diceAmount: int
    scoreMultiplier: int
    priceMultiplier: float
    key: str
    
    
#Effects Struct Declaration
@dataclass
class Effects:
    name: str
    chance: int
    effect: int
    effectInterval: float
    duration: float
    ActiveDuration: float
    LastUpdate: float = 0.0

    
#Upgrade Declarations
basic_side_Increase = Upgrades("Basic Side Increase", 10, 1, 0, 1,1.4,"1")
basic_Amount_Increase = Upgrades("Basic Amount Increase", 20, 0, 1, 1,2.8,"2")
basic_Score_Multiplier = Upgrades("Basic Score Multiplier", 50, 0, 0, 2,4.3,"3")
upgrade_list = [basic_side_Increase, basic_Amount_Increase, basic_Score_Multiplier]

    
#Effect Declarations
normal = Effects("Normal", 0, 0, 0,0, 0)
ice = Effects("Ice", 1, 100, 1.0, 3.0, 3.0)
fire = Effects("Fire", 2, 100, 1.0, 3.0, 3.0)
poison = Effects("Poison", 3, 100, 1.0, 3.0, 3.0)
effect_list = [normal,ice, fire, poison]

#Dice Generator Function
def generator():
    return random.randint(0,i)
def effectGenerator():
    return random.randint(0,3)

# clear screen function
def clear_screen():
    if os.name == 'nt':
        os.system('cls')


# effect updater & handler
def update_effects():
    global score, LastUpdate, CurrentEffect
    for effect in effect_list:
        if CurrentEffect == effect and effect != normal:
            now = time.time()
            if now - effect.LastUpdate >= effect.effectInterval:
                score += effect.effect
                effect.ActiveDuration -= effect.effectInterval
                effect.LastUpdate = now
                if effect.ActiveDuration > 0:
                        continue
                else:
                    CurrentEffect = normal
                    print(Fore.MAGENTA + effect.name + " effect has worn off." + Style.RESET_ALL)
                    effect.ActiveDuration = effect.duration


# score line updater
def update_score_line(new_score):
    global CurrentEffect, RollActive, diceSum
    print("\033[1A", end='')
    print("\033[K", end='')
    if RollActive:
        print("You rolled a " + Fore.RED + str(diceSum) + Style.RESET_ALL)
    if CurrentEffect != normal:
        print("your score is: " + Fore.RED + str(new_score) + Style.RESET_ALL + Style.RESET_ALL, flush=True)


# UI Printer
def printUI():
        print("=============================================================")
        print("Press " + Fore.GREEN + "'u'" + Style.RESET_ALL + " to enter Upgrade Screen")
        print("Press " + Fore.GREEN + "'a'" + Style.RESET_ALL + " to toggle advanced view")
        print("=============================================================")
        if AdvancedView == True:
            print("Current Dice sides: " + Fore.RED + str(i) + Style.RESET_ALL)
            print("Current Dice Amount: " + Fore.RED + str(rollAmmount) + Style.RESET_ALL)
            print("Current Score Multiplier: " + Fore.RED + str(scoreMultiplicator) + Style.RESET_ALL)
        print("You rolled a " + Fore.RED + str(diceSum) + Style.RESET_ALL)
        if CurrentEffect == normal:
            print("your score is: " + Fore.RED + str(score) + Style.RESET_ALL, flush=True)
        update_score_line(score)

#main Code
Instructions = True
i = 6
score = 0
scoreMultiplicator = 1
rollAmmount = 1
LastUpdate = time.time()
AdvancedView = False
LoreBookActive = False
CurrentEffect = normal


#game loop
while True:

    RollActive = False
    if CurrentEffect != normal:
        update_effects()
        update_score_line(score)
    if Instructions:
        Instructions = False
        print("Welcome to the dice roller!")
        print("Press " + Fore.GREEN + "'q'" + Style.RESET_ALL + " to quit")
        print("Press " + Fore.GREEN + "'enter'" + Style.RESET_ALL + " to roll the dice")
        print("Press " + Fore.GREEN + "'l'" + Style.RESET_ALL + " to read the Lore")
    if keyboard.is_pressed('q'):
        break
    
    
    # roll dice
    if keyboard.is_pressed('enter'):
        rollerCounter = 0
        diceSum = 0
        clear_screen()
        
        #roll handler
        while (rollerCounter < rollAmmount):
            RollActive = True
            dice = generator()
            for effect in effect_list:
                if CurrentEffect == normal:
                    if effectGenerator() == effect.chance:
                        CurrentEffect = effect
                        effect.LastUpdate = time.time()
                        if effect != normal:
                            print(Fore.CYAN + effect.name + " Random event!!!" + Style.RESET_ALL)
            if dice == i:
                print(str(dice) + Fore.YELLOW + " Critical Roll! 2x Points" + Style.RESET_ALL)
                dice = dice * 2
            rollerCounter += 1
            diceSum += dice
        score = score + (diceSum * scoreMultiplicator)
        time.sleep(0.2)
        printUI()    
    #Upgrade Menu
    if keyboard.is_pressed('u'):
        clear_screen()
        print("available upgrades:")
        for Upgrades in upgrade_list:
            print(Fore.GREEN + Upgrades.name + Style.RESET_ALL + " | Cost: " + Fore.RED + str(Upgrades.cost) + Style.RESET_ALL + " | Dice sides: " + Fore.RED + str(Upgrades.Dicesides) + Style.RESET_ALL + " | Dice Amount: " + Fore.RED + str(Upgrades.diceAmount) + Style.RESET_ALL + " | Score Multiplier: " + Fore.RED + str(Upgrades.scoreMultiplier) + Style.RESET_ALL)
        time.sleep(0.2)
        
        
    #advanced view toggle    
    if keyboard.is_pressed('a'):
        AdvancedView = not AdvancedView
        
    # Upgrade Handler
    for Upgrades in upgrade_list:
        if keyboard.is_pressed(Upgrades.key):
            if score >= Upgrades.cost:
                i += Upgrades.Dicesides
                score += Upgrades.diceAmount
                scoreMultiplicator *= Upgrades.scoreMultiplier
                rollAmmount += Upgrades.diceAmount
                score -= Upgrades.cost
                Upgrades.cost *= Upgrades.priceMultiplier
                print("You purchased " + Fore.GREEN + Upgrades.name + Style.RESET_ALL)
                time.sleep(0.2)
            else:
                print("You don't have enough points to purchase " + Fore.GREEN + Upgrades.name + Style.RESET_ALL)
                time.sleep(0.2)



    #Lore Book Handler
    if keyboard.is_pressed('l'):
        LoreBookActive = not LoreBookActive

    if LoreBookActive:
        clear_screen()
        LoreBook.readLore(score)
        
        
    time.sleep(0.05)