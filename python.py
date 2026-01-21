# imports
import random
import keyboard
import time
import os
from dataclasses import dataclass,field
from colorama import Fore, Style

# =======================
# Dataclasses
# =======================

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
    description: str
    ability: list[str]
    difficultyTier: int


@dataclass
class Gamestate:
    score: int = 0
    dicesides: int = 6
    diceAmount: int = 1
    diceSum: int = 0
    scoreMultiplier: int = 1
    loreBookActive: bool = False
    bossActive: bool = False
    printedLore: bool = False
    idleActivation: bool = False
    bossRollTimer: int = 0
    activeBossHealth: int = 0
    corruption: float = 0.0
    corruptionRate: float = 0.0
    startUIprinted: bool = False


# =======================
# Upgrades
# =======================

dice_Sides_Upgrades = Upgrades(
    "Dice Sides Upgrade",
    "Increase the amount of Dice sides",
    50, 1, 0, 0, 1.5, "1"
)

dice_Amount_Upgrades = Upgrades(
    "Dice Amount Upgrade",
    "Increase the amount of Dice [aka. How many spins u have per roll]",
    100, 0, 1, 0, 1.7, "2"
)

score_Multiplier_Upgrades = Upgrades(
    "Score Multiplier Upgrade",
    "Increases the multiplier to the sum of all the dice in the roll",
    200, 0, 0, 1, 2.0, "3"
)

idle_Activation_Upgrade = Upgrades(
    "Idle Activation Upgrade",
    "Activates the idle System [unlocks another upgrade menu, unlocks corruption]",
    1250, 0, 0, 0, 2.5, "4",
    OneTime=True
)

upgrade_list = [
    dice_Sides_Upgrades,
    dice_Amount_Upgrades,
    score_Multiplier_Upgrades,
    idle_Activation_Upgrade
]


# =======================
# Effects
# =======================

Bleeding = Effects(

)
Freeze = Effects(

)




# =======================
# Input / Logic
# =======================

def wait_for_key_release(key):
    while keyboard.is_pressed(key):
        time.sleep(0.01)
def InputHandler(gamestate: Gamestate):
    if keyboard.is_pressed('enter'):
        wait_for_key_release('enter')
        Roll_Logic(gamestate)
        time.sleep(0.3)

    if keyboard.is_pressed('q'):
        exit()


def Roll_Logic(gamestate: Gamestate):
    latestRolls: list[int] = []
    gamestate.diceSum = 0
    for i in range(gamestate.diceAmount):
        Roll = random.randint(1, gamestate.dicesides)
        gamestate.diceSum += Roll
        latestRolls.append(Roll)

    gamestate.score += gamestate.diceSum * gamestate.scoreMultiplier
    Print_UI(gamestate,latestRolls)


def Upgrade_Logic(gamestate: Gamestate, upgrade: Upgrades):
    if not keyboard.is_pressed(upgrade.key):
        return

    wait_for_key_release(upgrade.key)

    if upgrade.OneTime and upgrade.purchased:
        return

    if gamestate.score < upgrade.cost:
        return

    gamestate.score -= upgrade.cost
    gamestate.dicesides += upgrade.Dicesides
    gamestate.diceAmount += upgrade.diceAmount
    gamestate.scoreMultiplier += upgrade.scoreMultiplier
    upgrade.cost *= upgrade.priceMultiplier

    if upgrade.name == "Idle Activation Upgrade":
        gamestate.idleActivation = True
        upgrade.purchased = True

    Print_UI(gamestate,[])
    print(Fore.GREEN + f"You purchased {upgrade.name}!" + Style.RESET_ALL)
    time.sleep(0.3)


# =======================
# UI
# =======================

def Print_UI(gamestate: Gamestate,rolls:list[int]):
    os.system('cls' if os.name == 'nt' else 'clear')

    print("============================================================")
    print(Fore.GREEN + "Dice Game" + Style.RESET_ALL)
    print("============================================================")
    print(f"Score: {gamestate.score:.2f}")
    print(f"Dice Sides: {gamestate.dicesides}")
    print(f"Dice Amount: {gamestate.diceAmount}")
    print(f"Score Multiplier: {gamestate.scoreMultiplier}")
    print(f"Corruption: {gamestate.corruption:.2f}%")
    for i,Roll in enumerate(rolls):
        print(f"Roll {i + 1} = {Roll}")
    print("")
    print("============================================================")
    print(Fore.MAGENTA + "Upgrade Menu" + Style.RESET_ALL)
    print("============================================================")

    for upgrade in upgrade_list:
        if upgrade.OneTime and upgrade.purchased:
            continue
        print(
            Fore.RED + f"Press '{upgrade.key}' " +
            Fore.LIGHTBLUE_EX + upgrade.name +
            Fore.RESET + f" ({upgrade.cost:.2f} points)" + Style.RESET_ALL
        )
        print(Fore.YELLOW + upgrade.description + Style.RESET_ALL)

    print("")
    print("Press ENTER to roll | Q to quit")


# =======================
# Main Loop
# =======================

gamestate = Gamestate()
Print_UI(gamestate,[])

while True:
    InputHandler(gamestate)
    for upgrade in upgrade_list:
        Upgrade_Logic(gamestate, upgrade)
    time.sleep(0.02)
