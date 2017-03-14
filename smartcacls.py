#!/usr/bin/env python
import os, sys, subprocess, argparse, time

ap = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter,
    description=('''\
    Smarter CACLS search\n\tNot smartest, but...

    OI - Object inherit -
        This folder and files.  Sans subfolders.
    CI -
        Container inherit - This folder & subfolders.
    IO -
        Inherit only - the ACE doesn't apply to current file/directory

    (OI)(CI) This folder, subfolders, files
    (OI)(CI)(IO) Subfolders and files only
    (CI)(IO) Subfolders only
    (OI)(IO) Files only
    '''))
ap.add_argument("-l", "--list", help="List all files and folders that CACLS can be viewed by the current user",
                action="store_true")
ap.add_argument("-n", "--name", help="search each CACL that contains permissons for NAME.\n\tex: -n SYSTEM\n\twill be searched like:\n\tSYSTEM:",
                type=str, default="")
ap.add_argument("-p", "--permission", help="search for permission in CACL",
                type=str, default="")
ap.add_argument("-d", "--disableDelim", help="permission is NOT delimited, i.e., not a special permission\n\tBy default, permission search includes delimiter like\n\t:<userin>",
                action="store_true")
ap.add_argument("-c", "--combo", help="search for specific combo. \n\tex: SYSTEM:W",
                type=str, default="")
ap.add_argument("-r", "--raw", help="search for raw word/string.",
                type=str, default="")
ap.add_argument("-SL", "--singleline", help="Output full CACL as single line.",
                action='store_true')

agro = ap.parse_args()

allfiles=[]
cacls=[]


if agro.disableDelim == True:
    DELIM = ""
else:
    DELIM = ":"

if agro.combo != "":
    NAME = agro.combo.split(":")[0]
    PERM = agro.combo.split(":")[1]
    DELIM1= NAME + ":("
    DELIM2=")" + PERM

if agro.permission != "":
    PERM1 = ":" + agro.permission
    PERM2 = ")" + agro.permission



def safety():
    gimp = '&&&'.join(map(str, os.listdir('.')))
    pig = list(gimp.split("&&&"))
    for x in pig[:]:
        try:
            proc = subprocess.check_output(['cacls', x])
            cacls.append(proc)
        except:
            pig.remove(x)
    return pig

def stripper(a):
    swapmeet=""
    shimmie=""
    mutated = []
    tmp = []
    temper = []
    level_uno = []
    level_dose = []
    level_tres = []
    for item in a[:]:
        while "  " in item:
            item = item.replace("  ", " ")
        level_uno.append(item)
    for x in range(0, len(allfiles), 1):
        swapmeet = level_uno[x].replace(allfiles[x], (str(allfiles[x] + '\r\n')))
        if agro.singleline == True:
            shimmie = swapmeet.replace('\r\n', ' ')
        else:
            shimmie = swapmeet.replace('\r\n', '\r\n\t')
        mutated.append(shimmie)
        # print(mutated[x])
    return mutated




def printer(a, n):
    if n == 1:
        for x in a[:]:
            print x
        print ("\n")
    if n == 2:
        for x in a[:]:
            if agro.raw != "":
                if agro.raw in x:
                    print(x)
            else:
                temp = x.split(" ")
                for item in temp[:]:
                    if agro.combo != "":
                        if (item.find(agro.combo) != -1):
                            print(x)
                        else:
                            if ((item.find(DELIM1) != -1) and (item.find(DELIM2) != -1)) == True:
                                print(x)
                    elif agro.name != "" and agro.permission != "":
                        if (item.find(agro.name) != -1) and (item.find(PERM1) != -1):
                            print(x)
                        else:
                            if (item.find(agro.name) != -1) and (item.find(PERM2) != -1):
                                print(x)
                    else:
                        if (agro.name != "") and (agro.permission == ""):
                            if item.find(agro.name + DELIM) != -1:
                                print(x)
                        else:
                            if (agro.name == "") and (agro.permission != ""):
                                if item.find(PERM1) != -1 or item.find(PERM2) != -1:
                                    print(x)
            if agro.combo == "" and agro.name == "" and agro.permission == "" and agro.raw == "":
                print(x)
        print("Safety check had " + str(len(allfiles)) + " files to check")


if __name__ == "__main__":
    # allfiles = safety()
    # printer(allfiles)
    spanker = []
    allfiles = safety()
    spanker = stripper(cacls)
    if agro.list == True:
        printer(allfiles, 1)
    printer(spanker, 2)
