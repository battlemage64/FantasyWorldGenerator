import random # Used, of course, for random generation.
import os # Used to navigate directories to save logs and histories in order.
import datetime # Used for logging when the file was made
import time # Used for keeping fraction-of-a-second-accurate log times
import NameGen as ng

LISTS = open('lists.py', 'r').read()
exec(LISTS)
del LISTS # just good practice not to have this thing floating around

TOWNS = [] # master list of towns, for later
HEROS = [] # master list of great heros
WARS = [] # list of tuples of (first warring town, second warring town)

def rand_limit(low, high):
    "Gets a random decimal between low and high"
    choice = random.random()
    while choice < low or choice > high:
        choice = random.random()
    return choice

def bce_or_not(time):
    "Either returns 'year (space)' or 'year (space) B' so dates can just be this function with CAL_AB immediately afterward"
    if time < 0:
        return "{0} B".format(time * -1)
    else:
        return time

LAST_CHOSEN = "" # needs to be global

def iFromList(dictname, keyname = "all"):
    "Returns a random item from dictname[keyname] or all children of dictname"
    global LAST_CHOSEN
    if keyname == "all":
        choices = []
        for key, value in dictname.items():
            for item in value:
                choices.append(item)
        chosen = random.choice(choices)
    else:
        chosen = random.choice(dictname[keyname])
    if chosen == LAST_CHOSEN: # won't pick the same thing twice in a row
            chosen = iFromList(dictname, keyname)
    return chosen

def genTerrain(): # generates a named terrain location
    string = iFromList(TERRAIN_TYPES)
    choice = random.randint(1, 4)
    if choice == 1:
        string = string + " of {name}"
    elif choice == 2:
        string = "{name} " + string
    elif choice == 3:
        string = "{name} {name2} " + string
    elif choice == 4:
        string = string + " of {name} {name2}"
    return string.format(name=ng.genName().title(), name2=ng.genName().title())

# Initialize log
prev_logs = len(os.listdir("./Records/Logs/")) - 1
logfile = open("./Records/Logs/log_" + str(prev_logs) + '.txt', 'w')

INIT_TIME = time.time() # starting time in seconds since epoch, to be subtracted from log times

def log(text):
    "adds text to log along with timestamp"
    logfile.write(str(time.time() - INIT_TIME) + ": ")
    logfile.write(str(text))
    logfile.write("\n\n")
    logfile.flush()

now = datetime.datetime.now() # Current time (when this is called)
log("Log initialized at {0}-{1}-{2} at {3}:{4}:{5} using HistoryGen version 0.1!".format(now.year, now.month, now.day, now.hour, now.minute, now.second))

# Initialize history file
histfile = open("./Records/Histories/hist_" + str(prev_logs) + '.txt', 'w')

def addHist(text):
    "adds text to history file"
    histfile.write(str(text))
    histfile.write("\n\n")
    histfile.flush()

# Note that "now" has NOT updated since last used.
# This means the time here will be milliseconds off.
# This is more consistent and efficient, though.
addHist("History created at {0}-{1}-{2} at {3}:{4}:{5}.".format(now.year, now.month, now.day, now.hour, now.minute, now.second))
log("History created.")

class Continent: # a Continent has a randgen name and a few biomes attributed
    def __init__(self):
        self.name = ng.genName()
        self.biomes = []
        for i in range(0, random.randint(1, 4)):
            self.biomes.append(random.choice(BIOMETYPES))
        self.inhabFactor = 0
        if 'deciduous forest' in self.biomes:
            self.inhabFactor += 1
        if 'evergreen forest' in self.biomes:
            self.inhabFactor += 0.9
        if 'desert' in self.biomes:
            self.inhabFactor += 0.1
        if 'marsh' in self.biomes:
            self.inhabFactor += 0.5
        if 'grasslands' in self.biomes:
            self.inhabFactor += 0.9
        if 'mountains' in self.biomes:
            self.inhabFactor += 0.7
        if 'tundra' in self.biomes:
            self.inhabFactor += 0.45
        if 'hills' in self.biomes:
            self.inhabFactor += 0.85
        self.inhabFactor /= len(set(self.biomes))
        self.inhabited = False
        self.locations = [] # all locations of towns on continent

