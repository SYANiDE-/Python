#!/usr/bin/env python2.7
import argparse as ap, subprocess, sys, time
from concurrent import futures


p = ap.ArgumentParser(description="Enum SMB")
p.add_argument("-i", "--ip", type=str, help="Single IP address")
p.add_argument("-I", "--IP", type=str, help="File containing IP addresses")
p.add_argument("-T", "--tcp", help="DISABLE tcp scanning", action="store_true")
p.add_argument("-U", "--udp", help="DISABLE udp scanning", action="store_true")
a = p.parse_args()

class smb():
    def __init__(self):
        self.IPS = []
        self.SMBUpHosts = []
        self.SMBv1Hosts = []
        self.SMBv2Hosts = []
        self.SMBEnum = []
        self.simpleListIP = ""
        self.SMBUsers = []
        self.PORTS = [
                "nmap -sT -sU -Pn -vv --open -p U:137,U:138,T:137,T:139,T:445 -n ",
                "nmap -sT -Pn -vv --open -p T:137,T:139,T:445 -n "
                "nmap -sU -Pn -vv --open -p U:137,U:138 -n "
            ]
        self.MODE = [
            [" -iL ", " -oG ", "SMBUphosts.raw", "SMBUphosts.ips"],
            [" -iL ", " --script smbv2-enabled -oN ", "SMBv1Hosts.raw", "SMBv1Hosts.ips"],
            [" -iL ", " --script smb-enum-* -oN ", "SMBEnum.raw", "!SMBEnum.lineout"]
        ]
        self.p_MODE = self.portMode()
        self.preamble = self.PORTS[self.p_MODE]
        self._IPS()

    def _IPS(self):
        if a.IP is not None:
            with open(a.IP, "r") as f: self.IPS = list(set(f.readlines()))
            f.close()
        if a.ip is not None: self.IPS.append(a.ip)
        self.IPS = [s.replace('\n', '') for s in self.IPS]

    def portMode(self):
        if a.udp == True: return 1
        elif a.tcp == True: return 2
        else: return 0

    def writer(self, somefile, someobj, name):
        with open(somefile, "wb") as f:
            for x in range(0, len(someobj), 1):
                f.write(someobj[x] + "\n")
            print(someobj, " #" + name)
            f.close()

    def worker(self, mode, ipobj, searchstr, OBJ, split1, split2, splitmode, label):
        tmp = []
        tmpIP =""
        tmpCategory = ""
        subprocess.Popen(self.preamble + self.MODE[mode][0] + ipobj + self.MODE[mode][1] + self.MODE[mode][2], shell=True, stdout=subprocess.PIPE).communicate()
        with open(self.MODE[mode][2], "r") as f:
            tmp = list(f.readlines())
            f.close()
        tmp = [s.replace("\n", '') for s in tmp]
        for x in range(0, len(tmp), 1):
            if splitmode == 1:
                if tmp[x].find(searchstr) != -1:
                    OBJ.append(tmp[x].split(split1)[1])
            if splitmode == 2:
                if tmp[x].find(searchstr) != -1:
                    tmpIP = tmp[x].split(searchstr)[1].rstrip()
                if tmp[x].find(split1) != -1:
                    self.SMBv2Hosts.append(tmpIP)
            if splitmode == 3:
                if tmp[x].find(searchstr) != -1:
                    tmpIP = tmp[x].split(searchstr)[1].rstrip()
                if tmp[x].find(split1) != -1:
                    if tmp[x].find(split2) != -1:
                        tmpCategory = tmp[x].split(split2)[1]
                    if not tmp[x].find("filtered") != -1:
                        OBJ.append(tmpIP + ":" + tmpCategory.rstrip() + str(x) + ":" + tmp[x])
        if splitmode == 2:
            OBJ = [x for x in self.SMBUpHosts if x not in self.SMBv2Hosts]
            self.writer("SMBv2Hosts.ips", self.SMBv2Hosts, "SMBv2Hosts")
        if splitmode == 3:
            predicate = ""
            user = ""
            for x in range(0, len(OBJ), 1):
                if OBJ[x].find(":users:") != -1 and not OBJ[x].find(" smb-enum-") != -1:
                    predicate = ':'.join(OBJ[x].split(":")[:1]) + ":"
                    if OBJ[x].find("   ") != -1 and not OBJ[x].find("     ") != -1:
                        user = OBJ[x].split("|   ")[1]
                        self.SMBUsers.append(predicate + user.split(" (RID")[0] + ":" + user.split(" (RID: ")[1].split(")")[0])
            self.writer("!SMBUsers.lineout", self.SMBUsers, "SMBUsers")
        self.writer(self.MODE[mode][3], OBJ, label)

if __name__ == "__main__":
    Alpha = smb()
    Alpha.worker(0, a.IP, "Status: Up", Alpha.SMBUpHosts, " ", " ", 1, "SMBUphosts")
    Alpha.worker(1, "SMBUphosts.ips", "scan report for ", Alpha.SMBv1Hosts, "supports ", " ", 2, "SMBv1Hosts")
    Alpha.worker(2, "SMBv1Hosts.ips", "scan report for ", Alpha.SMBEnum, "|", "smb-enum-", 3, "SMBEnum")
