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

def genName():
    name = ""

    maxlen = random.randint(3, 6)
    
    while len(name) < maxlen:
        name += random.choice(phonemes)

    return name.title()

def iFromList(dictname, keyname = "all"):
    if keyname == "all":
        choices = []
        for key, value in dictname.iteritems():
            for item in value:
                choices.append(item)
        return random.choice(choices)
    else:
        return random.choice(dictname[keyname])

# Initialize log
prev_logs = len(os.listdir("./Records/Logs/")) - 1
logfile = open("./Records/Logs/log_" + str(prev_logs) + '.txt', 'w')

INIT_TIME = time.time() # starting time in seconds since epoch, to be subtracted from log times

def log(text):
    logfile.write(str(time.time() - INIT_TIME) + ": ")
    logfile.write(str(text))
    logfile.write("\n\n")
    logfile.flush()

now = datetime.datetime.now() # Current time (when this is called)
log("Log initialized at {0}-{1}-{2} at {3}:{4}:{5} using HistoryGen version 0.1!".format(now.year, now.month, now.day, now.hour, now.minute, now.second))

# Initialize history file
histfile = open("./Records/Histories/hist_" + str(prev_logs) + '.txt', 'w')

def addHist(text):
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

# Step 1: Generate continents
CONTINENTS = []
for i in range(0, random.randint(3, 9)):
    CONTINENTS.append(Continent())

# Step 2: Generate the evolution of each race.
def genWorld():
    # For now, this is the only case.
    # Begin to generate history, starting with the planet's creation,
    # then the first life, then first land life, then first humans.
    # Has no bearing on the generation except for first humans
    
    log("Generating starting history...")
    
    addHist("A small star, approximately 1 AU away. A ball of debris slowly grow larger and eventually forms into a planet.")
    addHist("Continents form, weather patterns form, all that great stuff.")
    addHist("A chance meeting of molecules forms the first amino acid.")
    addHist("An even more chance meeting forms the first eukaryote.")
    
    addHist("Before long, life is born.\n\n")

    # Generate where the first humans evolve.
    firstCont = random.choice(CONTINENTS)
    addHist("The first humans evolve on continent {0}.".format(firstCont.name))
    firstCont.inhabited = True

    log("Adding humans to continents...")
    
    for cont in CONTINENTS:
        if not cont.inhabited and random.randint(1, 8) != 1:
            addHist(str(random.randint(1000, 10000)) + " years later, "
                    + iFromList(REASONS_TO_LEAVE, "hunt&gath")
                    + ", {0}s of the {1} {2} discover the continent {3}. They call it {4} {5}, meaning '{6}'."
                    .format(iFromList(ROLES, "hunt&gath"), iFromList(GROUPS, "hunt&gath"),
                            genName(), cont.name, genName(), genName(), eval(iFromList(QW_CLAUSES, "where"))))
            cont.inhabited = True


# ---------------------------------------
# Current step order:
# genWorld()
# ---------------------------------------

genWorld()


# ---------------------------------------

print("Your history is saved at: ", end = "")
print(histfile.name)

# Closes the log and history files to save changes
logfile.close()
histfile.close()
print(len(CONTINENTS))
