def iFromList(dictname, keyname = "all"): # same as in the main file, but has to be here as well
    if keyname == "all":
        choices = []
        for key, value in dictname.iteritems():
            for item in value:
                choices.append(item)
        return random.choice(choices)
    else:
        return random.choice(dictname[keyname])

# !!!!!!!!!!!!
# Items that contain randomly-generated elements must be strings of code,
# that are then eval()'d later. I'm trying to find a better way.
# !!!!!!!!!!!!

BIOMETYPES = ('deciduous forest', 'evergreen forest', 'desert',
              'marsh', 'grasslands', 'mountains', 'tundra',
              'hills')

ANIMALS = {"land_prey_large":("boar", "deer", "buffalo", "giraffe", "hippo", "bison", "gorilla", "ape", "kangaroo"),
           "land_prey_small":("rabbit", "squirrel", "monkey"),
           "land_predator":("lion", "tiger", "leopard", "hyena", "jaguar", "cougar", "wolf"),
           "bird_predator":("owl", "eagle", "hawk", "vulture", "falcon"),
           "bird_prey":("sparrow", "finch", "hummingbird", "crow", "raven", "blue jay", "cardinal", "duck", "goose", "swallow", "blackbird", "robin"),
           "fish":("trout", "salmon", "flounder", "bass", "tilapia", "carp", "catfish", "mackerel", "mahi-mahi"),
           "sea":("shark", "octopus", "squid", "shrimp", "sea snail", "plankton"),
           "other":(),
           "tame":("dog", "cat", "horse")}

PLANTS = {"vegetables":("onion", "lettuce", "kale", "broccoli", "spinach", "turnip", "celery", "asparagus", "artichoke", "eggplant", "avocado", "tomato", "pepper", "garlic"),
          "fruits":("strawberry", "raspberry", "orange", "lemon", "grapefruit", "grape", "blackberry", "blueberry", "mango", "lychee", "clementine", "apricot", "olive", "peach", "nectarine"),
          "herbs":("oregano", "thyme", "pepper", "basil", "parsley", "cilantro", "dill", "sage", "tarragon")}

REASONS_TO_LEAVE = {"hunt&gath":("following the {0} herds".format(random.choice(ANIMALS["land_prey_large"])),
                                 "crossing a land bridge", "looking for a better hunting ground", "crossing a wide river", "exploring out of curiosity", "fleeing pursuers"),
                    "agriculture":("seeking better farmland", "looking for a new place to settle")}

ROLES = {"hunt&gath":("hunter", "gatherer", "healer", "shaman", "forager", "youth")}

GROUPS = {"hunt&gath":("tribe", "clan", "band", "pack")}

NOUNS = {"singular":("bird", "bee", "bug", "animal", "food", "club", "spice", "sword", "rock", "sand", "dirt", "coal", "sky", "leaf", "pebble", "plant", "rain", "lightning", "light", "thunder", "fish", "child"),
                    "plural":("birds", "bees", "bugs", "animals", "foods", "clubs", "spices", "swords", "rocks", "sands", "coals", "skies", "leaves", "pebbles", "plants", "rains", "lights", "fish", "children")}
NOUNS["other"] = [] # Yes, I know I'm editing a constant. Freakin' sue me.
for key, value in ANIMALS.items():
    for item in value:
        NOUNS["other"].append(item)
for key, value in PLANTS.items():
    for item in value:
        NOUNS["other"].append(item)

VERBS = {"1stsin":("call", "run", "am", "was", "want", "eat", "drink", "die", "read", "play", "fall", "slap", "skip", "walk", "sing", "fight", "bash", "lead", "fall", "strike", "roar", "change", "speak", "talk", "preach"),
         "2ndsin/3rdpl":("call", "run", "are", "were", "want", "eat", "drink", "die", "read", "play", "fall", "slap", "skip", "walk", "sing", "fight", "bash", "lead", "fall", "strike", "roar", "change", "speak", "talk", "preach"),
         "3rdsin":("calls", "runs", "is", "was", "eats", "drinks", "dies", "reads", "plays", "falls", "slaps", "skips", "walks", "sings", "fights", "bashes", "leads", "falls", "strikes", "roars", "changes", "speaks", "talks", "preaches"),
         "unconj":("to call", "to run", "to be", "to have been", "to eat", "to drink", "to die", "to read", "to play", "to fall", "to slap", "to skip", "to walk", "to sing", "to fight", "to bash", "to lead", "to fall", "to strike", "to roar", "to change", "to speak", "to talk", "to preach")}

QW_CLAUSES = {"where":('"where {0} {1}".format(iFromList(NOUNS, "plural"), iFromList(VERBS, "2ndsin/3rdpl"))', '"where the {0} {1}".format(iFromList(NOUNS, "plural"), iFromList(VERBS, "2ndsin/3rdpl"))', '"where {0} and {1} {2}".format(iFromList(NOUNS, "plural"), iFromList(NOUNS, "plural"), iFromList(VERBS, "2ndsin/3rdpl"))', '"where the {0} {1}".format(iFromList(NOUNS, "singular"), iFromList(VERBS, "3rdsin"))'),
              "who":('"who {0} the {1}".format(iFromList(VERBS, "3rdsin"), iFromList(NOUNS, "plural"))', '"who {0} {1}".format(iFromList(VERBS, "3rdsin"), iFromList(NOUNS, "plural"))', '"who {0} the {1}".format(iFromList(VERBS, "3rdsin"), iFromList(NOUNS, "singular"))', '"who {0} {1}".format(iFromList(VERBS, "3rdsin"), iFromList(NOUNS, "singular"))', '"who speaks with the {0}".format(iFromList(ANIMALS))'), # famous people's names/titles
              "when":('"when the {0} {1}".format(iFromList(NOUNS, "singular"), iFromList(VERBS, "3rdsin"))', '"when the {0} {1}".format(iFromList(NOUNS, "plural"), iFromList(VERBS, "2ndsin/3rdpl"))'),
              "why":('"why the {0} {1}".format(iFromList(NOUNS, "plural"), iFromList(VERBS, "2ndsin/3rdpl"))', '"why the {0} {1}".format(iFromList(NOUNS, "singular"), iFromList(VERBS, "3rdsin"))', '"why the {0} {1}".format(iFromList(NOUNS, "singular"), iFromList(VERBS, "3rdsin"))'), # why and how could both be for names of gods
              "what":('"what the {0} {1}".format(iFromList(NOUNS, "plural"), iFromList(VERBS, "2ndsin/3rdpl"))', '"what the {0} {1}".format(iFromList(NOUNS, "singular"), iFromList(VERBS, "3rdsin"))', '"what the {0} {1}".format(iFromList(NOUNS, "singular"), iFromList(VERBS, "3rdsin"))'),
              "how":('"how the {0} {1}".format(iFromList(NOUNS, "plural"), iFromList(VERBS, "2ndsin/3rdpl"))', '"how the {0} {1}".format(iFromList(NOUNS, "singular"), iFromList(VERBS, "3rdsin"))', '"how the {0} {1}".format(iFromList(NOUNS, "singular"), iFromList(VERBS, "3rdsin"))')}
