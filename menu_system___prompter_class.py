#!/usr/bin/env python
import os, sys, re, json
from colorama import Fore, Back


class menu():
	def __init__(s):
		pass
	def index_userin(s,question,valids=[]):
		""" Takes a question to prompt the user with, and list of possible options, returns an index to that list"""
		uin = 0
		if len(valids) > 0:
			exits = ['cancel','quit']
			while uin not in range(1,len(valids)+1+len(exits)):
				ct = 1
				print("[.] %s" % question)
				for item in valids:
					print("\t%d\t%s" % (ct,item))
					ct += 1
				for item in exits:
					print("\t%d\t%s" % (ct,item))
					ct+= 1
				try:
					uin = int(raw_input(":> "))
					if type(uin) == int and uin not in range(1,len(valids)+len(exits)+1):
						print("\n%s[!] Expected input in range(1,%s)%s\n" % (Fore.RED+Back.YELLOW,str(len(valids)+len(exits)),Fore.RESET+Back.RESET))
						uin=0
					if uin in range(len(valids)+1,len(valids)+1+len(exits)):
						if uin not in range(1,len(valids)+1):
							uin = uin - (len(valids)+1)
							if "cancel" in exits[uin]:
								return -1
							if "quit" in exits[uin]:
								sys.exit()
				except ValueError:
					print("\n%s[!] ERROR: Expected numerical input%s\n" % (Fore.RED+Back.YELLOW, Fore.RESET+Back.RESET))
				except:
					pass
			return uin-1
		return None

	
def main():
	m = menu()
	print(m.index_userin("Is this memey?", ['what','whatwhat','what the whatwhat']))


if __name__=="__main__":
	main()
