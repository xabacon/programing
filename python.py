# imports
import random
import keyboard
import time
import os
import LoreBook
from dataclasses import dataclass,field
from colorama import Fore, Style
from typing import Callable

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
    Description: str
    LoreDescription: str
    Formula: Callable[["Gamestate", "Effects"], None]
    activated: bool = False
    TimesCalled: int = 0
    Effect_Weights = [
                       70 # Normal Effect Weight
                      ,7 # Reconstruction Effect Weight
                      ,7 # Spark Effect Weight
                      ,5 # Freeze Effect Weight
                      ,5 # Critical Effect Weight
                      ,3 # Corruption Effect Weight
                      ,3 # Enlightment Effect Weight
                      ]
    
    def activate(self, gamestate):
        self.TimesCalled += 1
        self.Formula(gamestate,self)




@dataclass
class Gamestate:
    lastRoll: int = 0
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
# Effect Formulas,Definitions and Logic
# =======================
Normal_Formula = lambda Gamestate, Effects: setattr(Gamestate, "score", Gamestate.score)
Reconstruction_Formula = lambda Gamestate, Effects: setattr(Gamestate, "score", Gamestate.score - (Gamestate.diceSum * 2))
Spark_Formula = lambda Gamestate, Effects: setattr(Gamestate, "score", Gamestate.score + (Gamestate.diceSum * 2))
Freeze_Formula = lambda Gamestate, Effects: setattr(Gamestate, "dicesides", max(1, Gamestate.dicesides - 1))
Critical_Formula = lambda Gamestate, Effects: setattr(Gamestate, "score", Gamestate.score + Gamestate.lastRoll * 2)
Corruption_Formula = lambda Gamestate, Effects: setattr(Gamestate, "corruption", Gamestate.corruption + random.uniform(0.5, 1.0))
Enlightment_Formula = lambda Gamestate, Effects: setattr(Gamestate, "corruption", max(0.0, Gamestate.corruption - random.uniform(0.5, 1.0)))

Normal = Effects(
    "Normal",
    "No special Interactions",
    """The dice rolled,slowed down and stopped normally
Since no anomallies were detected the roll is considered normal""",
    Formula = Normal_Formula,
)
Reconstruction = Effects(
    "Reconstruction",
    "Reduces current Roll sum by 5%",
    """The dice was thrown to fast leading to a crack
Unfortunatelly this will need to be fixed before the next Dice roll
The dice will be mended with the energy it produced during the whole roll""",
    Formula = Reconstruction_Formula,
)
Spark = Effects(
    "Spark",
    "Increases current roll sum by 5%",
    """The dice starts Ricocheting accross the universe leading to sparks!
The energy it creates transforms into more value!""",
    Formula = Spark_Formula,
)
Freeze = Effects(
    "Freeze",
    "Reduce dice sides by 1 for the next roll",
    """The dice was thrown to fast leading to a crack
Unfortunatelly this will need to be fixed before the next Dice roll
The dice will be mended with the energy it produced during the whole roll""",
    Formula = Freeze_Formula,
)
Critical = Effects(
    "Critical",
    "Double the dice value",
    """The dice was thrown to fast leading to a crack
Unfortunatelly this will need to be fixed before the next Dice roll
The dice will be mended with the energy it produced during the whole roll""",
    Formula = Critical_Formula,
)
Corruption = Effects(
    "Corruption",
    "Adds 0.5-1% Corruption per triggered dice roll",
    """The dice Flew into a Tear!
Leading to it being slightly more Corrupted!""",
    Formula = Corruption_Formula,
)
Enlightment = Effects(
    "Enlightment",
    "Removes 0.5-1% Corruption per Triggered dice",
    """The dice Returned to sender!
Bringing back some of its Reality and Integrity back!""",
    Formula = Enlightment_Formula,
)
Effects_list = [
    Normal,
    Reconstruction,
    Spark,
    Freeze,
    Critical,
    Corruption,
    Enlightment
]

def Effect_Logic(gamestate: Gamestate) -> str:
    Rolled_Effect = random.choices(Effects_list, weights=Effects.Effect_Weights, k=1)[0]
    Rolled_Effect.activate(gamestate)
    return Rolled_Effect.name
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
        
    if keyboard.is_pressed('l'):
        gamestate.loreBookActive = not gamestate.loreBookActive
        clear_screen()
        if not gamestate.loreBookActive:
            Print_UI(gamestate, [])
        time.sleep(0.3)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def Roll_Logic(gamestate: Gamestate):
    latestRolls: list[int] = []
    latest_Effects: list[str] = []
    gamestate.diceSum = 0
    for i in range(gamestate.diceAmount):
        Roll = random.randint(1, gamestate.dicesides)
        gamestate.diceSum += Roll
        Effect_Name = Effect_Logic(gamestate)
        latestRolls.append(Roll)
        latest_Effects.append(Effect_Name)
        gamestate.lastRoll = latestRolls[0]
        gamestate.diceSum /= 1 - (gamestate.corruption / 100)
    gamestate.score += gamestate.diceSum * gamestate.scoreMultiplier
    Print_UI(gamestate,latestRolls,latest_Effects)
    
    for effect in Effects_list:
        effect.TimesCalled = 0


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

def Print_UI(gamestate: Gamestate,rolls:list[int],latest_Effects:list[str]=[]):
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
        print(f"Roll {i + 1} = " + Fore.CYAN + f"{Roll}" + Style.RESET_ALL + f" || Effect Applied :" + Fore.YELLOW + f" {latest_Effects[i]}" + Style.RESET_ALL)
    print("")
    if gamestate.diceAmount > 50:
        for effect in Effects_list:
            print(Fore.CYAN + f"Effect: {effect.name} | Times Triggered: {effect.TimesCalled}" + Style.RESET_ALL)
    print ("")
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
    

def lore(gamestate:Gamestate):
    if gamestate.loreBookActive and not gamestate.printedLore:
        LoreBook.readLore(gamestate.score)
        gamestate.printedLore = True

# =======================
# Main Loop
# =======================
gamestate = Gamestate()
Print_UI(gamestate,[])

while True:
    if gamestate.loreBookActive:
        lore(gamestate)
    InputHandler(gamestate)
    for upgrade in upgrade_list:
        Upgrade_Logic(gamestate, upgrade)
    time.sleep(0.02)
