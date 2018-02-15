#!/usr/bin/env python2

import sys, netaddr, argparse, csv
import datetime as dt



class CIDR():
    def __init__(s):
        s.CIDR = {1: 2147483648, 2: 1073741824, 3: 536870912, 4: 268435456, 5: 134217728, 6: 67108864,
            7: 33554432, 8: 16777216, 9: 8388608, 10: 4194304, 11: 2097152, 12: 1048576, 13: 524288,
            14: 262144, 15: 131072, 16: 65536, 17: 32768, 18: 16384, 19: 8192, 20: 4096, 21: 2048,
            22: 1024, 23: 512, 24: 256, 25: 128, 26: 64, 27: 32, 28: 16, 29: 8, 30: 4, 31: 2, 32: 1}
        s.prompt = "\n:> "
        s.USIN_ip = s.USIN_desc = s._USIN_netname = s.lowestIP = s.highestIP = s.ClientID = s.SODUser = s.Priority = s.Collector = s.timestamp = ""
        s.ScanSched = s.HostDiscovery = s.ServiceDiscovery = 0
        s.internal = 1
        s.IPs = s.networks = s.all_ips = []
        s.nos = ['n', 'no']
        s.yesses = ['y', 'yes']
        s.responses = { 'n':0, 'y':1 }


    def get_CIDR(s, input=""):
        if not input == "":
            s.USIN_ip = input
        else:
            a = ""
            while a not in s.yesses:
                a = ""
                s.USIN_ip = raw_input("Give CIDR format IP." + s.prompt)
                while a not in s.nos and a not in s.yesses:
                    print(s.USIN_ip)
                    a = raw_input("Is this correct?" + s.prompt)


    def get_DESC(s, input=""):
        if not input == "":
            s.USIN_desc = input
        else:
            a = ""
            while a not in s.yesses:
                a = ""
                s.USIN_desc = raw_input("Give intel description for all nets in that CIDR range." + s.prompt)
                while a not in s.nos and a not in s.yesses:
                    print(s.USIN_desc)
                    a = raw_input("Is this correct?" + s.prompt)

    def get_NETNAME(s, input=""):
        if not input == "":
            s.USIN_netname = input
        else:
            a = ""
            while a not in s.yesses:
                a = ""
                s.USIN_netname = raw_input("Give network name.  This should be brief." + s.prompt)
                while a not in s.nos and a not in s.yesses:
                    print(s.USIN_netname)
                    a = raw_input("Is this correct?" + s.prompt)


    def get_Priority(s, input=""):
        if not input == "":
            s.Priority = input
        else:
            a = ""
            while a not in s.yesses:
                a = ""
                s.Priority = raw_input("Give segment priority [1-5]." + s.prompt)
                while a not in s.nos and a not in s.yesses:
                    print(s.Priority)
                    a = raw_input("Is this correct?" + s.prompt)


    def get_ClientID(s, input=""):
        if not input == "":
            s.ClientID = input
        else:
            a = ""
            while a not in s.yesses:
                a = ""
                s.ClientID = raw_input("Give ClientID." + s.prompt)
                while a not in s.nos and a not in s.yesses:
                    print(s.ClientID)
                    a = raw_input("Is this correct?" + s.prompt)

    def get_date(s, input=""):
        if not input == "":
            s.timestamp = input
        else:
            s.timestamp = str(dt.datetime.now())

    def get_SODUSER(s, input=""):
        s.SODUSER = input

    def get_ScanSched(s, input="n"):
        s.ScanSched = input

    def get_ServiceDiscovery(s, input="n"):
        s.ServiceDiscovery = input

    def get_HostDiscovery(s, input="n"):
        s.HostDiscovery = input

    def get_Collector(s, input=""):
        s.Collector = input

    def normalize_range(s):
        temp_array = []
        s.networks = []
        for ip in netaddr.IPNetwork(s.USIN_ip):
            temp_array.append(str(ip))
            temp = str(ip)
            temp +="/24"
            s.networks.append(str(netaddr.IPNetwork(temp).network))
        s.networks = sorted(set(s.networks))
        s.all_ips = temp_array
        # print(temp_array)
        print(s.networks)
        s.lowestIP = temp_array[0]
        s.highestIP = temp_array[-1]
        print s.lowestIP, s.highestIP


    def generate_output(s):
        delim = ','
        qu = "'"
        f = open('SEGMENTS_out.csv', 'ab+')
        for network in s.networks:
            f.write(
                qu+ str(network) +qu +delim+
                qu+ s.ClientID +qu +delim+
                qu+ s.USIN_netname +qu +delim+
                str(s.Priority) +delim+
                qu+ s.USIN_desc +qu +delim+
                qu+ s.timestamp +qu +delim+
                qu+ s.SODUSER +qu +delim+
                qu+ s.timestamp +qu +delim+
                str(s.responses[s.ScanSched]) +delim+
                str(s.internal) +delim+
                str(s.responses[s.HostDiscovery]) +delim+
                str(s.responses[s.ServiceDiscovery]) +delim+
                qu+ s.Collector +qu
            +"\r\n")
        f.close()

