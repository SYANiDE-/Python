#!/usr/bin/python

#######
"It's slop, I admit, but it gets 'er done"
#######

import sys, argparse, time, struct


ap = argparse.ArgumentParser(description="Print hex range in a few different formats")
ap.add_argument("-b", "--bytecode", help="Print characters in bytecode format", action="store_true")
ap.add_argument("-f", "--full", help="Print at least the full spectrum minus badchars", action="store_true")
ap.add_argument("-r", "--remove_spaces", help="Remove spaces from output string", action="store_true")
ap.add_argument("-z", "--zero", help="Zeros instead of slashes", action="store_true")
ap.add_argument("-R", "--range", help="Range to N chars long from beginning.  Repeat range if more chars than 0xFF",
                type=int, default=1)
ap.add_argument("-n", "--nopsled", help="Generate NOPSLED of size N",
                type=int, default=0)
ap.add_argument("-q", "--quote", help="Quoted", action="store_true")
ap.add_argument("-bc", "--badchars",
                help="Remove bad characters from output string\nMUST be in hex, space separated list (no slash x)",
                type=str, default="ZZZZZ")
ap.add_argument("-c", "--compare",
                help="Enter comparison mode and compare existing string for chars not present\nMUST be in \\x format, single line.",
                action="store_true")
ap.add_argument("-S", "--search", help="Search for expression in character map",
                type=str, default="")
ap.add_argument("-C", "--charmap", help="Print charmap.\n\t-C [c|p|e|a]:\n\t\tc CONTROL charset\n\t\tp PRINTABLE charset\n\t\te EXTENDED charset\n\t\ta ALL c,p,e",
                type=str, default="")
a = ap.parse_args()

