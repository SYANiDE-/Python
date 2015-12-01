"""Creates a printing object to handle various printing and prompting."""
from blessings import Terminal
from string import lower
from types import FloatType
import string


class ColorPrompt:

    def __init__(self):
        self.__term = Terminal()
        self.__succ = "{t.normal}{t.green}{}{t.normal}".format     # green
        self.__fail = "{t.bold}{t.red}{}{t.normal}".format         # red
        self.__warn = "{t.bold}{t.yellow}{}{t.normal}".format      # yellow
        self.__info = "{t.normal}{t.grey}{}{t.normal}".format      # grey
        self.__norm = "{t.normal}{}{t.normal}".format              # explicit normal (clear)
        self.__s = "[+] "
        self.__f = "[x] "
        self.__w = "[!] "
        self.__i = "[...] "
        self.__q = "[?] "
        self.__n = "[.] "

    def state(self, strng, ty="", spec=0, lb=0):
        """Print something.

            ty(pe):
            s = success     (green)
            f = fail        (red)
            w = warn        (yellow)
            i = info        (grey)
            default is normal.

            spec:
            1 = normal
            2 = bold
            3 = blink
            4 = underline
            5 = reverse
            default is default

            lb = line breaks after."""
        one = self.__info if ty == lower("i") else self.__succ if ty == lower("s") else self.__warn if ty == lower("w") else self.__norm
        two = self.__i if ty == lower("i") else self.__s if ty == lower("s") else self.__w if ty == lower("w") else self.__n
        three = self.__term.normal if spec == 1 else self.__term.bold if spec == 2 else self.__term.blink if spec == 3 else self.__term.underline if spec == 4 else self.__term.reverse if spec == 5 else ""
        print(one(two + three + strng, t=self.__term))
        if lb > 0:
            for i in range(0, lb):
                print("")

    def prompt(self, strng, ret="s", spec=0, lb=0):
        """Prompt the user, return their input.  Will not return until user input matches return type requested.

        ret:
        s (default)     string
        sn              string; numeric-only
        sa              string; alpha-only
        sp              string; punctuation-only
        i               int
        f               float
        b               boolean

        spec:
        1 = normal
        2 = bold
        3 = blink
        4 = underline
        5 = reverse
        default is default

        lb = line breaks after."""
        one = self.__warn
        two = self.__w
        three = self.__term.normal if spec == 1 else self.__term.bold if spec == 2 else self.__term.blink if spec == 3 else self.__term.underline if spec == 4 else self.__term.reverse if spec == 5 else ""
        provided = None
        this = None
        bools = ["1", "0", "y", "n", "t", 'f', "Y", "N", "T", "F"]

        def say():
            print(one(two + three + strng, t=self.__term))
            print(self.__info(self.__q + three + ":  ", t=self.__term)),
        say()
        provided = raw_input().rstrip("\n")
        ret = lower(ret)
        if ret != "s":
            if ret == "sn":
                while not provided.isdigit():
                    print("")
                    print(self.__fail(self.__f + "Error! Input not strictly numeric.", t=self.__term))
                    say()
                    provided = raw_input().rstrip("\n")
            if ret == "sa":
                while not provided.isalpha():
                    print("")
                    print(self.__fail(self.__f + "Error! Input not strictly alpha.", t=self.__term))
                    say()
                    provided = raw_input().rstrip("\n")
            if ret == "sp":
                while not provided in string.punctuation:
                    print("")
                    print(self.__fail(self.__f + "Error! Input not strictly punctuation.", t=self.__term))
                    say()
                    provided = raw_input()
            if ret == "i":
                while not provided.isdigit:
                    print("")
                    print(self.__fail(self.__f + "Error! Input not strictly numeric.", t=self.__term))
                    say()
                    provided = raw_input().rstrip("\n")
                provided = int(provided)
            if ret == "f":
                if float(provided):
                    pass
                else:
                    while type(provided) != FloatType:
                        print("")
                        print(self.__fail(self.__f + "Error! Input not strictly numeric.", t=self.__term))
                        say()
                        provided = raw_input().rstrip("\n")
                provided = float(provided)
            if ret == "b":
                while provided[:1] not in bools:
                    print("")
                    print(self.__fail(self.__f + "Error! Input not very booleanic.", t=self.__term))
                    say()
                    provided = raw_input().rstrip("\n")
                if provided[:1] == "1" or provided[:1] == "t" or provided[:1] == "T" or provided[:1] == "y" or provided[:1] == "Y":
                    provided = True
                elif provided[:1] == "0" or provided[:1] == "f" or provided[:1] == "F" or provided[:1] == "n" or provided[:1] == "N":
                    provided = False
        if lb > 0:
            for i in range(0, lb):
                print("")
        return provided