class Town:
    "A town on a continent"
    def __init__(self, continent = None):
        self.name = ng.genName()
        if continent == None:
            self.continent = random.choice(CONTINENTS_INHABITED)
        else:
            self.continent = continent
        self.previousNames = []
        self.resources = random.randint(11, 25) # need 10 to stay fine, any less and starvation sets in
        self.size = random.randint(1, 2)
        self.propagate()
        self.trade_routes = []
        self.allies_enemies = {} # city entered with either 1 or -1. 1 = ally, -1 = enemy.
        global TOWNS
        TOWNS.append(self)
        self.propagate()
        self.gen_terrain()
    def changeName(self, return_name):
        "Change the name of a city, record the old name, and possibly return the new name"
        self.previousNames.append(self.name)
        self.name = ng.genName()
        if return_name:
            return self.name
    def propagate(self):
        self.relations = {}
        for town in TOWNS:
            if town == self:
                continue
            self.relations[town] = 0
            town.addRelation(self)
    def addRelation(self, town):
        self.relations[town] = 0
    def destroy(self):
        "Should be called upon the city's destruction."
        log("Destroying {0}...".format(self.name))
        for war in WARS:
            if self in war:
                WARS.remove(war)
        global TOWNS
        for town in TOWNS:
            if town == self:
                continue
            if self in town.trade_routes:
                town.trade_routes.remove(self)
            del town.relations[self]
        TOWNS.remove(self)
    def gen_terrain(self):
        terrain = []
        for i in range(3, 10):
            terrain.append(genTerrain())
        self.locations = terrain
        for item in terrain:
            self.continent.locations.append(item)

class Hero:
    "A famous person in history"
    def __init__(self, role = None, hometown = None):
        if hometown == None:
            self.hometown = random.choice(TOWNS)
        else:
            self.hometown = hometown
        self.role = role
        if role == None:
            self.role = iFromList(ROLES, TECH_LEVEL)
        self.name = ng.genName()
        self.nametitle = iFromList(TITLES).format(name=self.name, noun1=iFromList(NOUNS, "other"), verb1=iFromList(VERBS, "er"), noun2=iFromList(NOUNS, "plural"), noun3=iFromList(NOUNS, "singular"), verb2=iFromList(VERBS, "3rdsin"))
        self.birthdate = currentSimTime
        self.age = 0
        self.earnedTitle = False
        global HEROS
        HEROS.append(self)
    def move(self):
        "Home was destroyed or they decided to leave."
        newhome = random.choice(TOWNS)
        while newhome == self.hometown:
            newhome = random.choice(TOWNS)
    def die(self):
        "Hero dies."
        HEROS.remove(self)
        del self
    def flee(self):
        oldtown = self.hometown
        while self.hometown == oldtown:
            self.hometown = random.choice(TOWNS)
    def namewithtitle(self):
        if self.earnedTitle:
            return self.nametitle
        else:
            return self.name
    def earntitle(self):
        if self.role == "hunter":
            return "killing a {0} {1}".format(iFromList(COLORS), iFromList(ANIMALS))
        elif self.role == "farmer":
            return "having their crops spared during a plague of {0}s".format(iFromList(ANIMALS))
        elif self.role == "cook":
            return "cooking a meal so delicious that it caused the ruler of {0} to weep".format(random.choice(TOWNS).name)
        elif self.role == "merchant":
            newtown = Town(self.hometown.continent)
            return "becoming so rich their servants required their own town to live in. That town became known as {0}".format(newtown.name)
        elif self.role == "warrior":
            return "leading a charge and killing {0}, legendary enemy general, despite terrible odds".format(ng.genName())
        elif self.role == "shaman":
            return "a sign from the gods: a {0} {1}".format(iFromList(COLORS), iFromList(NOUNS))
        elif self.role == "priest":
            return "being spoken to by their god...supposedly"
        elif self.role == "youth":
            return "fomenting an uprising against the rulers of {0}".format(random.choice(TOWNS).name)
        elif self.role == "healer" or self.role == "herbalist":
            return "bringing {0} back from the brink of death".format(otherHero(self).name)
        elif self.role == "artist":
            return "creating the masterpiece \"{0}\"".format(eval(iFromList(QW_CLAUSES)))
        elif self.role == "ruler":
            self.hometown.resources += 20
            return "leading their city on to greatness and wealth"

