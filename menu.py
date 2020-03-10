import os, sys
""" This is a menu class definition for reuse """


class Menu():
    class stack():
        def __init__(ob):
            ob.__stack = []
        def push(ob,val):
            ob.__stack.append(val)
        def pop_byindex(index):
            """ Pop value off stack by index """
            return ob.__stack.pop(ob,index)
        def pop_byvalue(ob,val):
            """ Pop value off stack by value """
            temp = ob.__stack
            [temp.pop(index) for (index,value) in enumerate(ob.__stack) if value == val ]
            if val in ob.__stack:
                ob.__stack = temp
                return val
            else:
                return None
        def remove(ob,val):
            """ Remove all occurrence of val """
            temp = []
            for item in ob.__stack:
                if not item == val:
                    temp.append(item)
            ob.__stack = temp
        def insert(ob,index,val):
            """ Insert object before index """
            ob.__stack.insert(index,val)
        def get(ob):
            return ob.__stack
        def set(obj,input_list):
            ob.__stack = input_list
    
    
    def __init__(s):
        pass
    def quit(s):
        sys.exit()
    def cancel(s):
        return None
    def back(s):
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
            opts = []
            for item in app_adds:
                for k,v in item.items():
                    opts.append(k)
            print("[!] Selected option not among valid choices! Expected %s" % opts)
            return None

    def __validate_index(s,uin,valids):
        digit = int(uin)
        high = len(valids)
        if digit in range(0,high):
            return digit
        else:
            print("[!] Selected option not value between %s and %s" % (str(0),str(high)))
            print("[!] (truncated \"%s\" from selection)" % digit)
            return None

    def index_userin(s,question,valids,app_adds=[]):
        """ Prompt user with question and collect their selection as index to a list of choices
        """
        while True: 
            uin = ""
            s.__printer(question,valids,app_adds)
            uin = raw_input(":> " )
            if uin.isalpha():
                ## Then must be a menu option rather than indexed list item
                s.__trycall(uin,app_adds)
            if uin.isdigit():
                ## Then must be an indexed list item rather than a menu option
                result = s.__validate_index(uin,valids)
                if result is not None:
                    return result

    def index_userin_list(s, question, valids, app_adds=[]):
        """  Prompt user with question and collect their selection as csv list of indexes to a list of choices
        """
        while True:
            uin = []
            s.__printer(question + " (single or csv)",valids,app_adds)
            uin = raw_input(":> ").split(",")
            if any(x.isalpha() for x in uin):
                return [s.__trycall(x,app_adds) for x in uin if x.isalpha()]
            if any(x.isdigit() for x in uin):
                dest = []
                for x in uin:
                    if x.isdigit():
                        result = s.__validate_index(x,valids)
                        if result is not None:
                            dest.append(result)
                if len(dest) > 0:
                    return dest
