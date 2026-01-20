imports

import random

import keyboard

import time

import os

import LoreBook

from dataclasses import dataclass

from colorama import Fore, Style

#Dataclasses

@dataclass

class Upgrades:

name: str

description: str

cost: int

Dicesides: int

diceAmount: int

scoreMultiplier: int

priceMultiplier: float

key: str

purchased: bool = False

OneTime: bool = False

#Effects Struct Declaration

@dataclass

class Effects:

name: str

chance: int

effect: int

effectInterval: float

duration: float

activated: bool = False

LastUpdate: float = 0.0

@dataclass

class Bosses:

name: str

description : str

ability : list[str]

difficultyTier : int

@dataclass

class Gamestate:

score:int = 0

dicesides:int = 6

diceAmount:int = 1

diceSum:int = 0

scoreMultiplier:int = 1

loreBookActive:bool = False

bossActive:bool = False

printedLore:bool = False

idleActivation:bool = False

bossRollTimer:int = 0

activeBossHealth:int = 0

corruption:float = 0.0

corruptionRate:float = 0.0

Upgrades:list = None

Effects:list = None

Bosses:list = None

startUIprinted = False

dice_Sides_Upgrades = Upgrades(

"Dice Sides Upgrade",

"Increase the amount of Dice sides",

50, 1, 0, 0, 1.5,

"1")

dice_Amount_Upgrades = Upgrades(

"Dice Amount Upgrade",

"Increase the amount of Dice [aka. How many spins u have per roll]",

100, 0, 1, 0, 1.7,

"2")

score_Multiplier_Upgrades = Upgrades(

"Score Multiplier Upgrade",

"Increases the multiplier to the sum of all the dice in the roll",

200, 0, 0, 1, 2.0,

"3")

idle_Activation_Upgrade = Upgrades(

"Idle Activation Upgrade",

"Activates the idle System [unlocks another upgrade menu,unlocks corruption]",

1250, 0, 0, 0, 2.5,

"4",

OneTime=True)

upgrade_list = [dice_Sides_Upgrades, dice_Amount_Upgrades, score_Multiplier_Upgrades, idle_Activation_Upgrade]

def InputHandler(gamestate:Gamestate):

if keyboard.is_pressed('l'):

    gamestate.loreBookActive = not gamestate.loreBookActive

    time.sleep(0.3)



if keyboard.is_pressed('a'):

    gamestate.advancedView = not gamestate.advancedView

    time.sleep(0.3)



if keyboard.is_pressed('enter'):

    Roll_Logic(gamestate)

    time.sleep(0.3)



if keyboard.is_pressed('q'):

    exit()

def print_Start_UI(gamestate:Gamestate):

if not gamestate.startUIprinted:

    print(Fore.RED + "Welcome to the Dice Game!" + Style.RESET_ALL)

    print("the basic rules are simple:")

    print("Press " + Fore.LIGHTBLUE_EX + "'Enter'" + Style.RESET_ALL + " to roll the dice and earn points based on your roll.")

    print("Press " + Fore.LIGHTBLUE_EX + "'L'" + Style.RESET_ALL + " to open the Lore Book and learn more about the game's story.")

    print("Press " + Fore.LIGHTBLUE_EX + "'U'" + Style.RESET_ALL + " to Open the Upgrade Menu.")

    gamestate.startUIprinted = True

else :

    pass

def Roll_Logic(gamestate:Gamestate):

gamestate.diceSum = 0

for i in range(gamestate.diceAmount):

    gamestate.diceSum += random.randint(1, gamestate.dicesides)

gamestate.score += gamestate.diceSum * gamestate.scoreMultiplier

Print_UI(gamestate)

def Upgrade_Logic(gamestate:Gamestate, upgrade:Upgrades):

if keyboard.is_pressed(upgrade.key):

    if gamestate.score >= upgrade.cost:

        gamestate.score -= upgrade.cost

        gamestate.dicesides += upgrade.Dicesides

        gamestate.diceAmount += upgrade.diceAmount

        gamestate.scoreMultiplier *= upgrade.scoreMultiplier

        gamestate.idleActivation = True if upgrade.name == "Idle Activation Upgrade" else gamestate.idleActivation

    print(Fore.GREEN + "You have purchased " + upgrade.name + Style.RESET_ALL)

    time.sleep(0.2)

    if upgrade.OneTime:

            upgrade.purchased = True

    else:

        print("You don't have enough points to purchase " + Fore.GREEN + upgrade.name + Style.RESET_ALL)

        time.sleep(0.2)

def clear_screen():

if os.name == 'nt':

    os.system('cls')

def lore(gamestate:Gamestate):

if gamestate.loreBookActive and not gamestate.printedLore:

    LoreBook.readLore(gamestate.score)

    gamestate.printedLore = True

    if keyboard.is_pressed('l'):

        gamestate.loreBookActive = False

        clear_screen()

def Print_UI(gamestate:Gamestate):

os.system('cls' if os.name == 'nt' else 'clear')

print("============================================================")

print(Fore.GREEN + "Dice Game" + Style.RESET_ALL)

print("============================================================")

print(f"Score: {gamestate.score}")

print(f"Dice Sides: {gamestate.dicesides}")

print(f"Dice Amount: {gamestate.diceAmount}")

print(f"Score Multiplier: {gamestate.scoreMultiplier}")

print(f"Corruption: {gamestate.corruption:.2f}%")

print("")

print("============================================================")

print(Fore.MAGENTA + "Controls" + Style.RESET_ALL)

print("============================================================")

print("Press " + Fore.LIGHTBLUE_EX + "'Enter'" + Style.RESET_ALL + " to roll the dice.")

print("Press " + Fore.LIGHTBLUE_EX + "'L'" + Style.RESET_ALL + " to toggle Lore Book.")

print("Press " + Fore.LIGHTBLUE_EX + "'A'" + Style.RESET_ALL + " to toggle Advanced View.")

print("Press " + Fore.LIGHTBLUE_EX + "'Q'" + Style.RESET_ALL + " to quit the game.")

print("")

print("============================================================")

print(Fore.MAGENTA + "Upgrade Menu" + Style.RESET_ALL)

print("============================================================")

for upgrade in upgrade_list:

    if upgrade.OneTime and upgrade.purchased:

        continue

    print(Fore.RED + f"Press '{upgrade.key}' to purchase"+ Fore.LIGHTBLUE_EX + f" {upgrade.name}" + Fore.RESET+ f" for " + Fore.RED + f"{upgrade.cost}" + Fore.RESET + f" points." + Style.RESET_ALL)

    print(Fore.YELLOW + f"'{upgrade.description}'" + Style.RESET_ALL)

gamestate = Gamestate()

while True:

if gamestate.loreBookActive:

    lore(gamestate)

print_Start_UI(gamestate)

InputHandler(gamestate)

for upgrade in upgrade_list:

    Upgrade_Logic(gamestate, upgrade)