CTL_CHARS = [['Dec', 'Hex', 'Bin', 'Char', 'Desc'], ['00', '00', '00000000', 'NUL', 'null'], ['01', '01', '00000001', 'SOH', 'start of header'], ['02', '02', '00000010', 'STX', 'start of text'], ['03', '03', '00000011', 'ETX', 'end of text'], ['04', '04', '00000100', 'EOT', 'end of transmission'], ['05', '05', '00000101', 'ENQ', 'enquiry'], ['06', '06', '00000110', 'ACK', 'acknowledge'], ['07', '07', '00000111', 'BEL', 'bell'], ['08', '08', '00001000', 'BS', 'backspace'], ['09', '09', '00001001', 'HT', 'horizontal tab'], ['10', '0A', '00001010', 'LF', 'line feed'], ['11', '0B', '00001011', 'VT', 'vertical tab'], ['12', '0C', '00001100', 'FF', 'form feed'], ['13', '0D', '00001101', 'CR', 'enter / carriage return'], ['14', '0E', '00001110', 'SO', 'shift out'], ['15', '0F', '00001111', 'SI', 'shift in'], ['16', '10', '00010000', 'DLE', 'data link escape'], ['17', '11', '00010001', 'DC1', 'device control 1'], ['18', '12', '00010010', 'DC2', 'device control 2'], ['19', '13', '00010011', 'DC3', 'device control 3'], ['20', '14', '00010100', 'DC4', 'device control 4'], ['21', '15', '00010101', 'NAK', 'negative acknowledge'], ['22', '16', '00010110', 'SYN', 'synchronize'], ['23', '17', '00010111', 'ETB', 'end of trans. block'], ['24', '18', '00011000', 'CAN', 'cancel'], ['25', '19', '00011001', 'EM', 'end of medium'], ['26', '1A', '00011010', 'SUB', 'substitute'], ['27', '1B', '00011011', '\xc2\xa0ESC', 'escape'], ['28', '1C', '00011100', '\xc2\xa0FS', 'file separator'], ['29', '1D', '00011101', 'GS', 'group separator'], ['30', '1E', '00011110', 'RS', 'record separator'], ['31', '1F', '00011111', 'US', 'unit separator'], ['127', '7F', '01111111', 'DEL', 'delete']]
PRNT_CHARS = [['Dec', 'Hex', 'Bin', 'Char', 'Desc'], ['32', '20', '00100000', 'Space', 'space'], ['33', '21', '00100001', '!', 'exclamation mark'], ['34', '22', '00100010', '"', 'double quote'], ['35', '23', '00100011', '#', 'number'], ['36', '24', '00100100', '$', 'dollar'], ['37', '25', '00100101', '%', 'percent'], ['38', '26', '00100110', '&', 'ampersand'], ['39', '27', '00100111', "'", 'single quote'], ['40', '28', '00101000', '(', 'left parenthesis'], ['41', '29', '00101001', ')', 'right parenthesis'], ['42', '2A', '00101010', '*', 'asterisk'], ['43', '2B', '00101011', '+', 'plus'], ['44', '2C', '00101100', ',', 'comma'], ['45', '2D', '00101101', '-', 'minus'], ['46', '2E', '00101110', '0', 'period'], ['47', '2F', '00101111', '/', 'slash'], ['48', '30', '00110000', '0', 'zero'], ['49', '31', '00110001', '1', 'one'], ['50', '32', '00110010', '2', 'two'], ['51', '33', '00110011', '3', 'three'], ['52', '34', '00110100', '4', 'four'], ['53', '35', '00110101', '5', 'five'], ['54', '36', '00110110', '6', 'six'], ['55', '37', '00110111', '7', 'seven'], ['56', '38', '00111000', '8', 'eight'], ['57', '39', '00111001', '9', 'nine'], ['58', '3A', '00111010', ':', 'colon'], ['59', '3B', '00111011', ';', 'semicolon'], ['60', '3C', '00111100', '<', 'less than'], ['61', '3D', '00111101', '=', 'equality sign'], ['62', '3E', '00111110', '>', 'greater than'], ['63', '3F', '00111111', '?', 'question mark'], ['64', '40', '01000000', '@', 'at sign'], ['65', '41', '01000001', 'A', '\xc2\xa0'], ['66', '42', '01000010', 'B', '\xc2\xa0'], ['67', '43', '01000011', 'C', '\xc2\xa0'], ['68', '44', '01000100', 'D', '\xc2\xa0'], ['69', '45', '01000101', 'E', '\xc2\xa0'], ['70', '46', '01000110', 'F', '\xc2\xa0'], ['71', '47', '01000111', 'G', '\xc2\xa0'], ['72', '48', '01001000', 'H', '\xc2\xa0'], ['73', '49', '01001001', 'I', '\xc2\xa0'], ['74', '4A', '01001010', 'J', '\xc2\xa0'], ['75', '4B', '01001011', 'K', '\xc2\xa0'], ['76', '4C', '01001100', 'L', '\xc2\xa0'], ['77', '4D', '01001101', 'M', '\xc2\xa0'], ['78', '4E', '01001110', 'N', '\xc2\xa0'], ['79', '4F', '01001111', 'O', '\xc2\xa0'], ['80', '50', '01010000', 'P', '\xc2\xa0'], ['81', '51', '01010001', 'Q', '\xc2\xa0'], ['82', '52', '01010010', 'R', '\xc2\xa0'], ['83', '53', '01010011', 'S', '\xc2\xa0'], ['84', '54', '01010100', 'T', '\xc2\xa0'], ['85', '55', '01010101', 'U', '\xc2\xa0'], ['86', '56', '01010110', 'V', '\xc2\xa0'], ['87', '57', '01010111', 'W', '\xc2\xa0'], ['88', '58', '01011000', 'X', '\xc2\xa0'], ['89', '59', '01011001', 'Y', '\xc2\xa0'], ['90', '5A', '01011010', 'Z', '\xc2\xa0'], ['91', '5B', '01011011', '[', 'left square bracket'], ['92', '5C', '01011100', '\\', 'backslash'], ['93', '5D', '01011101', ']', 'right square bracket'], ['94', '5E', '01011110', '^', 'caret / circumflex'], ['95', '5F', '01011111', '_', 'underscore'], ['96', '60', '01100000', '`', 'grave / accent'], ['97', '61', '01100001', 'a', '\xc2\xa0'], ['98', '62', '01100010', 'b', '\xc2\xa0'], ['99', '63', '01100011', 'c', '\xc2\xa0'], ['100', '64', '01100100', 'd', '\xc2\xa0'], ['101', '65', '01100101', 'e', '\xc2\xa0'], ['102', '66', '01100110', 'f', '\xc2\xa0'], ['103', '67', '01100111', 'g', '\xc2\xa0'], ['104', '68', '01101000', 'h', '\xc2\xa0'], ['105', '69', '01101001', 'i', '\xc2\xa0'], ['106', '6A', '01101010', 'j', '\xc2\xa0'], ['107', '6B', '01101011', 'k', '\xc2\xa0'], ['108', '6C', '01101100', 'l', '\xc2\xa0'], ['109', '6D', '01101101', 'm', '\xc2\xa0'], ['110', '6E', '01101110', 'n', '\xc2\xa0'], ['111', '6F', '01101111', 'o', '\xc2\xa0'], ['112', '70', '01110000', 'p', '\xc2\xa0'], ['113', '71', '01110001', 'q', '\xc2\xa0'], ['114', '72', '01110010', 'r', '\xc2\xa0'], ['115', '73', '01110011', 's', '\xc2\xa0'], ['116', '74', '01110100', 't', '\xc2\xa0'], ['117', '75', '01110101', 'u', '\xc2\xa0'], ['118', '76', '01110110', 'v', '\xc2\xa0'], ['119', '77', '01110111', 'w', '\xc2\xa0'], ['120', '78', '01111000', 'x', '\xc2\xa0'], ['121', '79', '01111001', 'y', '\xc2\xa0'], ['122', '7A', '01111010', 'z', '\xc2\xa0'], ['123', '7B', '01111011', '{', 'left curly bracket'], ['124', '7C', '01111100', '|', 'vertical bar'], ['125', '7D', '01111101', '}', 'right curly bracket'], ['126', '7E', '01111110', '~', 'tilde'], ['127', '7F', '01111111', 'DEL', 'delete']]
EXTENDED_CHARS = [['Dec', 'Hex', 'Bin', 'Char', 'Desc'], ['128', '80', '10000000', '\xe2\x82\xac', 'euro'], ['129', '81', '10000001', '\xc2\x81', '\xc2\xa0'], ['130', '82', '10000010', '\xe2\x80\x9a', '\xc2\xa0'], ['131', '83', '10000011', '\xc6\x92', 'florin'], ['132', '84', '10000100', '\xe2\x80\x9e', '\xc2\xa0'], ['133', '85', '10000101', '\xe2\x80\xa6', '\xc2\xa0'], ['134', '86', '10000110', '\xe2\x80\xa0', 'dagger'], ['135', '87', '10000111', '\xe2\x80\xa1', 'double dagger'], ['136', '88', '10001000', '\xcb\x86', '\xc2\xa0'], ['137', '89', '10001001', '\xe2\x80\xb0', 'per-mille'], ['138', '8A', '10001010', '\xc5\xa0', '\xc2\xa0'], ['139', '8B', '10001011', '\xe2\x80\xb9', '\xc2\xa0'], ['140', '8C', '10001100', '\xc5\x92', '\xc2\xa0'], ['141', '8D', '10001101', '\xc2\x8d', '\xc2\xa0'], ['142', '8E', '10001110', '\xc5\xbd', '\xc2\xa0'], ['143', '8F', '10001111', '\xc2\x8f', '\xc2\xa0'], ['144', '90', '10010000', '\xc2\x90', '\xc2\xa0'], ['145', '91', '10010001', '\xe2\x80\x98', '\xc2\xa0'], ['146', '92', '10010010', '\xe2\x80\x99', '\xc2\xa0'], ['147', '93', '10010011', '\xe2\x80\x9c', '\xc2\xa0'], ['148', '94', '10010100', '\xe2\x80\x9d', '\xc2\xa0'], ['149', '95', '10010101', '\xe2\x80\xa2', '\xc2\xa0'], ['150', '96', '10010110', '\xe2\x80\x93', '\xc2\xa0'], ['151', '97', '10010111', '\xe2\x80\x94', '\xc2\xa0'], ['152', '98', '10011000', '\xcb\x9c', '\xc2\xa0'], ['153', '99', '10011001', '\xe2\x84\xa2', 'trademark'], ['154', '9A', '10011010', '\xc5\xa1', '\xc2\xa0'], ['155', '9B', '10011011', '\xe2\x80\xba', '\xc2\xa0'], ['156', '9C', '10011100', '\xc5\x93', '\xc2\xa0'], ['157', '9D', '10011101', '\xc2\x9d', '\xc2\xa0'], ['158', '9E', '10011110', '\xc5\xbe', '\xc2\xa0'], ['159', '9F', '10011111', '\xc5\xb8', '\xc2\xa0'], ['160', 'A0', '10100000', '\xc2\xa0', '\xc2\xa0'], ['161', 'A1', '10100001', '\xc2\xa1', '\xc2\xa0'], ['162', 'A2', '10100010', '\xc2\xa2', 'cent'], ['163', 'A3', '10100011', '\xc2\xa3', 'pound'], ['164', 'A4', '10100100', '\xc2\xa4', 'currency sign'], ['165', 'A5', '10100101', '\xc2\xa5', 'yen, yuan'], ['166', 'A6', '10100110', '\xc2\xa6', 'broken bar'], ['167', 'A7', '10100111', '\xc2\xa7', 'section sign'], ['168', 'A8', '10101000', '\xc2\xa8', '\xc2\xa0'], ['169', 'A9', '10101001', '\xc2\xa9', 'copyright'], ['170', 'AA', '10101010', '\xc2\xaa', 'ordinal indicator'], ['171', 'AB', '10101011', '\xc2\xab', '\xc2\xa0'], ['172', 'AC', '10101100', '\xc2\xac', '\xc2\xa0'], ['173', 'AD', '10101101', '\xc2\xad', '\xc2\xa0'], ['174', 'AE', '10101110', '\xc2\xae', 'registered trademark'], ['175', 'AF', '10101111', '\xc2\xaf', '\xc2\xa0'], ['176', 'B0', '10110000', '\xc2\xb0', 'degree'], ['177', 'B1', '10110001', '\xc2\xb1', 'plus-minus'], ['178', 'B2', '10110010', '\xc2\xb2', '\xc2\xa0'], ['179', 'B3', '10110011', '\xc2\xb3', '\xc2\xa0'], ['180', 'B4', '10110100', '\xc2\xb4', '\xc2\xa0'], ['181', 'B5', '10110101', '\xc2\xb5', 'mu'], ['182', 'B6', '10110110', '\xc2\xb6', 'pilcrow'], ['183', 'B7', '10110111', '\xc2\xb7', '\xc2\xa0'], ['184', 'B8', '10111000', '\xc2\xb8', '\xc2\xa0'], ['185', 'B9', '10111001', '\xc2\xb9', '\xc2\xa0'], ['186', 'BA', '10111010', '\xc2\xba', 'ordinal indicator'], ['187', 'BB', '10111011', '\xc2\xbb', '\xc2\xa0'], ['188', 'BC', '10111100', '\xc2\xbc', '\xc2\xa0'], ['189', 'BD', '10111101', '\xc2\xbd', '\xc2\xa0'], ['190', 'BE', '10111110', '\xc2\xbe', '\xc2\xa0'], ['191', 'BF', '10111111', '\xc2\xbf', 'inverted question mark'], ['192', 'C0', '11000000', '\xc3\x80', '\xc2\xa0'], ['193', 'C1', '11000001', '\xc3\x81', '\xc2\xa0'], ['194', 'C2', '11000010', '\xc3\x82', '\xc2\xa0'], ['195', 'C3', '11000011', '\xc3\x83', '\xc2\xa0'], ['196', 'C4', '11000100', '\xc3\x84', '\xc2\xa0'], ['197', 'C5', '11000101', '\xc3\x85', '\xc2\xa0'], ['198', 'C6', '11000110', '\xc3\x86', '\xc2\xa0'], ['199', 'C7', '11000111', '\xc3\x87', '\xc2\xa0'], ['200', 'C8', '11001000', '\xc3\x88', '\xc2\xa0'], ['201', 'C9', '11001001', '\xc3\x89', '\xc2\xa0'], ['202', 'CA', '11001010', '\xc3\x8a', '\xc2\xa0'], ['203', 'CB', '11001011', '\xc3\x8b', '\xc2\xa0'], ['204', 'CC', '11001100', '\xc3\x8c', '\xc2\xa0'], ['205', 'CD', '11001101', '\xc3\x8d', '\xc2\xa0'], ['206', 'CE', '11001110', '\xc3\x8e', '\xc2\xa0'], ['207', 'CF', '11001111', '\xc3\x8f', '\xc2\xa0'], ['208', 'D0', '11010000', '\xc3\x90', '\xc2\xa0'], ['209', 'D1', '11010001', '\xc3\x91', '\xc2\xa0'], ['210', 'D2', '11010010', '\xc3\x92', '\xc2\xa0'], ['211', 'D3', '11010011', '\xc3\x93', '\xc2\xa0'], ['212', 'D4', '11010100', '\xc3\x94', '\xc2\xa0'], ['213', 'D5', '11010101', '\xc3\x95', '\xc2\xa0'], ['214', 'D6', '11010110', '\xc3\x96', '\xc2\xa0'], ['215', 'D7', '11010111', '\xc3\x97', 'multiplication sign'], ['216', 'D8', '11011000', '\xc3\x98', '\xc2\xa0'], ['217', 'D9', '11011001', '\xc3\x99', '\xc2\xa0'], ['218', 'DA', '11011010', '\xc3\x9a', '\xc2\xa0'], ['219', 'DB', '11011011', '\xc3\x9b', '\xc2\xa0'], ['220', 'DC', '11011100', '\xc3\x9c', '\xc2\xa0'], ['221', 'DD', '11011101', '\xc3\x9d', '\xc2\xa0'], ['222', 'DE', '11011110', '\xc3\x9e', '\xc2\xa0'], ['223', 'DF', '11011111', '\xc3\x9f', '\xc2\xa0'], ['224', 'E0', '11100000', '\xc3\xa0', '\xc2\xa0'], ['225', 'E1', '11100001', '\xc3\xa1', '\xc2\xa0'], ['226', 'E2', '11100010', '\xc3\xa2', '\xc2\xa0'], ['227', 'E3', '11100011', '\xc3\xa3', '\xc2\xa0'], ['228', 'E4', '11100100', '\xc3\xa4', '\xc2\xa0'], ['229', 'E5', '11100101', '\xc3\xa5', '\xc2\xa0'], ['230', 'E6', '11100110', '\xc3\xa6', '\xc2\xa0'], ['231', 'E7', '11100111', '\xc3\xa7', '\xc2\xa0'], ['232', 'E8', '11101000', '\xc3\xa8', '\xc2\xa0'], ['233', 'E9', '11101001', '\xc3\xa9', '\xc2\xa0'], ['234', 'EA', '11101010', '\xc3\xaa', '\xc2\xa0'], ['235', 'EB', '11101011', '\xc3\xab', '\xc2\xa0'], ['236', 'EC', '11101100', '\xc3\xac', '\xc2\xa0'], ['237', 'ED', '11101101', '\xc3\xad', '\xc2\xa0'], ['238', 'EE', '11101110', '\xc3\xae', '\xc2\xa0'], ['239', 'EF', '11101111', '\xc3\xaf', '\xc2\xa0'], ['240', 'F0', '11110000', '\xc3\xb0', '\xc2\xa0'], ['241', 'F1', '11110001', '\xc3\xb1', '\xc2\xa0'], ['242', 'F2', '11110010', '\xc3\xb2', '\xc2\xa0'], ['243', 'F3', '11110011', '\xc3\xb3', '\xc2\xa0'], ['244', 'F4', '11110100', '\xc3\xb4', '\xc2\xa0'], ['245', 'F5', '11110101', '\xc3\xb5', '\xc2\xa0'], ['246', 'F6', '11110110', '\xc3\xb6', '\xc2\xa0'], ['247', 'F7', '11110111', '\xc3\xb7', 'obelus'], ['248', 'F8', '11111000', '\xc3\xb8', '\xc2\xa0'], ['249', 'F9', '11111001', '\xc3\xb9', '\xc2\xa0'], ['250', 'FA', '11111010', '\xc3\xba', '\xc2\xa0'], ['251', 'FB', '11111011', '\xc3\xbb', '\xc2\xa0'], ['252', 'FC', '11111100', '\xc3\xbc', '\xc2\xa0'], ['253', 'FD', '11111101', '\xc3\xbd', '\xc2\xa0'], ['254', 'FE', '11111110', '\xc3\xbe', '\xc2\xa0'], ['255', 'FF', '11111111', '\xc3\xbf', '\xc2\xa0']]

