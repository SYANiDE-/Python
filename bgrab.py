"""A simple banner-grabbing program."""
"""Lots of cool things going on in here:
Uses:
    socket to make communication
    argparse to take in positional parameters, both positional and optional examples given.
    subprocess to run (Popen) programs, read into pipe, print the pipe back  (nmap)
    dynamic variable placement "something %s" % (somevar to place in string)
    blessings.Terminal()  for colorization, really cool!
    Really cool how timeout is set; if --timeout is passed as param, use that, else use socketTO
"""
import socket, argparse, string
from subprocess import Popen, PIPE
from blessings import Terminal


# Useful:  https://docs.python.org/2/library/socket.html
# Useful:  https://docs.python.org/2/howto/sockets.html
# Useful:  http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
# Useful:  https://docs.python.org/2/howto/argparse.html
# Useful:  https://pymotw.com/2/argparse/
# Useful:  http://blog.endpoint.com/2015/01/getting-realtime-output-using-python.html
# Useful:  https://docs.python.org/2/library/curses.html  #for reference; another way to colorize
# Useful:  http://stackoverflow.com/questions/18551558/how-to-use-terminal-color-palette-with-curses
# Useful:  http://gnosis.cx/publish/programming/charming_python_6.html  more curses fun-ness
# Useful:  https://pypi.python.org/pypi/blessings
# Useful:  https://pypi.python.org/pypi?%3Aaction=browse

term = Terminal()
succ = "{t.normal}{t.green}{}{t.normal}".format     #green
fail = "{t.bold}{t.red}{}{t.normal}".format         #red
warn = "{t.bold}{t.yellow}{}{t.normal}".format      #yellow
info = "{t.normal}{t.grey}{}{t.normal}".format      #grey
norm = "{t.normal}{}{t.normal}".format              #explicit normal (clear)

socketTO = 3
parser = argparse.ArgumentParser(prefix_chars='-')   # create the parser, and define prefix chars
# nargs=
"""
N 	The absolute number of arguments (e.g., 3).
? 	0 or 1 arguments
* 	0 or all arguments
+ 	All, and at least one, argument  [list]
"""
# What defines a positional parameter or a keyed parameter?  The use of prefix chars or not!
# The first two are positional (requires no explicit key declaration in parameter pass)
# The third one is an optional argument.
# you can also define a default='' in case the parameter isn't supplied.
parser.add_argument('ip', nargs='?', help="The IP to connect to", type=str)
parser.add_argument('port', nargs='?', help="The PORT to connect to", type=int)
parser.add_argument('--timeout', nargs='?', help="Set max timeout", type=int)
ins = parser.parse_args()


def main():
    IP = ins.ip
    PORT = ins.port
    socket.setdefaulttimeout(ins.timeout or socketTO)
    print(succ("[+] Socket default timeout set to "+ str(ins.timeout or socketTO) +" seconds.", t=term))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(succ("[+] Created a socket object.", t=term))
    print(succ("[+] Attempting to make connection to IP "+ IP +" and PORT "+ str(PORT) +".", t=term))
    try:
        s.connect((IP, PORT))
        comm = s.recv(1024)
        print("")
        if (len(comm) > 1):
            print(succ(term.bold + "[+] Connected!", t=term))
            print(term.bold + "Response:" + term.normal)
        else:
            print("Nothing...")
        print(norm(comm, t=term))
        print("")
    except socket.error:
        print("")
        print(fail("[x] Couldn't connect; connection refused on IP "+ IP +" and PORT "+ str(PORT) +".", t=term))
        print("")
        print(warn("[!] Maybe port isn't open...  Examine target with nmap?  (Y/N)", t=term))
        print(info("[?]: ", t=term)),
        try:
            input = raw_input()
            print("")
            if (string.upper(input)[0] == "Y"):
                print(warn("[!] Please wait... running nmap against target IP", t=term))
                proc = Popen(['sudo', 'nmap', '-sTU', '--top-ports=60000', "%s" % IP], stdout=PIPE)
                output = proc.communicate()[0]
                print('{}'.format(output))
                #condensed:  print('{}'.format(Popen(['sudo', 'nmap', '-sTU', '--top-ports=60000', "%s" % IP], stdout=PIPE).communicate()[0])
            print(warn("[!] Grab banner of different port? (Y/N)", t=term))
            print(info("[?]: ", t=term)),
            inp = raw_input()
            print("")
            if (string.upper(inp) == "Y"):
                print(warn("[!] Enter the port number.", t=term))
                print(info("[?]: ", t=term)),
                ins.port = int(raw_input().strip('\n'))
                print("")
                main()
            print(warn("[!] Exiting...", t=term))
            print("")
        except:
            raise
    except:
        print(fail("Some unhandled exception went wrong...", t=term))


if __name__ == "__main__":
    main()
