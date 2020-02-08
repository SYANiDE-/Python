#!/usr/bin/env python2
import os, sys, time, importlib

## The point is:
## program.py would compile with testing.py.  However what do we do when we have, let's say, want to constantly update testing.py?  If program.py is compiled by PyInstaller --onefile, this would freeze testing.py as well.  With this demo application, it is demonstrated how to compile into --onefile, and dynamically at runtime, look for ext_testing.py to use in place of testing.py.  This works.
## ext_testing.py should not exist at compile time.  This way, all references attempt to point to testing.py at compile time.  Then, when testing.py is updated, copy it to ext_testing.py to have program include it instead of frozen testing.py.


def test():
    print("This is a test")
    if os.path.isfile("ext_testing.py"):
	sys.path.append(os.getcwd())
        from ext_testing import * 
    else:
        from testing import *
    print(thetest())
    


if __name__=="__main__":
	test()
	