class LengthError(Exception):
    def __init__(self, message):
        self.message = message

def otherTown(town):
    if len(TOWNS) == 1:
        raise LengthError("TOWNS is 1 item")
    town2 = town
    while town2 == town:
        town2 = random.choice(TOWNS)

def otherHero(hero):
    if len(HEROS) == 1:
        log("HEROS is 1 item, adding...")
        greatRise()
    hero2 = hero
    while hero2 == hero:
        hero2 = random.choice(HEROS)
    return hero2

# Step 1: Generate continents
CONTINENTS = []
CONTINENTS_INHABITED = []
for i in range(0, random.randint(3, 9)):
    CONTINENTS.append(Continent())

log("Creating calendar...")
cal_cre_fn = ng.genName() # Calendar creator's first and last name, and origin town
cal_cre_ln = ng.genName()
cal_cre_org = ng.genName()
CAL_AB = cal_cre_fn[0].upper() + cal_cre_ln[0].upper() # Calendar abbreviation
addHist("Note: Calendar uses the {0} scale, named for {1} {2}, famous historian of {3}".format(CAL_AB, cal_cre_fn, cal_cre_ln, cal_cre_org))
log("Calendar created")

# Step 2: Generate the evolution of people
def genWorld():
    # For now, this is the only case.
    # Begin to generate history, starting with the planet's creation,
    # then the first life, then first land life, then first humans.
    
    log("Generating starting history...")
    
    addHist("A small star, approximately 1 AU away. A ball of debris slowly grow larger and eventually forms into a planet.")
    addHist("Continents form, weather patterns form, all that great stuff.")
    addHist("A chance meeting of molecules forms the first amino acid.")
    addHist("An even more chance meeting forms the first eukaryote.")
    
    addHist("Before long, life is born.\n\n--------------------")

    # Generate where the first humans evolve.
    firstCont = random.choice(CONTINENTS)
    addHist("The first humans evolve on continent {0} around {1} million {2}. They survive by hunting the herds of {3}.".format(firstCont.name, str(random.randint(10, 15)), CAL_AB, iFromList(ANIMALS, "land_prey_large")))
    firstCont.inhabited = True

    log("Adding humans to continents...")

    ago = random.randint(10, 100) * 0.1
    ago = round(ago, 2)
    
    for cont in CONTINENTS:
        if not cont.inhabited and random.randint(1, 8) != 1:
            addHist(str(ago) + " million B{0}: ".format(CAL_AB)
                    + iFromList(REASONS_TO_LEAVE, "hunt&gath")
                    + ", {0}s of the {1} {2} discover the continent {3}. They call it {4} {5}, meaning '{6}'."
                    .format(iFromList(ROLES, "hunt&gath"), iFromList(GROUPS, "hunt&gath"),
                            ng.genName(), cont.name, ng.genName(), ng.genName(), eval(iFromList(QW_CLAUSES, "where"))))
            cont.inhabited = True
            CONTINENTS_INHABITED.append(cont)
            ago *= rand_limit(0.5, 1) # Next one will be more recent
            ago = round(ago, 2) # Rounds it so it's not super long
    log("World generation finished, continents inhabited")

