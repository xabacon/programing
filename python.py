# imports
import random
import keyboard
import time
import os
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
    activated: bool = False
    LastUpdate: float = 0.0

@dataclass
class Bosses:
    name: str
    description : str
    ability : list[str]
    difficultyTier : int


    
# upgrade Declarations
basic_side_Increase = Upgrades("Basic Side Increase", 10, 1, 0, 1,1.4,"1")
basic_Amount_Increase = Upgrades("Basic Amount Increase", 20, 0, 1, 1,2.8,"2")
basic_Score_Multiplier = Upgrades("Basic Score Multiplier", 50, 0, 0, 2,4.3,"3")


# effect Declarations
normal = Effects("Normal", 0, 0, 0, 0)
ice = Effects("Ice", 1, 1, 5.0, 20.0)
fire = Effects("Fire", 2, 5, 2.0, 5.0)
poison = Effects("Poison", 3, 10, 15.0, 30.0)

Boss_List = [
    Bosses("Frostbane", "", ["nullifier", "fortifier"], 2),
    Bosses("Emberlord", "", ["damager", "mutator"], 3),
    Bosses("Nightfall", "", ["corruptor", "randomizer"], 2),
    Bosses("Ironclad", "", ["fortifier", "damager"], 3),
    Bosses("Chaosborn", "", ["randomizer", "mutator", "chancer"], 4),
    Bosses("Venomash", "", ["corruptor", "damager"], 2),
    Bosses("Hexroot", "", ["chancer", "nullifier"], 1),
    Bosses("Riftmaw", "", ["mutator", "fortifier"], 3),
    Bosses("Bonegrim", "", ["damager", "corruptor", "chancer"], 4),
    Bosses("Stormrend", "", ["randomizer", "chancer"], 2)
]

#All Declared lists
upgrade_list = [basic_side_Increase, basic_Amount_Increase, basic_Score_Multiplier]
effect_list = [ice, fire, poison]
Boss_Effect_list = ["damager","nullifier","chancer","randomizer","mutator","corruptor","fortifier"]

#Dice Generator Function
def generator(DiceSides):
    return random.randint(0,DiceSides)
def effectGenerator():
    return random.randint(0,3)
def BossHealthGenerator(Tiers):
    match Tiers:
        case 1 :
            health = random.randint(80,150)
            return health
        case 2:
            health = random.randint(150,250)
            return health
        case 3:
            health = random.randint(250,400)
            return health
        case 4:
            health = random.randint(400,600)
            return health

# clear screen function
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
        
# effect Updater function
def update_effects():
    global score, LastUpdate, ActiveEffect
    for effect in effect_list:
        if effect.activated:
            now = time.time()
            if now - effect.LastUpdate >= effect.effectInterval:
                score += effect.effect
                effect.duration -= effect.effectInterval
                effect.LastUpdate = now
                if effect.duration > 0:
                        continue
                else:
                    normal.activated = True
                    effect.activated = False
                    print(Fore.MAGENTA + effect.name + " effect has worn off." + Style.RESET_ALL)
# boss spawner function
def Boss_Spawner(Tier):
    Possible_Bosses = [b for b in Boss_List if b.difficultyTier == Tier]
    global ActiveBoss,ActiveBossHealth,BossActive,ActiveBossTier
    ActiveBoss = random.choice(Possible_Bosses)
    ActiveBossHealth = BossHealthGenerator(Tier)
    BossActive = True
    ActiveBossTier = Tier

def Boss_Logic():
    global score
    for ability in ActiveBoss.abilities:
        match ActiveBoss.abilities:
            case "damager":
                return
            case "nullifier":
                return
            case "chancer":
                return
            case "randomizer":
                return
            case "mutator":
                return
            case "corruptor":
                return 
            case "fortifier":
                return


def update_score_line(new_score):
    print("\033[1A", end='')
    print("\033[K", end='')
    print("your score is: " + Fore.RED + str(new_score) + Style.RESET_ALL, flush=True)
def printUI():
        print("=============================================================")
        print("Press " + Fore.GREEN + "'u'" + Style.RESET_ALL + " to enter Upgrade Screen")
        print("Press " + Fore.GREEN + "'a'" + Style.RESET_ALL + " to toggle advanced view")
        print("Number of rolls before a" + Fore.RED + "BOSS ENCOUNTER" + Fore.GREEN +)
        print("=============================================================")
        if AdvancedView == True:
            print("Current Dice sides: " + Fore.RED + str(DiceSides) + Style.RESET_ALL)
            print("Current Dice Amount: " + Fore.RED + str(rollAmmount) + Style.RESET_ALL)
            print("Current Score Multiplier: " + Fore.RED + str(scoreMultiplicator) + Style.RESET_ALL)
        print("You rolled a " + Fore.RED + str(diceSum) + Style.RESET_ALL)
        update_score_line(score)


#main Code
Instructions = True
DiceSides = 6
score = 0
scoreMultiplicator = 1
rollAmmount = 1
LastUpdate = time.time()
AdvancedView = False
ActiveEffect = False
BossRollTimer = 75
BossActive = False
ActiveBoss : Bosses | None = None
ActiveBossHealth = 0
Corruption = 0.00
ActiveBossTier = 0



#game loop
while True:
    if ActiveEffect:
        update_effects()
        update_score_line(score)
    if Instructions:
        Instructions = False
        print("Welcome to the dice roller!")
        print("Press " + Fore.GREEN + "'q'" + Style.RESET_ALL + " to quit")
        print("Press " + Fore.GREEN + "'enter'" + Style.RESET_ALL + " to roll the dice")
    if keyboard.is_pressed('q'):
        break
    
    
    # roll dice
    if keyboard.is_pressed('enter'):
        rollerCounter = 0
        diceSum = 0
        while not BossActive:
            BossRollTimer -= 1
            if BossRollTimer == 0:
                Boss_Spawner(random.randint(1,4))
                BossRollTimer == random.randint(50,150)
        else : Boss_Logic()
        clear_screen()

        #roll handler
        while (rollerCounter < rollAmmount):
            dice = generator(DiceSides)
            for effect in effect_list:
                if effectGenerator() == effect.chance:
                    effect.activated = True
                    ActiveEffect = True
                    print(Fore.CYAN + effect.name + " Random event!!!" + Style.RESET_ALL)
            if dice == DiceSides:
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
        
    if keyboard.is_pressed('a'):
        AdvancedView = not AdvancedView
        
        
        # Upgrade Handler
    for Upgrades in upgrade_list:
        if keyboard.is_pressed(Upgrades.key):
            if score >= Upgrades.cost:
                DiceSides += Upgrades.Dicesides
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
    time.sleep(0.05)