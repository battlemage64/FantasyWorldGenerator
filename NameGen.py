# letter frequencies from Cornell 
#http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html

import random

def genName():
    cons = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'y', 'rare', 'digraph', 'digraph', 'digraph']
    rares = ['q', 'z', 'qu']
    digraphs = ['ck', 'ch', 'sh', 'th']
    vowels = ['a', 'a', 'e', 'e', 'e', 'e', 'i', 'i', 'o', 'o', 'u']
    # aio are more common than u, and e is most common. inelegant solution but wtf

    lastcons = 0
    lastvowels = 0
    hasvowel = False

    word = ""

    for i in range(random.randint(4, 7)):
      choice = random.randint(1, 5)

      if choice in (1, 2):
        if lastvowels >= 2:
          i -= 1
          continue
        letter = random.choice(vowels)
        lastcons = 0
        lastvowels += 1
      elif choice in (3, 4, 5):
        if lastcons >= 2:
          i -= 1
          continue
        letter = random.choice(cons)
        if letter == 'rare':
          letter = random.choice(rares) # rare letter
        if letter == 'digraph':
          letter = random.choice(digraphs) # digraph
        lastvowels = 0
        lastcons += 1

      word += letter
      
    if not hasvowel:
      word += random.choice(vowels)

    return word.title()

if __name__ == '__main__':
    name = genName()
    print(name)
    record = open("Records/Generated Names.txt", "a")
    record.write(name)
    record.write("\n\n")
    record.close()