def ExpandRange(cidr):
    temp_array = []
    networks = []
    for ip in netaddr.IPNetwork(cidr):
        temp_array.append(str(ip))
        temp = str(ip)
        temp +="/24"
        networks.append(str(netaddr.IPNetwork(temp).network))
    networks = sorted(set(networks))
    all_ips = temp_array
    # print(temp_array)
    print(networks)
    lowestIP = temp_array[0]
    highestIP = temp_array[-1]
    print lowestIP, highestIP





if __name__=="__main__":
#    PARAM_LEN = len(sys.argv)
    parser = argparse.ArgumentParser(description='Expand any CIDR ranges and output in CSV format suitable for import into Segments page.\n Single range (req: -c, -n, -d, -i, -u), or via CSV with "ip/cidr, netname, netdescr" format (req: -f, -i, -u).\n\nNote that output can be found in SEGMENTS_out.csv\n\n')
    parser.add_argument("-f", "--file", help="Use CSV file (IP, netname, desc) instead of single call (-c, -n, -d) for IP/cidr and desc.", type=str, default="")
    parser.add_argument("-c", "--cidr", help="CIDR format IP range", type=str, default="")
    parser.add_argument("-n", "--name", help="Network name", type=str, default="")
    parser.add_argument("-d", "--desc", help="Intel for this range", type=str, default="")
    parser.add_argument("-i", "--clientID", help="Client ID", type=str, default="")
    parser.add_argument("-u", "--user", help="SOD username", type=str, default="")
    parser.add_argument("-p", "--priority", help="[optional] Segment Priority (default=3 on 1-5, 5=critical)", type=int, default=3)
    parser.add_argument("-C", "--collector", help="[optional] Collector the segment is most likely to be seen from; leave blank if in doubt", type=str, default="")
    parser.add_argument("-s", "--scan", help="[optional] Add to Scheduled Scan? (default=n)", type=str, default="n")
    parser.add_argument("-H", "--hostd", help="[optional] Add segment to Host Discovery? (default=n)", type=str, default="n")
    parser.add_argument("-S", "--svc", help="[optional] Add segment to Service Discovery? (default=n)", type=str, default="n")
    parser.add_argument("-t", "--treat", help="[optional] Treat IP(s) as /24 by default.", action="store_true")
    parser.add_argument("-g", "--get", help="GET - print IP range based on CIDR and EXIT", type=str, default=None)
    P = parser.parse_args()
    if P.get != None:
        ExpandRange(P.get)
        sys.exit()

    a = CIDR()
    a.get_ClientID(P.clientID)
    a.get_SODUSER(P.user)
    a.get_date()
    a.get_Priority(P.priority)
    a.get_Collector(P.collector)
    a.get_ScanSched(P.scan)
    a.get_HostDiscovery(P.hostd)
    a.get_ServiceDiscovery(P.svc)
    if P.file != "":
        with open(P.file, 'rb') as f:
            reader = csv.reader(f, delimiter=",", quotechar="'")
            for row in reader:
                if P.treat == True:
                    IP = str('.'.join(row[0].strip("'").split(".")[0:3])) + ".0/24"
                else:
                    IP = row[0].strip("'")
                print(IP)
                a.get_CIDR(IP)
                a.get_NETNAME(str(row[1]))
                a.get_DESC(str(row[2]))
                a.normalize_range()
                a.generate_output()
    else:
        if P.treat == True:
            IP = str('.'.join(P.cidr.split(".")[0:3])) + ".0/24"
            print(IP)
        else:
            IP = P.cidr
        a.get_CIDR(IP)
        a.get_NETNAME(P.name)
        a.get_DESC(P.desc)
        a.normalize_range()
        a.generate_output()


