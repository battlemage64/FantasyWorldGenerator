import random # Used, of course, for random generation.
import os # Used to navigate directories to save logs and histories in order.
import datetime # Used for logging when the file was made
import time # Used for keeping fraction-of-a-second-accurate log times

# These constants control which things are generated.
# Easier to have defaults than to input them each time
GEN_HUMANS = True
GEN_DWARVES = False # To be implemented
GEN_ELVES = False # T be implemented
GEN_CUSTOM_RACE = False # To be implemented, a race with a randgen name
NUM_CUSTOM_RACES = 0 # Number of above

LISTS = open("lists.py", "r").read() # Gets lists of items from lists.py
exec(LISTS) # Because lists.py will probably become frickin' huge
del LISTS # lists.py won't work on its own, only meant to be read

GETPHONEMES = open('phonemeswithrares.txt', 'r').read()
exec(GETPHONEMES)
del GETPHONEMES # just good practice not to have this thing floating around

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

def genName():
    "Generates a random name from phonemes"
    name = ""

    maxlen = random.randint(3, 6)
    
    while len(name) < maxlen:
        name += random.choice(phonemes)

    return name.title()

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
        self.name = genName()
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

class Town:
    "A town on a continent"
    def __init__(self, continent = None):
        self.name = genName()
        if continent == None:
            self.continent = random.choice(CONTINENTS)
        else:
            self.continent = continent
        self.previousNames = []
        self.propagate()
        global towns
        towns.append(self)
        self.propagate()
    def changeName(self, return_name):
        "Change the name of a city, record the old name, and possibly return the new name"
        self.previousNames.append(self.name)
        self.name = genName()
        if return_name:
            return self.name
    def propagate(self):
        self.relations = {}
        for town in TOWNS:
            if town == self:
                continue
            self.relations[town] = 0
            town.relations[self] = 0
    def destroy(self):
        "Should be called upon the city's destruction."
        global TOWNS
        for town in TOWNS:
            if town == self:
                continue
            del town.relations[self]
        TOWNS.remove(self)

# Step 1: Generate continents
CONTINENTS = []
for i in range(0, random.randint(3, 9)):
    CONTINENTS.append(Continent())

towns = [] # master list of towns, for later

log("Creating calendar...")
cal_cre_fn = genName() # Calendar creator's first and last name, and origin town
cal_cre_ln = genName()
cal_cre_org = genName()
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
    
    addHist("Before long, life is born.\n\n")

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
                            genName(), cont.name, genName(), genName(), eval(iFromList(QW_CLAUSES, "where"))))
            cont.inhabited = True
            ago *= rand_limit(0.5, 1) # Next one will be more recent
            ago = round(ago, 2) # Rounds it so it's not super long
    log("World generation finished, continents inhabited")

def beginAgric():
    log("Discovering agriculture...")
    cont_where = random.choice(CONTINENTS)
    global begintime
    begintime = random.randint(9000, 20000)
    addHist("{0} B{1}, in {2}: The {3} {4} notice that {5} plants have grown where they dropped seeds last year.".format(begintime, CAL_AB, cont_where.name, genName(), iFromList(GROUPS, "hunt&gath"), iFromList(PLANTS)))
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
        for cont in CONTINENTS:
            for i in range(2, 5):
                newtown = Town(cont)
                log("Town {0} created as {1}".format(newtown.name, newtown))

def raid_town(t1 = None, t2 = None):
    "One town raids another town. Leave at None to be set randomly."
    log("City attack called")
    if t1 == None:
        t1 = random.choice(TOWNS)
    checker = False
    for key, value in t1.relations.items():
        if value <= 0:
            checker = True
    if not checker:
        log("No valid cities found, aborting city attack")
        return
    t2 = t1
    while t2 == t1:
        t2 = random.choice(TOWNS)
        if t1.relations[t2] >= 0:
            t2 = t1 # mark to be reassigned
    log("City raid: Cities chosen {0} raids {1}".format(t1.name, t2.name))
    addHist("{0}{1}: The town of {2} raids the town of {3}.".format(bce_or_not(currentSimTime), CAL_AB, t1.name, t2.name))    
    t2.relations[t1] -= 50
    
# ---------------------------------------
# Current step order:
# genWorld()
# beginAgric()
# Begin the pool of events:
# -Adds towns can attack
# -Trade alliances can form
# ---------------------------------------

genWorld()
beginAgric()

currentSimTime = -begintime

TECH_LEVEL = "agric"

action_options = (raid_town)
while TECH_LEVEL == "agric":
    action = random.choice(action_options)
    action()
    currentSimTime += random.randint(1, 100)

# ---------------------------------------

print("Your history is saved at: ", end = "")
print(histfile.name)

# Closes the log and history files to save changes
logfile.close()
histfile.close()
