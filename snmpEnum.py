#!/usr/bin/env python2.7
import argparse as ap, subprocess
from concurrent import futures


p = ap.ArgumentParser(description="Enum SNMP Processes, Programs, Process Paths, Storage Paths, Software Names, Users, Ports")
p.add_argument("-c", "--cmty", help="Single community string", type=str)
p.add_argument("-C", "--CMTY", type=str, help="File containing community strings")
p.add_argument("-i", "--ip", type=str, help="Single IP address")
p.add_argument("-I", "--IP", type=str, help="File containing IP addresses")
p.add_argument("-p", "--port", type=int, help="Port", default=161)
p.add_argument("-v", "--version", help="SNMP version 1|2c", type=str, default="1")
p.add_argument("-a", "--async", help="Number of IPs to BF against asyncronously.", type=int, default=1)
p.add_argument("-t", "--timeout", help="Timeout on an IP after N seconds", type=int, default=5)
a = p.parse_args()

class snmp():
    def __init__(self):
        self.OIDS = [
            ["1.3.6.1.2.1.25.1.6.0", "System Processes", "SYSPROC"],
            ["1.3.6.1.2.1.25.4.2.1.2", "Running Programs", "RUNPROGS"],
            ["1.3.6.1.2.1.25.4.2.1.4", "Processes Path", "PROCPATH"],
            ["1.3.6.1.2.1.25.2.3.1.4", "Storage Units", "STOR"],
            ["1.3.6.1.2.1.25.6.3.1.2", "Software Name", "SOFTNAME"],
            ["1.3.6.1.4.1.77.1.2.25", "User Accounts", "USER"],
            ["1.3.6.1.2.1.6.13.1.3", "TCP Ports", "TCPPORT"],
            ["1.3.6.1.2.1.1.1", "System Description", "SYSDESCR_L"],
            ["1.3.6.1.2.1.1.2", "System ObjID", "SYSID_L"],
            ["1.3.6.1.2.1.1.5", "System Name", "SYSNAME_L"]
        ]
        self.CMTY = []; self.IPS = []; self.port = a.port; self.ver = a.version
        self.__DATA = []; self._CMTY(); self._IPS(); self.MASTERLIST_IPS = []

    def _CMTY(self):
        if a.CMTY is not None:
            with open(a.CMTY, "r") as f:
                self.CMTY = list(set(f.readlines()))
            f.close()
        if a.cmty is not None:
            self.CMTY.append(a.cmty)
        self.CMTY = [s.replace('\n', '') for s in self.CMTY]


    def _IPS(self):
        if a.IP is not None:
            with open(a.IP, "r") as f:
                self.IPS = list(set(f.readlines()))
            f.close()
        if a.ip is not None:
            self.IPS.append(a.ip)
        self.IPS = [s.replace('\n', '') for s in self.IPS]

    def worker(self, bravo):
        delim=":"; WORKING_CMTYS = []
        for cmty in self.CMTY[:]:
            out, err = subprocess.Popen("timeout " + str(a.timeout) + "snmpwalk -Ov -c " + cmty + " -v " + self.ver + " " + bravo + ":" + str(self.port) + " 1.3.6.1.2.1.1.3", shell=True, stdout=subprocess.PIPE).communicate()
            out = out.splitlines()
            if len(out) >= 1:
                WORKING_CMTYS.append(cmty)
        if len(WORKING_CMTYS) != 0:
            for cmty in WORKING_CMTYS[:]:
                for oid, phrase, tid in self.OIDS[:]:
                    out, err = subprocess.Popen("timeout " + str(a.timeout) + " snmpwalk -Ov -c " + cmty + " -v " + self.ver + " " + bravo + ":" + str(self.port) + " " + oid, shell=True, stdout=subprocess.PIPE).communicate()
                    out = out.splitlines()
                    if len(out) >= 1:
                        if bravo not in self.MASTERLIST_IPS:
                            self.MASTERLIST_IPS.append(bravo)
                        for line in out:
                            if not line.find("End of MIB") != -1:
                                self.__DATA.append(bravo + delim + cmty + delim + tid + delim + line.split(":")[-1].strip(' "'))

    def repeater(self, bb):
        print("[#] Narrowing down to working community strings and responsive hosts.\n[#] Please be patient, and Timeout warnings are normal for this step.")
        with futures.ThreadPoolExecutor(max_workers=a.async) as executor:
            for i in bb[:]:
                executor.submit(self.worker, i.strip("\n"))

    def printer(self):
        self.MASTERLIST_IPS.sort()
        self.__DATA.sort()
        tmp = list(set(self.__DATA))
        tmp.sort()
        self.__DATA = tmp
        with open("./SNMPEnum.raw", "wb") as f:
            for item in self.__DATA:
                print(item.strip('\r'))
                f.write(item.strip("\n") + "\n")
        f.close()
        print("\n[#] Stats for n3rds")
        self.counter()
        print("[#] Raw output written to ./SNMPEnum.raw in format <ip>:<cmty>:<branch>:<val>")

    def counter(self):
        for IP in self.MASTERLIST_IPS:
            ipcount=0; IPCOUNT=0
            for cmty in self.CMTY:
                cmtycount=0; a=0; b=0; c=0; d=0
                for line in self.__DATA:
                    if line.find(IP + ":") != -1 and line.find(":" + cmty + ":") != -1 and ipcount == 0 and cmtycount == 0:
                        cmtycount+=1; ipcount+=1
                        print("" + IP + ":" + cmty)
                    if line.find(IP + ":") != -1 and line.find(":" + cmty + ":") != -1:
                        IPCOUNT+=1
                        if line.find(self.OIDS[1][2]) != -1:
                            a+=1
                        if line.find(self.OIDS[4][2]) != -1:
                            b+=1
                        if line.find(self.OIDS[5][2]) != -1:
                            c+=1
                        if line.find(self.OIDS[6][2]) != -1:
                            d+=1
                        if line.find(self.OIDS[7][2]) != -1:
                            print(self.OIDS[7][1] + ": " + line.split(":")[-1])
                        if line.find(self.OIDS[8][2]) != -1:
                            print(self.OIDS[8][1] + ": " + line.split(":")[-1])
                        if line.find(self.OIDS[9][2]) != -1:
                            print(self.OIDS[9][1] + ": " + line.split(":")[-1])
                if IPCOUNT != 0:
                    print("Total Lines: " + str(IPCOUNT))
                    print(("%-9s %-9s %-5s %-8s") % (self.OIDS[1][2], self.OIDS[4][2], self.OIDS[5][2], self.OIDS[6][2]))
                    print(("%-9s %-9s %-5s %-8s\n") % (str(a), str(b), str(c), str(d)))

if __name__ == "__main__":
    Alpha = snmp()
    Alpha.repeater(Alpha.IPS)
    Alpha.printer()
