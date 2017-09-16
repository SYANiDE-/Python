#!/usr/bin/env python2
import random, sys

bangbang="""
BBBBBBBBBBBBBBBBB               AAA               NNNNNNNN        NNNNNNNN        GGGGGGGGGGGGG !!! 
B::::::::::::::::B             A:::A              N:::::::N       N::::::N     GGG::::::::::::G!!:!!
B::::::BBBBBB:::::B           A:::::A             N::::::::N      N::::::N   GG:::::::::::::::G!:::!
BB:::::B     B:::::B         A:::::::A            N:::::::::N     N::::::N  G:::::GGGGGGGG::::G!:::!
  B::::B     B:::::B        A:::::::::A           N::::::::::N    N::::::N G:::::G       GGGGGG!:::!
  B::::B     B:::::B       A:::::A:::::A          N:::::::::::N   N::::::NG:::::G              !:::!
  B::::BBBBBB:::::B       A:::::A A:::::A         N:::::::N::::N  N::::::NG:::::G              !:::!
  B:::::::::::::BB       A:::::A   A:::::A        N::::::N N::::N N::::::NG:::::G    GGGGGGGGGG!:::!
  B::::BBBBBB:::::B     A:::::A     A:::::A       N::::::N  N::::N:::::::NG:::::G    G::::::::G!:::!
  B::::B     B:::::B   A:::::AAAAAAAAA:::::A      N::::::N   N:::::::::::NG:::::G    GGGGG::::G!:::!
  B::::B     B:::::B  A:::::::::::::::::::::A     N::::::N    N::::::::::NG:::::G        G::::G!!:!!
  B::::B     B:::::B A:::::AAAAAAAAAAAAA:::::A    N::::::N     N:::::::::N G:::::G       G::::G !!! 
BB:::::BBBBBB::::::BA:::::A             A:::::A   N::::::N      N::::::::N  G:::::GGGGGGGG::::G     
B:::::::::::::::::BA:::::A               A:::::A  N::::::N       N:::::::N   GG:::::::::::::::G !!! 
B::::::::::::::::BA:::::A                 A:::::A N::::::N        N::::::N     GGG::::::GGG:::G!!:!!
BBBBBBBBBBBBBBBBBAAAAAAA                   AAAAAAANNNNNNNN         NNNNNNN        GGGGGG   GGGG !!! 
"""
exits = ['q', 'e']
re = "####"
cylinder = 6
firing_pin = 0
rand = [i for i in range(1,7)]
for i in range(0, random.randint(1, 9999)):
    random.shuffle(rand)


def trigger(pin):
    bullet = rand[pin]
    if (int(bullet)%6) == 0:
        print(bangbang + "\nYou died.  Your family weeps at your misfortune\n")
        sys.exit(0)
    else:
        print("Your lucky day...")
        return pin+1


while not re.lower() in exits and cylinder != 0:
    if cylinder == 6:
        print("\n#### Rules ####\n\t1. Don't die.\n\t2. [Emter] key to pull the trigger.\n\t3. Exit with '[e] [enter]', '[q] [enter]'.\n\n")
    re = raw_input("%i shots left... your move, kid.:  " %  cylinder)
    firing_pin = trigger(firing_pin)
    cylinder -= 1
