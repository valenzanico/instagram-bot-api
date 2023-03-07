import time

list = ["Beaterr", "eagle", "nmescquock", " cazzo nes o", "dioebuono ", "roma è vella"]

def printList():
    for i in list:
        yield i
lists = printList()

print(next(lists))
lists.send("ciao")

lists.send("ciao")
print(next(lists))
print(next(lists))
lists.send("ciao")