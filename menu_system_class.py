#!/usr/bin/env python2
import os, sys, re



class menu():
    def __init__(s):
        pass
    def quit(s):
        sys.exit()
    def cancel(s):
        return None
    def add_mapped_option(s,target_list,choice,title,mapped_function):
        """ Create a mapped menu choice.  Selecting this choice in a menu instead calls a mapped_function rather than
            the callee returning an index to the selection.  Append to target_list, a dict within a dict such that:
            
            target_list.append( { "option": {"This is the title": mapped_function}})
            i.e., target_list.append({'q':{"quit":sys.exit}})
            
            These options should be preferred to be non-numeric
        """
        if not choice.isalpha():
            raise ValueError("Expected non-numeric value for \"choice\"")
        target_list.append({choice: {title: mapped_function}})
    
    def __printer(s,question,valids,app_adds=[]):
        print("[?] %s" % question)
        for (index,item) in enumerate(valids):
            print("\t%s\t%s" % (index,item))
        for item in app_adds:
            for k,v in item.items():
                for a,b in v.items():
                    print("\t%s\t%s" % (k,a))
    
    def __trycall(s,uin,app_adds):
        opts = []
        for item in app_adds:
            for k,v in item.items():
                opts.append(k)
                for a,b in v.items():
                    if k == uin:
                        b()
                        return None
        if not uin in opts:
            print("[!] Selected option not among valid choices!")
            return None
        
    def index_userin(s,question,valids,app_adds=[]):
        uin = ""
        while True: 
            s.__printer(question,valids,app_adds)
            uin = raw_input(":> " )
            if uin.isalpha():
                ## Then must be a menu option rather than indexed list item
                s.__trycall(uin,app_adds)
            if uin.isdigit():
                ## Then must be an indexed list item rather than a menu option
                digit = int(uin)
                high = len(valids)
                if digit in range(0,high):
                    return digit
                else:
                    opts = []
                    for item in app_adds:
                        for k,v in item.items():
                            opts.append(k)
                    print("[!] Expected option in %s or value in range(%s,%s)" % (opts, str(0),str(high)))


def main():
    z = menu()
    z.var = []
    z.add_mapped_option(z.var,'c','cancel',z.cancel)
    z.add_mapped_option(z.var,'q','quit',z.quit)
    tests = ['alpha','beta','gamma','delta','echo']
    resp = z.index_userin("Is this sane?",tests,z.var)
    print(resp)

if __name__=="__main__":
    main()
