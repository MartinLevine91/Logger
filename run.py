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


import main
import graphics


def selectNodeChild(current,userIn):

    listOfChildren = current.children()
    
    if isinstance(userIn,int):
        if userIn < len(listOfChildren)+1 and userIn >= 0:
            current = listOfChildren[userIn-1]
        elif userIn == len(listOfChildren)+1:
            current = current.parent()
    
    return current




def addLogTemplate(branch):
#v0
#-add field, give options for dataType
# number, range, text, choice, timestamp 

    
    while True:
        break
    return None


class LoggerState:
    def __init__(self,menu,logRoot):
        self.mode = "Menu"
        self.menu = menu
        self.currentL = logRoot
        self.logs = logRoot
    def returnMode(self):
        return self.mode
    def changeMode(self,newMode):
        if newMode in ["Menu","DisplayInfo","AddEntry","AddEditTemplate"]:
            self.mode = newMode
            return 0
        else:
            print "Invalid mode!"
            print invalidMode


class Choice:
# List of form [[name1, option],
#               [name2,[[name2a,option],[name2b,option]],
#               [name3,option]]
# list[

    def __init__(self, choiceList):
        self.choiceList = choiceList
        self.currentChoiceList = choiceList
        self.keyList = []
        self.name = ""
        
    def updateCurrentList(self):
        currentChoiceList = self.choiceList
        self.name = ""
        for key in self.keyList:
            self.name = currentChoiceList[key][0]
            currentChoiceList = currentChoiceList[key][1]
        self.currentChoiceList = currentChoiceList
        
        
    def pickChoice(self,key):
        # Pick a choice, indexing from one. If currently on a leaf choice, it assumes the wanted choice is "back"        
        if isinstance(self.currentChoiceList,list):
            if key-1 < len(self.currentChoiceList):
                self.keyList.append(key-1)
            elif key-1 == len(self.currentChoiceList):
                self.keyList.pop()

            self.updateCurrentList()
        else:
            self.keyList.pop()
            self.updateCurrentList()

    def addChoice(self,newName,newOption):
        if isinstance(currentChoiceList[0],list):
            #add a sibling option            
            self.currentChoiceList.append([newName,newOption])
        else:
            print error

    def changeName(self,newName):
        if isinstance(currentChoiceList[0], string):
            currentChoiceList[0] = newName
        else:
            print error

    def changeOption(self,newOption):
        if isinstance(currentChoiceList[0], string):
            currentChoiceList[1] = newOption
        else:
            print error
        
    

def userInput():
    try:
        userIn = input()
    except:
        userIn = None
    return userIn


def mainMenu(state):
    if hasattr(state.menu.currentChoiceList, '__call__'):
        #If have selected a function: run it, then return to the parent menu.  
        state.menu.currentChoiceList(state)
        state.menu.pickChoice(0)

    #Draw the menu.
    graphics.drawMainMenu(state.menu)

    #Select the option inputted by the user.
    UI = userInput()
    if isinstance(UI,int) and UI > 0:
        state.menu.pickChoice(UI)
    

def addEntry(state):
    graphics.drawNotYetProgrammed()
    userInput()    

    
def addNewLog(state):



    
    graphics.drawNotYetProgrammed()
    userInput()   

    
def moveLog(state):
    graphics.drawNotYetProgrammed()
    userInput()

    
def editLog(state):
    graphics.drawNotYetProgrammed()
    userInput()

    
def viewData(state):
    graphics.drawNotYetProgrammed()
    userInput()



################################################################################
# RUN - ACTUAL                                                                 #
################################################################################

menu = main.read("Menu.xml")

logs = main.read("Logs.xml")

dataTypes = {"integer": int,"float": float, "range:": tuple, "choice": main.Root,"timeStamp":"fish"}


# List of form [[name1, option],
#               [name2,[[name2a,option],[name2b,option]],
#               [name3,option]]

menu =    Choice( \
               [["Add new log entry", addEntry], \
                ["Add or edit a log template", \
                   [["Add log template", addNewLog], \
                    ["Edit log template", \
                       [["Edit template location within data structure", moveLog], \
                        ["Edit fields of log", editLog]]]]], \
                ["View log data",viewData]])




globalButtons = {}
"""
current = selectLeaf(menu)
print "User selected:", current
"""

state = LoggerState(menu,logs)


for i in range(10):
    mainMenu(state)


    





"""

while True:

    graphics.draw(state)    

    try:
        userIn = input()
    except:
        userIn = None

    state = findNewState(state,userIn)
    
    if isinstance(state.currentM,main.Leaf) and isinstance(state.currentL,main.Leaf):
        break





"""