def beginAgric():
    log("Discovering agriculture...")
    cont_where = random.choice(CONTINENTS_INHABITED)
    global begintime
    begintime = random.randint(9000, 20000)
    addHist("{0} B{1}, in {2}: The {3} {4} notice that {5} plants have grown where they dropped seeds last year.".format(begintime, CAL_AB, cont_where.name, ng.genName(), iFromList(GROUPS, "hunt&gath"), iFromList(PLANTS)))
    if random.randint(1, 2) == 1:
        log("Choice: disregard plants")
        addHist("They disregard this, believing it to be a coincidence.")
        addHist("They regret this later, when another tribe discovers how to cultivate plants and settles down to form the first town.")
    else:
        log("Choice: Settle and cultivate")
        addHist("They decide to settle down and farm the land (a few years later, after figuring out just what farming is).")
    first_town = Town(cont_where)
    addHist("This town comes to be known as {0}.".format(first_town.name))
    addHist("Soon, other towns are formed as the secret of agriculture spreads.")
    for cont in CONTINENTS_INHABITED:
        for i in range(2, 5):
            newtown = Town(cont)
            log("Town {0} created as {1}".format(newtown.name, newtown))

def raidTown(t1 = None, t2 = None):
    "One town raids another town. Leave at None to be set randomly."
    log("City attack called")
    global TOWNS
    if t1 == None:
        cs_in_raid = random.sample(TOWNS, 2)
        t1 = cs_in_raid[0]
        t2 = cs_in_raid[1]
            
    log("City raid: targets {0} raids {1}".format(t1.name, t2.name))
    if t1.relations[t2] <= 0:
        addHist("{0}{1}: The town of {2} raids the town of {3}.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name))
    else:
        addHist("{0}{1}: The town of {2} raids their ally {3}, {4}.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name, iFromList(REASONS_TO_ATTACK)))
        t2.relations[t1] = 0

    allybonus = 0

    for town, relation in t1.allies_enemies.items():
        if town == t2:
            continue
        if relation == 1:
            allybonus += int(town.resources * 0.2)
            town.resources = int(town.resources * 0.8)

    for town, relation in t2.allies_enemies.items():
        if town == t1:
            continue
        if relation == 1:
            allybonus -= int(town.resources * 0.2)
            town.resources = int(town.resources * 0.8)
        
    for person in HEROS:
        if person.age in range(15, 25) and person.role in ("hunter", "warrior"):
            if person.hometown == t1:
                addHist("{0} accompanies the attackers.".format(person.nametitle))
            if person.hometown == t2:
                addHist("{0} accompanies the defenders.".format(person.nametitle))
            if person.hometown in (t1, t2) and not person.earnedTitle:
                addHist("After the battle, {0} becomes known as {1}.".format(person.name, person.nametitle))
                person.earnedTitle = True
            if person.hometown in (t1, t2) and random.randint(1, 5) == 1:
                addHist("In the fighting, {0} is killed.".format(person.namewithtitle()))
                person.die()
    t2.relations[t1] -= 50
    roll = random.randint(1, 100) + t1.resources - t2.resources + allybonus
    log("Roll is {0} (>50 to succeed)".format(roll))
    if roll <= 50:
        log("Raid failed")
        addHist("However, {0} manages to fight off the attack.".format(t2.name))
        t1.resources -= 7
        t2.resources -= 3
        log("New resources: {0} {1}, {2} {3}".format(t1.name, t1.resources, t2.name, t2.resources))
    else:
        log("Raid succeeded")
        addHist("Warriors of {0} make it into {1} and make off with crates of l00t.".format(t1.name, t2.name))
        amount_raided = int(rand_limit(0.3, 0.7) * t2.resources)
        t1.resources += int(amount_raided * 0.9)
        t2.resources -= amount_raided
    if t1 in t2.trade_routes:
        log("Breaking off trade...")
        addHist("Of course, the citizens of {0} are {1}. Trade between {0} and {2} has stopped.".format(t2.name, random.choice(ANGRY_SYNONYMS), t1.name))

def destroyCity(t1 = None, t2 = None, protectTOWNS = True):
    "t1 destroys t2. Leave blank for random. If protectTOWNS then won't destroy below 5 total towns."
    log("City destroy called")
    global TOWNS
    if protectTOWNS and len(TOWNS) < 6:
        log("Aborting attack to preserve TOWNS")
        return
    if t1 == None:
        cs_in_raid = random.sample(TOWNS, 2)
        t1 = cs_in_raid[0]
        t2 = cs_in_raid[1]
    t2.relations[t1] = -100

    log("Destroy: targets {0} and {1}".format(t1.name, t2.name))
    
    roll = random.randint(1, 100) + t1.resources - t2.resources
    
    todestroy = False
    if t1.relations[t2] <= 0:
        if roll > 50:
            log("Attack succeeded")
            addHist("{0}{1}: The town of {2} destroys the town of {3}, {4}.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name, iFromList(REASONS_TO_ATTACK)))
            todestroy = True
            t1.resources -= random.randint(1, 3) * t2.size
        else:
            log("Attack failed")
            addHist("{0}{1}: The town of {2} attempts to destroy the town of {3}, {4}, but is driven back.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name, iFromList(REASONS_TO_ATTACK)))
            t1.resources -= random.randint(1, 5) * t2.size
            t2.resources -= random.randint(1, 3) * t1.size
    else:
        if roll > 50:
            log("Attack succeeded")
            addHist("{0}{1}: The town of {2} destroys their ally {3}, {4}.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name, iFromList(REASONS_TO_ATTACK)))
            todestroy = True
            t1.resources -= random.randint(1, 3) * t2.size
        else:
            log("Attack failed")
            addHist("{0}{1}: The town of {2} attempts to destroys their ally {3}, {4}, but is driven back.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name, iFromList(REASONS_TO_ATTACK)))
            t1.resources -= random.randint(1, 5) * t2.size
            t2.resources -= random.randint(1, 3) * t1.size
            
    for person in HEROS:
        if person.age in range(15, 25) and person.role in ("hunter", "warrior"):
            if person.hometown == t1:
                addHist("{0} accompanies the attackers.".format(person.nametitle))
            if person.hometown == t2:
                addHist("{0} accompanies the defenders.".format(person.nametitle))
            if person.hometown in (t1, t2) and not person.earnedTitle:
                addHist("After the battle, {0} becomes known as {1}.".format(person.name, person.nametitle))
                person.earnedTitle = True
            if person.hometown in (t1, t2) and random.randint(1, 5) == 1:
                addHist("In the fighting, {0} is killed.".format(person.name))
                person.die()
                
    if todestroy:
        for person in HEROS:
            if person.hometown == t2:
                if random.randint(1, 2) == 1:
                    addHist("{0} is killed by the attackers.".format(person.nametitle))
                    person.die()
                else:
                    person.flee()
                    addHist("{0} flees to {1}.".format(person.nametitle, person.hometown))
        t2.destroy()
        

def foundCity():
    global TOWNS
    global HEROS
    choices = []
    for town in TOWNS:
        if town.resources < 10:
            for i in range(1, 5):
                choices.append(town)
        else:
            choices.append(town)
    target = random.choice(choices)
    log("Founding new city from {0}...".format(target.name))
    addHist("{0}{1}: {2}, {3}s from {4} found a new city on {5}.".format(bce_or_not(currentSimTime), CAL_AB, iFromList(REASONS_TO_LEAVE, TECH_LEVEL), iFromList(ROLES), target.name, target.continent.name))
    newtown = Town(target.continent)
    newtown.relations[target] = random.randint(-10, 10)
    for person in HEROS:
        if person.hometown == target:
            if person.age in range(15, 40) and person.role in ("hunter", "artist", "farmer", "cook", "shaman", "priest", "healer", "herbalist"):
                if random.randint(1, 3) == 1:
                    addHist("Among them is {0}".format(person.nametitle))
                    person.hometown = newtown
    addHist("They decide to call it {0}.".format(newtown.name))
    log("Town founded: {0} at {1}".format(newtown.name, newtown))
    if random.randint(1, 2) == 1:
        log("Old trade set up")
        addHist("They maintain trade with their former hometown.")
        newtown.trade_routes.append(target)
        target.trade_routes.append(newtown)
        

def researchTech():
    "Upgrades tech level to advance history."
    log("Tech up")
    if random.randint(1, 3) != 1: # can be tweaked to make history go faster or shorter
        return
    global TECH_NUM, TECH_LEVEL
    TECH_NUM += 1
    if TECH_NUM > 1:
        TECH_LEVEL = "pass"

def estTrade(t1 = None, t2 = None):
    "Two towns begin trading. Leave at None to be set randomly."
    log("Trade agreement")
    global TOWNS
    if t1 == None:
        cs_in_trade = random.sample(TOWNS, 2)
        t1 = cs_in_trade[0]
        t2 = cs_in_trade[1]
    log("Trade est: targets {0} and {1}".format(t1.name, t2.name))
    if random.randint(1, 2) == 1:
        addHist("{0}{1}: The towns of {2} and {3} decide to establish trade to promote both cities.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name))
    else:
        addHist("{0}{1}: Merchants begin following a route between the towns of {2} and {3}.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name))
    t1.trade_routes.append(t2)
    t2.trade_routes.append(t1)

def breakTrade(t1 = None, t2 = None):
    "Two trading towns stop trading. Leave at None to be chosen randomly."
    log("Trade broken")
    global TOWNS
    if t1 == None:
        cs_in_trade = random.sample(TOWNS, 2)
        t1 = cs_in_trade[0]
        t2 = cs_in_trade[1]
        timeout = 0
    while not t2 in t1.trade_routes:
        cs_in_trade = random.sample(TOWNS, 2)
        t1 = cs_in_trade[0]
        t2 = cs_in_trade[1]
        timeout += 1
        if timeout == 100:
            log("Timeout: Couldn't find 2 cities to trade. Assuming no trade deals exist...")
            return
    log("Trade break: targets {0} and {1}".format(t1.name, t2.name))
    addHist("{0}{1}: Due to unfairly high prices, {2} breaks off trade with {3}".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name))
    t1.trade_routes.remove(t2)
    t2.trade_routes.remove(t1)

def greatRise(role = None, target = None):
    "The birth and childhood of a great hero/celebrity. Role sets their profession, not implemented. Town is where."
    if role == None:
        role = iFromList(ROLES, TECH_LEVEL)
    log("Generating hero...")

    person = Hero(role = role, hometown = target)

    log("Hero: {0} at {1}".format(person.name, person))
    
    addHist("{0}{1}: In the town of {2}, {3} is born.".format(bce_or_not(currentSimTime), CAL_AB, person.hometown.name, person.name))

def formAlliance(t1 = None, t2 = None):
    "Forms an alliance between two default-random cities."
    log("Forming alliance...")
    if t1 == None:
        i = 0
        while True:
            townstouse = random.sample(TOWNS, 2)
            t1 = townstouse[0]
            t2 = townstouse[1]
            if t1 in t2.allies_enemies or t2 in t1.allies_enemies:
                i += 1
                if i > 50:
                    log("Could not find cities to ally, aborting.")
                    return
                continue
            break
    log("Alliance: targets {0} and {1}".format(t1.name, t2.name))
    if t1.relations[t2] < 0 or t2.relations[t1] < 0:
        addHist("{2}{3}: In a historic deal, the towns of {0} and {1} form an alliance with each other.".format(t1.name, t2.name, bce_or_not(currentSimTime), CAL_AB))
    else:
        addHist("{2}{3}: The towns of {0} and {1} form an alliance to benefit both.".format(t1.name, t2.name, bce_or_not(currentSimTime), CAL_AB))
    t1.allies_enemies[t2] = 1
    t2.allies_enemies[t1] = 1
    t1.resources += random.randint(1, 10)
    t2.resources += random.randint(1, 10)

def declareWar(t1 = None, t2 = None, tryResolve = True):
    "Starts a war between two default-random cities. Leave tryResolve at True for a 50% chance to avert war."
    log("Declaring war...")
    if t1 == None:
        i = 0
        while True:
            townstouse = random.sample(TOWNS, 2)
            t1 = townstouse[0]
            t2 = townstouse[1]
            if t1 in t2.allies_enemies or t2 in t1.allies_enemies or t1.resources < 10 or (t1, t2) in WARS or (t2, t1) in WARS:
                i += 1
                if i > 50:
                    log("Could not find cities to ally, aborting.")
                    return
                continue
            break
    log("War: targets {0} and {1}".format(t1.name, t2.name))
    if tryResolve:
        if random.randint(1, 2) == 1: # could be if random.randint(0, 1) but this is easier
            log("Aborting war...")
            addHist("{0}{1}: The towns of {2} and {3} almost go to war, but it's avoided through diplomacy.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name))
            return
    if t1.relations[t2] < 0 or t2.relations[t1] < 0:
        addHist("{2}{3}: After rising tensions, {0} declares war on {1}.".format(t1.name, t2.name, bce_or_not(currentSimTime), CAL_AB))
    else:
        addHist("{2}{3}: The town of {0} suddenly declares war on {1}.".format(t1.name, t2.name, bce_or_not(currentSimTime), CAL_AB))
    t1.allies_enemies[t2] = -1
    t2.allies_enemies[t1] = -1
    t1.resources -= random.randint(1, 10)
    t2.resources -= random.randint(1, 10)
    WARS.append((t1, t2))
    
def evalTowns():
    log("Evaluating towns...")
    average_res = 0
    for town in TOWNS:
        average_res += town.resources
    average_res /= len(TOWNS)
    for town in TOWNS:
        if town.resources < (average_res * 0.1): # if city is very below average resources
            log("{0} low on resources".format(town.name))
            addHist("Starvation is rampant in {0} due to lack of resources. Many either die or leave.".format(town.name))
            town.size -= random.randint(1, 2)
            if town.size <= 0:
                addHist("{0} becomes abandoned.".format(town.name))
                town.destroy()
                if len(TOWNS) < 6:
                    refnewtown = Town(town.continent)
                    addHist("Refugees found the town of {0}.".format(refnewtown.name))
        elif town.resources > (average_res * 1.5): # town is very above average resources
            log("{0} high on resources".format(town.name))
            addHist("{0} grows rich and attracts people, causing them to expand.".format(town.name))
            town.size += random.randint(1, 3)
        for target in town.trade_routes:
            target.resources += random.randint(1, 3)
            try:
                town.relations[target] += 5
            except:
                log("Could not find town {0} as {1}. Removing relations...".format(target.name, target))
                town.trade_routes.remove(target)

def evalPeople():
    log("Evaluating people...")
    for person in HEROS:
        person.age = currentSimTime - person.birthdate
        if TECH_LEVEL == "agriculture":
            if person.age > 10 and not person.earnedTitle:
                person.earnedTitle = True
                addHist("{0} becomes known as {1} after {2}.".format(person.name, person.nametitle, person.earntitle()))
            if person.age > 20 and random.randint(1, 5) == 1:
                log("{0} dies".format(person.name))
                addHist("{0} dies of old age".format(person.name))
                person.die()

def evalWars():
    log("Evaluating wars...")
    for war_towns in WARS:
        log("Evaluating {0}".format(war_towns))
        for i in range(1, 3):
            if random.randint(1, 2) == 1:
                battleeventnum = random.randint(1, 10)
                if battleeventnum in range(1, 6):
                    log("Attack rolled")
                    if battleeventnum in range(1, 3):
                        t1 = war_towns[0]
                        t2 = war_towns[1]
                    else:
                        t1 = war_towns[1]
                        t2 = war_towns[0]
                    roll = random.randint(1, 100) + t1.resources - t2.resources
                    for town, relation in t1.allies_enemies.items():
                        if relation == 1:
                            roll += int(0.8 * town.resources)
                            town.resources *= 0.9
                    for town, relation in t2.allies_enemies.items():
                        if relation == 1:
                            roll -= int(0.8 * town.resources)
                            town.resources *= 0.9
                    if roll > 50:
                        addHist("{0} attacks {1} at the {2}. The attack succeeds.".format(war_towns[0].name, war_towns[1].name, random.choice(war_towns[1].locations)))
                        t1.resources += 10
                        t2.resources -= 20
                    else:
                        addHist("{0} attacks {1} at the {2}. The attack fails.".format(war_towns[0].name, war_towns[1].name, random.choice(war_towns[1].locations)))
                        t1.resources -= 20
                        t2.resources += 10
                elif battleeventnum == 7:
                    log("Mercenaries rolled (1)")
                    addHist("{0} hires mercenaries to raid {1}.".format(war_towns[0].name, war_towns[1].name))
                    war_towns[0].resources -= 10
                    war_towns[1].resources -= 30
                elif battleeventnum == 8:
                    log("Mercenaries rolled (2)")
                    addHist("{0} hires mercenaries to raid {1}.".format(war_towns[1].name, war_towns[0].name))
                    war_towns[1].resources -= 10
                    war_towns[0].resources -= 30
                elif battleeventnum == 9:
                    log("Stalemate rolled")
                    places = []
                    for town in war_towns:
                        town.resources -= random.randint(5, 15)
                        for place in town.locations:
                            places.append(place)
                    addHist("{0} and {1} fight for a while at {2} with no clear winner.".format(war_towns[0].name, war_towns[1].name, random.choice(places)))
                elif battleeventnum == 10:
                    log("Treaty rolled")
                    avg = 0
                    for town in TOWNS:
                        avg += town.resources
                    avg /= len(TOWNS)
                    if war_towns[0].resources < 0.5 * avg and war_towns[1].resources < 0.5 * avg:
                        addHist("After long, hard fighting, the populations of {0} and {1} are too poor to continue fighting.".format(war_towns[0].name, war_towns[1].name))
                        WARS.remove((war_towns[0], war_towns[1]))
                        return
                    elif war_towns[0].resources < 0.5 * avg:
                        addHist("{0} surrenders to {1} and gives up the following territories:".format(war_towns[0].name, war_towns[1].name))
                        for i in range(1, int(rand_limit(0.3, 0.6) * len(war_towns[0].locations))):
                            if len(war_towns[0].locations) <= 1: # Shouldn't happen, but just in case...
                                continue
                            territory = random.choice(war_towns[0].locations)
                            war_towns[0].locations.remove(territory)
                            war_towns[1].locations.append(territory)
                            addHist(territory)
                        WARS.remove((war_towns[0], war_towns[1]))
                        return
                    elif war_towns[1].resources < 0.5 * avg:
                        addHist("{0} surrenders to {1} and gives up the following territories:".format(war_towns[1].name, war_towns[0].name))
                        for i in range(1, int(rand_limit(0.3, 0.6) * len(war_towns[1].locations))):
                            if len(war_towns[1].locations) <= 1: # Shouldn't happen, but just in case...
                                continue
                            territory = random.choice(war_towns[1].locations)
                            war_towns[1].locations.remove(territory)
                            war_towns[0].locations.append(territory)
                            addHist(territory)
                        WARS.remove((war_towns[0], war_towns[1]))
                        return
                    else:
                        which = random.randint(0, 1)
                        capturer = war_towns[which]
                        loser = war_towns[which - 1]
                        territory = random.choice(loser.locations)
                        addHist("{0} captures the {1} from {2}.".format(capturer, territory, loser))
                        try:
                            loser.locations.remove(territory)
                            capturer.locations.append(territory)
                        except:
                            addHist("However, it's quickly recaptured.")
    
# ---------------------------------------
# Current step order:
# genWorld()
# beginAgric()
# Begin the pool of events:
# -Adds towns can attack
# -Trade alliances can form
# Evaluate resources every so often
# ---------------------------------------

genWorld()
beginAgric()

currentSimTime = -begintime

TECH_NUM = 0
TECH_LEVEL = "agriculture"

action_options = (raidTown, foundCity, researchTech, estTrade, breakTrade, destroyCity, formAlliance, declareWar, greatRise, greatRise)
while TECH_LEVEL == "agriculture":
    checkTech = TECH_LEVEL
    for i in range(1, random.randint(2, 6)):
        action = random.choice(action_options)
        action()
        if checkTech != TECH_LEVEL:
            break
        evalWars()
        currentSimTime += random.randint(1, 25)
    evalTowns()
    evalPeople()

# ---------------------------------------

print("Your history is saved at: ", end = "")
print(histfile.name)

# Closes the log and history files to save changes
logfile.close()
histfile.close()