def charmap(a, b="", c="", d=0):
    if d == 0:
        print(b)
        for row in a:
           print ("%-5s %-6s %-5s %-10s %-20s" % (row[1], row[3], row[0], row[2], row[4]))
        print('\t')
    if d == 1:
        print(b)
        print ("%-5s %-6s %-5s %-10s %-20s" % (a[0][1], a[0][3], a[0][0], a[0][2], a[0][4]))
        for row in a:
            check=0
            for dig in row:
                if dig.find(c) != -1:
                   check = 1
            if check == 1:
                print ("%-5s %-6s %-5s %-10s %-20s" % (row[1], row[3], row[0], row[2], row[4]))
        print("\t")

if a.search != "":
    charmap(CTL_CHARS, "CONTROL CHARACTERS", a.search, 1)
    charmap(PRNT_CHARS, "PRINTABLE CHARACTERS", a.search, 1)
    charmap(EXTENDED_CHARS, "EXTENDED CHARACTERS", a.search, 1)
    sys.exit()

if a.charmap != "":
    num = 1 if a.charmap == "c" else 2 if a.charmap == "p" else 3 if a.charmap == "e" else 4 if a.charmap == "a" else 5
    if num == 1 or num == 4:
        charmap(CTL_CHARS, "CONTROL CHARACTERS", "", 0)
    if num == 2 or num == 4:
        charmap(PRNT_CHARS, "PRINTABLE CHARACTERS", "", 0)
    if num == 3 or num == 4:
        charmap(EXTENDED_CHARS, "EXTENDED CHARACTERS", "", 0)
    if num == 5:
        sys.exit()
    sys.exit()



