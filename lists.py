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

ANIMALS = {"land_prey_large":("boar", "deer", "buffalo", "giraffe"),
           "land_prey_small":("rabbit"),
           "land_predator":("lion", "tiger", "leopard", "hyena"),
           "bird_predator":("owl", "eagle", "hawk", "vulture", "falcon"),
           "bird_prey":("sparrow", "finch", "hummingbird", "crow", "raven", "blue jay", "cardinal"),
           "fish":("trout", "salmon", "flounder"),
           "sea":("shark", "octopus")}

REASONS_TO_LEAVE = {"hunt&gath":("following the {0} herds".format(random.choice(ANIMALS["land_prey_large"])),
                                 "crossing a land bridge", "looking for a better hunting ground"),
                    "agriculture":("seeking better farmland", "looking for a new place to settle")}

ROLES = {"hunt&gath":("hunter", "gatherer", "healer", "shaman")}

GROUPS = {"hunt&gath":("tribe", "clan", "band", "pack")}

NOUNS = {"singular":("bird", "bee", "bug", "animal", "food", "club", "spice", "sword", "rock", "sand", "dirt", "coal", "sky"),
                    "plural":("birds", "bees", "bugs", "animals", "foods", "clubs", "spices", "swords", "rocks", "sands", "dirts", "coals", "skies")}

VERBS = {"1stsin":("call", "run", "am", "was", "want", "eat", "drink", "die", "read", "play", "fall", "slap", "skip"),
         "2ndsin/3rdpl":("call", "run", "are", "were", "want", "eat", "drink", "die", "read", "play", "fall", "slap", "skip"),
         "3rdsin":("calls", "runs", "is", "was", "eats", "drinks", "dies", "reads", "plays", "falls", "slap", "skips"),
         "unconj":("to call", "to run", "to be", "to have been", "to eat", "to drink", "to die", "to read", "to play", "to fall", "to slap", "to skip")}

QW_CLAUSES = {"where":('"where {0} {1}".format(iFromList(NOUNS, "plural"), iFromList(VERBS, "2ndsin/3rdpl"))', '"where the {0} {1}".format(iFromList(NOUNS, "plural"), iFromList(VERBS, "2ndsin/3rdpl"))'),
              "who":(),
              "when":(),
              "why":(), # why and how could both be for names of gods
              "what":(),
              "how":()}
