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
import graphics

def selectChild(current,userIn):


    listOfChildren = current.children()
    
    if isinstance(userIn,int):
        if userIn < len(listOfChildren)+1 and userIn >= 0:
            current = listOfChildren[userIn-1]
        elif userIn == len(listOfChildren)+1:
            current = current.parent()
    
    return current


dataTypes = {"integer": int,"float": float, "range:": tuple, "choice": main.Root,"timeStamp":"fish"}


def addLogTemplate(branch):
#v0
#-add field, give options for dataType
# number, range, text, choice, timestamp 

    
    while True:
        break
    return None


class LoggerState:
    def __init__(self,currentM,currentL):
        self.mode = "Menu"
        self.currentM = currentM
        self.currentL = currentL
        self.logs = currentL
        self.menu = currentM
    def returnMode(self):
        return self.mode
    def changeMode(self,newMode):
        if newMode in ["Menu","DisplayInfo","AddEntry","AddEditTemplate"]:
            self.mode = newMode
            return 0
        else:
            print "Invalid mode!"
            print invalidMode


def findNewState(state,userIn):
    



    for button in globalButtons:
        print "Not defined!"
        print NotDefined

#If in leaf selecting mode    
    if state.returnMode() == "Menu":
#If currentM is not a leaf:
        if isinstance(state.currentM,main.Branch):
# Select from the children of the currentM
            state.currentM = selectChild(state.currentM,userIn)
# If a leaf was selected
            if isinstance(state.currentM,main.Leaf):
                print "leaf"
        elif isinstance(state.currentL,main.Branch):
            state.currentL = selectChild(state.currentL,userIn)
            if state.currentL == None:
                state.currentL = state.logs
                state.currentM = state.currentM.parent()

                

    return state


################################################################################
# RUN - ACTUAL                                                                 #
################################################################################
"""
%%VIEW MODES%%
!!
_____________________________
Title bar
----------------------------
!Content!





!Content!
-----------------------------
Instruction bar
-----------------------------
User input bar

_____________________________
!!

Examples:

Title bar: "Menu selction: ~/'Add or edit log templates'/..."
Content: List of options (add logs, edit logs, back)
Instruction bar: "Select menu option from above."
User input: "1"

Title bar: "Adding entries to Health/'Toilet Visit'"
Content: Table of previous entries.
Instruction bar: "Rate consistency on a scale of 0 to 10, 'H' for help with this datum, 'B' to go back to previous datum or 'Q' to quit entry"
User input: "4.5"

Title bar: "Editting log template - Health/Sleep"
Content: Table of datums, complete with defaults and ranges etc. Followed by list of options/instructions for next part of next datum
Instruction bar: "Choose a data type from the list for 'Asleep by'"
User input: "4"








"""
menu = main.read("Menu.xml")

logs = main.read("Logs.xml")

globalButtons = {}
"""
current = selectLeaf(menu)
print "User selected:", current
"""

state = LoggerState(menu,logs)



while True:

    graphics.draw(state)    


    userIn = input()


    state = findNewState(state,userIn)
    

    if isinstance(state.currentM,main.Leaf) and isinstance(state.currentL,main.Leaf):
        break


