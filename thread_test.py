#!/usr/bin/env python2
import os, sys, random, threading, time

ints = []


def sleeper_cell(x):
	a = random.randint(1,20)
	time.sleep(a)
	print("Thread %s finished after %s secs" % (x,a))

for x in range(1,6):
	thread = threading.Thread(target=sleeper_cell, args=(x,))
	# thread.setDaemon(True)
	ints.append(thread)

for thr in ints:
	thr.start()


	
	




