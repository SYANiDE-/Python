#!/usr/bin/env python2.7
import argparse as ap, subprocess, sys
from concurrent import futures

p = ap.ArgumentParser(description=('Ping sweep a range in a net.'))
p.add_argument('-n', '--net', help="Network [first three octets]", type=str)
p.add_argument('-s', '--start', help="4th octet start", type=int)
p.add_argument('-e', '--end', help="4th octet end", type=int)
a=p.parse_args()


class pingsweep():
    def __init__(self):
        self.net = a.net
        if not self.net.endswith('.'):
            self.net += "."
        self.start = a.start
        self.end = a.end
        self.uphosts=[]
        self.range=[]
        sys.stdout.write("[#] Trying: ")
        sys.stdout.flush()
        # copy_reg.pickle(types.MethodType, self.flail)
        for x in range (self.start, self.end, 1):
            self.range.append(str(x))
        self.repeater(self.range)
        print("")
        print("\n[#] Uphosts: " + str(len(self.uphosts[:])))
        with open("./" + self.net + "ips", 'w') as f:
            f.close()
        with open("./" + self.net +"ips", 'a') as f:
            for x in self.uphosts[:]:
                print(x)
                f.write(x +"\n")
        print("[#] Output written to ./" + self.net +"ips")


    def flail(self, a):
        sys.stdout.write(str(a) + ", ")
        sys.stdout.flush()
        temp = str(subprocess.Popen('ping -c1 -W1 ' + self.net + str(a), shell=True, stdout=subprocess.PIPE).stdout.read())
        if temp.find(" 0% packet loss") != -1:
            self.uphosts.append(self.net + a)

    def repeater(self, a):
        with futures.ThreadPoolExecutor(max_workers=50) as executor:
            for i in a[:]:
                executor.submit(self.flail, i)


if __name__ == "__main__":
    pingsweep()
