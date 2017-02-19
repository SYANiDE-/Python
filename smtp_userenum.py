#!/usr/bin/env python2.7
import socket, argparse as ap
from concurrent import futures


p = ap.ArgumentParser(description="Enum SMTP users using VRFY method (default) or -e EXPN.")
p.add_argument("-u", "--user", help="Single user name", type=str)
p.add_argument("-U", "--USER", type=str, help="File containing user names")
p.add_argument("-i", "--ip", type=str, help="Single IP address")
p.add_argument("-I", "--IP", type=str, help="File containing IP addresses")
p.add_argument("-p", "--port", type=int, help="Port", default=25)
p.add_argument("-e", "--expn", action="store_true", help="Use EXPN mode instead.  Default is VRFY")
p.add_argument("-c", "--concurrent", help="Number of IPs to BF against concurrently.", type=int, default=1)
p.add_argument("-t", "--timeout", help="Timeout on an IP after N seconds", type=int, default=30)
a = p.parse_args()


class smtp():
    def __init__(self):
        self.IPS = []
        self.PORT = a.port
        self.USERS = []
        self.EXIST = []
        self.BANNERS = []
        self.pBANNERS = []
        self.METHOD = "EXPN" if a.expn == True else "VRFY"
        self._IPS()
        self._USERS()

    def _IPS(self):
        if a.IP is not None:
            with open(a.IP, "r") as f:
                self.IPS = list(set(f.readlines()))
            f.close()
        if a.ip is not None:
            self.IPS.append(a.ip)

    def _USERS(self):
        if a.USER is not None:
            with open(a.USER, "r") as f:
                self.USERS = list(set(f.readlines()))
            f.close()
        if a.user is not None:
            self.USERS.append(a.user)

    def BF(self, bb):
        def connrecon():
            d=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            d.settimeout(a.timeout)
            d.connect((bb, int(self.PORT)))
            resp = d.recv(1024)
            domain = resp.split(" ")[1]
            self.BANNERS.append(bb + ":" + resp)
            print(bb + " " + resp)
            d.send("HELO spanker.com\r\n")
            resp = d.recv(1024)
            self.BANNERS.append(bb + ":" + resp)
            print(bb + " " + resp)
            return d,domain
        s,domain = connrecon()
        for user in self.USERS:
            print(bb + " " + user.strip("\n"))
            s.send(self.METHOD + " " + user.strip("\n") + "\r\n")
            resp = s.recv(1024)
            if resp.startswith("421"):
                s,domain = connrecon()
                s.send(self.METHOD + " " + user.strip("\n") + "\r\n")
                resp = s.recv(1024)
            if resp.startswith("502"):
                s.close()
                return "EXIT"
            print(bb + " " + resp.strip("\n"))
            if resp.startswith("250") or resp.startswith("251"):
                print(resp.strip("\n"))
                self.EXIST.append(bb + ":" + domain + ":" + resp.split("<")[1].split(">")[0].strip("\n"))
            if resp.startswith("252") and not resp.find("take message") != -1 and not resp.find("Cannot VRFY") != -1:
                self.EXIST.append(bb + ":" + domain + ":" + resp.split(" ")[-1].strip("\n"))

    def repeater(self, bb):
        with futures.ThreadPoolExecutor(max_workers=a.concurrent) as executor:
            for i in bb[:]:
                executor.submit(self.BF, i.strip("\n"))

    def printer(self):
        tmplist = []
        with open("./SMTPUsers." + self.METHOD + ".txt", "w") as f:
            pass
        f.close()
        masterlist = list(set(self.EXIST))
        masterlist.sort()
        self.EXIST = masterlist
        print("\n\n[#] Found total " + str(len(self.EXIST)) + " valid users:")
        if len(masterlist) > 0:
            with open("./SMTPUsers." + self.METHOD + ".txt", "a") as f:
                for item in self.EXIST[:]:
                    print(item)
                    f.write(item)
            f.close()
            print("[#] Banners:")
            for item in self.BANNERS[:]:
                for meti in self.EXIST[:]:
                    if meti.find(item.split(":")[0]) != -1:
                        tmplist.append(item.strip("\n"))
            self.pBANNERS = list(set(tmplist))
            self.pBANNERS.sort()
            for item in self.pBANNERS:
                print(item)
            print("[#] Output written to ./SMTPUsers." + self.METHOD + ".txt in format <IP>:<domain>:<user@domain>")


if __name__ == "__main__":
    Alpha = smtp()
    Alpha.repeater(Alpha.IPS)
    Alpha.printer()