base_16 = "0123456789ABCDEF"
chars = list(base_16)
charArr = []
badchars = []
comparechars = []
daftchar = []
if a.badchars != "ZZZZZ":
    badchars = list(a.badchars.upper().split(" "))

for x in chars[:]:
    for y in chars[:]:
        if ''.join(str(x) + str(y)) not in badchars[:]:
            if a.bytecode == True:
                if a.zero == True:
                    charArr.append(r"0x" + str(x) + str(y))
                else:
                    charArr.append(r"\x" + str(x) + str(y))
            else:
                charArr.append(str(x) + str(y))

if a.compare == True:
    a.badchars = ""
    badchars[:] = []
    charArr[:] = []
    transChar = []
    for x in chars[:]:
        for y in chars[:]:
            transChar.append(str(x) + str(y))

    tempchar = input('Enter existing shellcode.  Enter to complete.\n')
    plank = sorted(tempchar.replace('\\x', ' ').upper().split(' '))
    comp = []
    for item in plank:
        if item not in comp[:] and item != "":
            comp.append(item)

    for lop in transChar:
        if lop not in comp:
            badchars.append(lop)
            a.badchars += lop + " "
    for lop in comp:
        if a.bytecode == True:
            if a.zero == True:
                charArr.append(r"0x" + lop)
            else:
                charArr.append(r"\x" + lop)
        else:
            charArr.append(lop)
    # time.sleep(90)
    if len(charArr) > a.range:
        a.range = len(charArr)
    print('\t')


