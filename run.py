"""
This module:
* Keeps track of program state
* Interprets user inputs, sending some through main.py
* Sends the state to graphicalOut.py to update the UI


The state needs to know what menu-node is currently active, as well the user's
location within the program.


- read in current data
- offer user options

> Add new log entry
>> Choose between logs until hit leaf
>>> Enter data for new entry
> Add/edit logs
>> Add log
>>> Flick through branches until decide where to add leaf
>>>> Fill in fieds for new log
>> Edit log
>>> Pick log to edit
>>>> Edit location of log in data structure
>>>> Edit fields for log
> View log data
>> Pick log


Menu options stored as nodes, their functions must all be able to run with only State as input.

When an option is selected, if it is a leaf then something along the lines of:
"runMenuOption(currentNode, state)"
is run.

* Build in menu navigation with a runMenuOption simply printing the selected leags' location.


"""


import main

import os

def selectLeaf(current):
    print current
    while True:
        listOfChildren = current.children()
        for i in range(len(listOfChildren)):
            print str(i) + ". " + listOfChildren[i].key()
        if not isinstance(current,main.Root):
            print str(len(listOfChildren)) +". Back"
        else:
            print str(len(listOfChildren)) +". Quit"
        
        userIn = input()
            
        if isinstance(userIn,int):
            if userIn < len(listOfChildren) and userIn >= 0:
                current = listOfChildren[userIn]
            elif userIn == len(listOfChildren):
                current = current.parent()

        if isinstance(current,main.Leaf):
            returnStr = ""
            while not isinstance(current,main.Root):
                returnStr = "/" + current.key() +  returnStr
                current = current.parent()
            returnStr = current.key() + returnStr
            break
        if current == None:
            returnStr = "User quit without selecting an option."
            break
    print returnStr
    return current


dataTypes = {"integer": int,"float": float, "range:": tuple, "choice": main.Root,"timeStamp":"fish"}


def addLogTemplate(branch):
#v0
#-add field, give options for dataType
# number, range, text, choice, timestamp 

    
    while True:
        break
    return None


menu = main.read("Menu.xml")
current = menu
while current != None:
    current = selectLeaf(menu)
    print "User selected:", current



