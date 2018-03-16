# This program generates a name from random phonemes. Each phoneme is either
# consonant-vowel-consonant, v-c, or c-v. Very quick-and-dirty but it seems
# to work better than my original system.

import random

# Phoneme list obtained from a quick-and-dirty generator
# Offloaded to an exec'd text file for easy editing
# and so changes to the file are easy to make.
# phonemes doesn't use certain rare letters
# phonemeswithrares does.
codetoexec = open('phonemeswithrares.txt', 'r').read()
exec(codetoexec)

def genName():
    name = ""

    maxlen = random.randint(3, 6)
    
    while len(name) < maxlen:
        name += random.choice(phonemes)

    record = open("Records/Generated Names.txt", "a")
    record.write(name.title())
    record.write("\n\n")
    record.close()

    return name.title()

if __name__ == "__main__": # Could be imported into another proj
    print(genName()) # Importing was the original idea