if a.full == True and len(charArr) > a.range:
    a.range = len(charArr)

nuArr = []
if a.range > 1:
    leng = len(charArr)
    while len(nuArr) < a.range:
        for x in charArr:
            nuArr.append(x)

if len(nuArr) > len(charArr):
    charArr = nuArr
if a.range < len(charArr):
    if a.full == True:
        a.range = len(charArr)


bquote = ""
equote = ""
if a.quote == True:
    bquote = 'notBadChars = "'
    equote = '"'
else:
    bquote = ''
    equote = ''

if a.badchars != "ZZZZZ":
    print("badchars = '" + r'\x' + r'\x'.join(map(str, badchars)) + "'" + "\t## " + str(len(badchars)))
if a.remove_spaces == True:
    print(bquote + ''.join(map(str, charArr[:a.range])) + equote + "\t## " + str(len(charArr[:a.range])))
else:
    print(bquote + ' '.join(map(str, charArr[:a.range])) + equote + "\t## " + str(len(charArr[:a.range])))
if a.badchars != "ZZZZZ":
    print("sadchars = '" + r'\x' + r'\x'.join(map(str, badchars)) + "'" + "\t## " + str(len(badchars)))

if a.nopsled >=1 :
    noppysumbitch = []
    for lol in range (0, a.nopsled):
        if a.bytecode == True:
            if a.zero == True:
                noppysumbitch.append(r"0x" + "90")
            else:
                noppysumbitch.append(r"\x" + "90")
        else:
            noppysumbitch.append("90")
    if a.remove_spaces == True:
        print(bquote + ''.join(map(str, noppysumbitch[:a.nopsled])) + equote + "\t## " + str(len(noppysumbitch[:a.nopsled])))
    else:
        print(bquote + ' '.join(map(str, noppysumbitch[:a.nopsled])) + equote + "\t## " + str(len(noppysumbitch[:a.nopsled])))
