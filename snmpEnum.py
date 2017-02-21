#!/usr/bin/env python2.7
import argparse as ap, subprocess
from concurrent import futures


p = ap.ArgumentParser(description="Enum SNMP Processes, Programs, Process Paths, Storage Paths, Software Names, Users, Ports, hostnames, system descriptions.  Finds working community strings then performs individual OID queries via SNMPWALK.")
p.add_argument("-c", "--cmty", help="Single community string", type=str)
p.add_argument("-C", "--CMTY", type=str, help="File containing community strings")
p.add_argument("-i", "--ip", type=str, help="Single IP address")
p.add_argument("-I", "--IP", type=str, help="File containing IP addresses")
p.add_argument("-p", "--port", type=int, help="Port", default=161)
p.add_argument("-v", "--version", help="SNMP version 1|2c", type=str, default="1")
p.add_argument("-a", "--async", help="Number of IPs to BF against asyncronously.", type=int, default=1)
p.add_argument("-t", "--timeout", help="Timeout on single query after N seconds", type=int, default=10)
a = p.parse_args()

class snmp():
    def __init__(self):
        self.OIDS = [
            ["1.3.6.1.2.1.1.1", "System Description", "SYSDESCR_L"],
            ["1.3.6.1.2.1.1.2", "System ObjID", "SYSID_L"],
            ["1.3.6.1.2.1.1.5", "System Name", "SYSNAME_L"],
            ['1.3.6.1.4.1.77.1.4.1.0', "Workgroup", "WORKGROUP"],
            ["1.3.6.1.4.1.77.1.2.25", "User Accounts", "USER"],
            ["1.3.6.1.4.1.77.1.2.3.1.1", "Services", "SERVICE"],
            ["1.3.6.1.2.1.25.6.3.1.2", "Software Name", "SOFTNAME"]
        ]
        self.PROC = [
            ["1.3.6.1.2.1.25.4.2.1.1", "PIDs", "PROCS"],
            ["1.3.6.1.2.1.25.4.2.1.2", "PROCs", "PROCS"],
            ["1.3.6.1.2.1.25.4.2.1.4", "Processes Path", "PROCS"]
        ]
        self.NET = [
            ["1.3.6.1.2.1.4.20.1.1", "IP", "NETINT"],
            ["1.3.6.1.2.1.4.20.1.3", "Netmask", "NETINT"],
            ["1.3.6.1.2.1.2.2.1.2", "Interface", "NETINT"]
        ]
        self.ROUTE = [
            ["1.3.6.1.2.1.4.21.1.1", "Destination", "ROUTE"],
            ["1.3.6.1.2.1.4.21.1.11", "Mask", "ROUTE"],
            ["1.3.6.1.2.1.4.21.1.7", "Next Hop", "ROUTE"],
            ["1.3.6.1.2.1.4.21.1.3", "Metric", "ROUTE"]
        ]
        self.SHARE = [
            ["1.3.6.1.4.1.77.1.2.27.1.1", "Share name", "SHARE"],
            ["1.3.6.1.4.1.77.1.2.27.1.2", "Share path", "SHARE"],
            ["1.3.6.1.4.1.77.1.2.27.1.3", "Share comment", "SHARE"]
        ]
        self.TCP = [
            ["1.3.6.1.2.1.6.13.1.2", "LocalAddr", "TCPCONN"],
            ["1.3.6.1.2.1.6.13.1.3", "LocalPort", "TCPCONN"],
            ["1.3.6.1.2.1.6.13.1.4", "RAddr", "TCPCONN"],
            ["1.3.6.1.2.1.6.13.1.5", "RPort", "TCPCONN"],
            ["1.3.6.1.2.1.6.13.1.1", "STATE", "TCPCONN"]
        ]
        self.UDP = [
            ["1.3.6.1.2.1.7.5.1.1", "LocalAddrUDP", "UDPCONN"],
            ["1.3.6.1.2.1.7.5.1.2", "LocalPortUDP", "UDPCONN"],
        ]
        self.CMTY = []; self.IPS = []; self.port = a.port; self.ver = a.version
        self.__DATA = []; self._CMTY(); self._IPS(); self.MASTERLIST_IPS = []
        self.__PROC = []; self.__NET = []; self.__SHARE = []; self.__ROUTE = []
        self.__TCP = []; self.__UDP = []

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

    def arb(self, OBJ, cmtystr, ip):
        tmpObj=[]
        oid, phrase, tid = map(str, OBJ)
        out, err = subprocess.Popen("timeout " + str(a.timeout) + " snmpwalk -Ova -c " + cmtystr + " -v " + self.ver + " " + ip + ":" + str(self.port) + " " + oid, shell=True, stdout=subprocess.PIPE).communicate()
        out = out.splitlines()
        if len(out) >= 1:
            if ip not in self.MASTERLIST_IPS:
                self.MASTERLIST_IPS.append(ip)
            for line in out:
                if not line.find("End of MIB") != -1:
                    tmpObj.append(line.split(":")[-1].strip(' "'))
        else:
            tmpObj.append("NONE")
        return tmpObj

    def worker(self, bravo):
        delim=":"; WORKING_CMTYS = []
        for cmty in self.CMTY[:]:
            out, err = subprocess.Popen("timeout " + str(a.timeout) + " snmpwalk -Ov -c " + cmty + " -v " + self.ver + " " + bravo + ":" + str(self.port) + " 1.3.6.1.2.1.1.3", shell=True, stdout=subprocess.PIPE).communicate()
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
                # Processes
                self.__PROC.append(self.arb(self.PROC[0], cmty, bravo))
                self.__PROC.append(self.arb(self.PROC[1], cmty, bravo))
                self.__PROC.append(self.arb(self.PROC[2], cmty, bravo))
                for i,j,k in zip(self.__PROC[0][:], self.__PROC[1][:], self.__PROC[2][:]):
                    self.__DATA.append(bravo + delim + cmty + delim + self.PROC[0][2] + delim + 
                    i.split(":")[-1].strip(' "') + ":" + 
                    j.split(":")[-1].strip(' "') + ":" +
                    k.split(":")[-1].strip(' "'))
                # Network interfaces
                self.__NET.append(self.arb(self.NET[0], cmty, bravo))
                self.__NET.append(self.arb(self.NET[1], cmty, bravo))
                self.__NET.append(self.arb(self.NET[2], cmty, bravo))
                for i,j,k in zip(self.__NET[0][:], self.__NET[1][:], self.__NET[2][:]):
                    self.__DATA.append(bravo + delim + cmty + delim + self.NET[0][2] + delim + " " +
                        i.split(":")[-1].strip(' "') + " : " +
                        j.split(":")[-1].strip(' "') + " : " +
                        k.split(":")[-1].strip(' "'))
                # Shares
                self.__SHARE.append(self.arb(self.SHARE[0], cmty, bravo))
                self.__SHARE.append(self.arb(self.SHARE[1], cmty, bravo))
                self.__SHARE.append(self.arb(self.SHARE[2], cmty, bravo))
                for i, j, k in zip(self.__SHARE[0][:], self.__SHARE[1][:], self.__SHARE[2][:]):
                    self.__DATA.append(bravo + delim + cmty + delim + self.SHARE[0][2] + delim +
                                       i.split(":")[-1].strip(' "') + ":" +
                                       j.split(":")[-1].strip(' "') + ":" +
                                       k.split(":")[-1].strip(' "'))
                # Routes
                self.__ROUTE.append(self.arb(self.ROUTE[0], cmty, bravo))
                self.__ROUTE.append(self.arb(self.ROUTE[1], cmty, bravo))
                self.__ROUTE.append(self.arb(self.ROUTE[2], cmty, bravo))
                self.__ROUTE.append(self.arb(self.ROUTE[3], cmty, bravo))
                for i, j, k, l in zip(self.__ROUTE[0][:], self.__ROUTE[1][:], self.__ROUTE[2][:], self.__ROUTE[3][:]):
                    self.__DATA.append(bravo + delim + cmty + delim + self.ROUTE[0][2] + delim + " " +
                                       i.split(":")[-1].strip(' "') + "/" +
                                       j.split(":")[-1].strip(' "') + " : " +
                                       k.split(":")[-1].strip(' "')+ " : " +
                                       l.split(":")[-1].strip(' "'))
                # TCP connections
                self.__TCP.append(self.arb(self.TCP[0], cmty, bravo))
                self.__TCP.append(self.arb(self.TCP[1], cmty, bravo))
                self.__TCP.append(self.arb(self.TCP[2], cmty, bravo))
                self.__TCP.append(self.arb(self.TCP[3], cmty, bravo))
                self.__TCP.append(self.arb(self.TCP[4], cmty, bravo))
                for i, j, k, l, m in zip(self.__TCP[0][:], self.__TCP[1][:], self.__TCP[2][:], self.__TCP[3][:], self.__TCP[4][:]):
                    self.__DATA.append(bravo + delim + cmty + delim + self.TCP[0][2] + delim + " " +
                                       i.split(":")[-1].strip(' "') + "/" +
                                       j.split(":")[-1].strip(' "') + " : " +
                                       k.split(":")[-1].strip(' "') + "/" +
                                       l.split(":")[-1].strip(' "')+ " : " +
                                       m.split(":")[-1].strip(' "'))
                # UDP Connections
                self.__UDP.append(self.arb(self.UDP[0], cmty, bravo))
                self.__UDP.append(self.arb(self.UDP[1], cmty, bravo))
                for i, j in zip(self.__UDP[0][:], self.__UDP[1][:]):
                    self.__DATA.append(bravo + delim + cmty + delim + self.UDP[0][2] + delim + " " +
                                       i.split(":")[-1].strip(' "') + "/" +
                                       j.split(":")[-1].strip(' "'))


    def repeater(self, bb):
        print("[#] Narrowing down to working community strings and responsive hosts.\n[#] Please be patient.")
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
        self.counter()
        print("[#] Raw output written to ./SNMPEnum.raw in format <ip>:<cmty>:<branch>:<val>")

    def counter(self):
        print("\n[#] Stats for n3rds")
        for IP in self.MASTERLIST_IPS:
            ipcount=0; IPCOUNT=0
            for cmty in self.CMTY:
                cmtycount=0; a=0; b=0; c=0; d=0; e=0; f=0; g=0; h=0; i=0
                for line in self.__DATA:
                    if line.find(IP + ":") != -1 and line.find(":" + cmty + ":") != -1 and ipcount == 0 and cmtycount == 0:
                        cmtycount+=1; ipcount+=1
                        print("" + IP + ":" + cmty)
                    if line.find(IP + ":") != -1 and line.find(":" + cmty + ":") != -1:
                        IPCOUNT+=1
                        if line.find(self.OIDS[4][2]) != -1:
                            a+=1
                        if line.find(self.SHARE[0][2]) != -1:
                            b+=1
                        if line.find(self.PROC[0][2]) != -1:
                            c+=1
                        if line.find(self.OIDS[5][2]) != -1:
                            d+=1
                        if line.find(self.OIDS[6][2]) != -1:
                            e += 1
                        if line.find(self.NET[0][2]) != -1:
                            f += 1
                        if line.find(self.ROUTE[0][2]) != -1:
                            g += 1
                        if line.find(self.TCP[0][2]) != -1:
                            h += 1
                        if line.find(self.UDP[0][2]) != -1:
                            i += 1
                        if line.find(self.OIDS[0][2]) != -1:
                            print(self.OIDS[0][1] + ": " + line.split(":")[-1])
                        if line.find(self.OIDS[1][2]) != -1:
                            print(self.OIDS[1][1] + ": " + line.split(":")[-1])
                        if line.find(self.OIDS[2][2]) != -1:
                            print(self.OIDS[2][1] + ": " + line.split(":")[-1])
                        if line.find(self.OIDS[3][2]) != -1:
                            print(self.OIDS[3][1] + ": " + line.split(":")[-1])
                if IPCOUNT != 0:
                    print("Total Lines: " + str(IPCOUNT))
                    print(("%-5s %-6s %-5s %-8s %-9s %-7s %-6s %-8s %-8s") % (self.OIDS[4][2], self.SHARE[0][2], self.PROC[0][2], self.OIDS[5][2], self.OIDS[6][2], self.NET[0][2], self.ROUTE[0][2], self.TCP[0][2], self.UDP[0][2]))
                    print(("%-5s %-6s %-5s %-8s %-9s %-7s %-6s %-8s %-8s\n") % (str(a), str(b), str(c), str(d), str(e), str(f), str(g), str(h), str(i)))

if __name__ == "__main__":
    Alpha = snmp()
    Alpha.repeater(Alpha.IPS)
    Alpha.printer()
