#!/usr/bin/env python2
import sys
#_  brute force iteration through caesars cipher on a given string.


def bf_caesar(incrementor):
    ciphertext = """this is a test of the emergency broadcast system""" if not len(sys.argv) > 1 else sys.argv[1]
    note = "" if not incrementor == 95 else " ## original ciphertext"
    plaintext = ""
    for char in ciphertext:
        glyph = (ord(char)-incrementor) % 126
        if glyph < 32:
            glyph +=95
        plaintext+=chr(glyph)
    print(plaintext+note)


for i in range(1,96,1):
    bf_caesar(i)
print("")
