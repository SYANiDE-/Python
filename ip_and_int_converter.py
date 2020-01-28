#!/usr/bin/env python2


def ip_to_int(zzz):
    a,b,c,d = zzz.split(".")
    e,f,g,h = [(int(x) <<y) for x,y in zip([a,b,c,d],[24,16,8,0])]
    return int(e+f+g+h)

def int_to_ip(zzz):
    octets = [str(zzz >>x & 255) for x in [24,16,8,0]]
    return ".".join(octets)


def get_list():
	inp = []
	userin = ""
	ends = ['eof','end','quit','stop','exit','done']
	print("[!] Give IPs or integers, one per line. Or as CSV\n[!] End with: end, quit, stop, exit, done:")
	userin = raw_input()
	while not userin.lower() in ends:
		if userin.find(",") != -1:
			for item in userin.split(","):
				if item.find(".") != -1:
					inp.append(str(item).replace(" ",""))
				else:
					inp.append(int(item.replace(" ","")))
		else:
			if userin.find(".") != -1:
				inp.append(str(userin).replace(" ",""))
			else:
				inp.append(int(userin.replace(" ","")))
		userin = raw_input()
	inp = list(dict.fromkeys(inp))
	inp.sort()
	return inp

def listify(zzz):
	ips = []
	ints = []
	for item in zzz:
		if type(item) == int or type(item) == long:
			ints.append(item)
			ips.append(int_to_ip(item))
		if type(item) == str:
			ips.append(item)
			ints.append(ip_to_int(item))
	return (ips, ints)


def print_handler((xxx,yyy)):
	print("\n[.] IPs:\n %s" % xxx)
	print("\n[.] Ints:\n %s" % yyy)
	print("\n[.] IP, Int:")
	for item,meti in zip(xxx,yyy):
		print("%s, %s" % (item,meti))



if __name__=="__main__":
	print_handler(listify(get_list()))



		

		
		



