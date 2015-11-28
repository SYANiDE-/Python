"""Provides support for client list."""
from os import path
from string import rstrip, upper
from copy import deepcopy


class ClientList():
    """Clients list object."""

    def __init__(self,
                 MaxColumns = 6,
                 Column_Width = 12,
                 Char_Separator = "*",
                 ClientListFile = "data/clients.lst"):
        """Initialize the client list object by reading from the '__ClientFile' file.
        MaxColumns = maximum number of columns the table should be.
        Column_Width = maximum width in characters for the columns.
        Char_Separator = the character to use as a separator between column headers and column data.
        ClientListFile = the client file for persistent storage.
        """

        self.__maxCols = MaxColumns
        self.__columnSize = Column_Width
        self.__separator = Char_Separator
        self.__ClientFile = ClientListFile
        self.__OLDSELF = []
        self.__DIFF_ITEMS = []
        self.__DIFFCOUNT = 0
        if path.exists(self.__ClientFile):
            with open(self.__ClientFile, 'r') as tmp:
                t = sorted(map(rstrip, tmp))
                self.clients = []
                for item in t:
                    self.clients.append(upper(item))
            tmp.close()
        else:
            self.clients = []
            z = open(self.__ClientFile, 'w')
            z.close()
        self.__OLDSELF = deepcopy(self.clients)
        self.__OLDSELF.sort()

    def add(self, thewhat):
        """ADDS a client to the list object."""
        t = deepcopy(self.clients)
        t.append(upper(thewhat))
        self.clients = sorted(t)

    def remove(self, thewhat):
        """REMOVES a client from the list object."""
        iterator = 0
        for i in self.clients:
            if str(upper(thewhat)) == i:
                self.clients.pop(iterator)
                break
            iterator += 1

    def write(self):
        """WRITES the changes to the '__ClientFile'."""
        wr = open(self.__ClientFile, 'w')
        for i in range(0, len(self.clients)):
            wr.write(self.clients[i] + '\n')
        wr.close()
        self.__DIFF_ITEMS = []
        self.__OLDSELF = deepcopy(self.clients)

    def tabulate(self):
        """TABULATE the client list object."""
        self.__tablePrinter("Client(s)", self.clients)

    def announce(self):
        """RETURNS the client list object."""
        return self.clients

    def diff(self):
        """DIFFERENTIATES between the old __ClientFile and the new __ClientFile."""
        a = set(self.clients).union(set(self.__OLDSELF))
        b = set(self.clients).intersection(set(self.__OLDSELF))
        c = list(a - b)
        c.sort()
        self.__DIFF_ITEMS = deepcopy(c[:])
        self.__DIFF_ITEMS.sort()
        added = []
        deleted = []
        for i in self.clients:
            if i not in self.__OLDSELF:
                added.append(i)
        for i in self.__OLDSELF:
            if i not in self.clients:
                deleted.append(i)
        added.sort()
        deleted.sort()
        self.__DIFFCOUNT = len(deleted) + len(added)
        if self.__DIFFCOUNT != 0:
            self.__tablePrinter("Added", added, 1)
            self.__tablePrinter("Deleted", deleted, 1)
        else:
            print ("No changes have been made.")

    def __isDividesBy(self, num, base):
        """Check if a number is an exponent of another.  Return true or false."""
        if num <= 0 or num == 1 or base == 1 or base <= 0:
            return False
        if num % base == 0:
            return True
        return False

    def __tablePrinter(self, colLabel, lstObj, toCompare=0 ):
        """Prints a two-dimensional table, somewhat proportional to screen size and number of elements.
            colLabel = Label for the column.
            lstObj = The list to iterate over.
            toCompare = (Set to "1" if we're printing difference objects, and not the clientlist).
        """
        itemcount = len(lstObj)
        if itemcount == 0:
            return False
        Count = itemcount / 3
        if len(colLabel) > self.__columnSize:
            self.columnSize = len(colLabel) + 2
        HDR = str(self.__separator) * (self.__columnSize - 2)
        dynPlace = "%-" + str(self.__columnSize) + "s"
        if Count > self.__maxCols:
            Count = self.__maxCols
        if Count < 1:
            Count = 1
        for i in range(0, Count):
            print(dynPlace % (colLabel)),
            if i > 1 and i % Count == 0:
                print(" ")
        print(" ")
        for i in range(0, Count):
            print(dynPlace % (HDR)),
            if i > 1 and i % Count == 0:
                print(" ")
        print(" ")
        if toCompare == 1:
            if Count != 1:
                printed = 0
                for j in range(0, self.__DIFFCOUNT):
                    for i in range(0, itemcount):
                        if lstObj[i] == self.__DIFF_ITEMS[j]:
                            print(dynPlace % (lstObj[i])),
                            printed += 1
                            if (self.__isDividesBy(printed, Count)) and printed > 1:
                                print(" ")
            else:
                for j in range(0, self.__DIFFCOUNT):
                    for i in range(0, itemcount):
                        if lstObj[i] == self.__DIFF_ITEMS[j]:
                            print(dynPlace % (lstObj[i]))
        else:
            if Count != 1:
                printed = 0
                for i in range(0, itemcount):
                    print(dynPlace % (lstObj[i])),
                    printed += 1
                    if printed > 1 and self.__isDividesBy(printed, Count):
                        print("")
            else:
                for i in range(0, itemcount):
                    print(dynPlace % (lstObj[i]))
        print(" ")
        print(" ")


def main():
    """Exec block when run as main."""
    pass

if __name__ == "__main__":
    main()
