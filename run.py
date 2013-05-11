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


def userInput():
    try:
        userIn = raw_input()
        try:
            userIn = int(userIn)
        except:
            try:
                userIn = str(userIn)
            except:
                pass
    except:
        userIn = None
    return userIn




def mainMenu(state):

    done = False
    
    while True:
        if hasattr(state.menu.currentChoiceList, '__call__'):
            #If have selected a function: reset the log tree, run the function, then return to the parent menu.  
            state.currentL = state.logs
            if state.menu.currentChoiceList(state) == -1:
                break
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

# Find place for new log
# Name it
# Confirm name, then create log
# 
#
#
#
#
#
#
#
    state.currentL = state.logs
    graphics.drawPickLog("AddNewLog",state)

    while True:
        UI = userInput()
        if isinstance(UI, int) and UI > 0:
            if UI-1 < len(state.currentL.children()):
                state.currentL = state.currentL.children()[UI-1]
                if isinstance(state.currentL,main.Leaf):
                    state.currentL = state.currentL.parent()
                    graphics.drawPickLog("AddNewLog_noLeaves",state)
                else:
                    graphics.drawPickLog("AddNewLog",state)

            elif UI-1 == len(state.currentL.children()):
                state.currentL = state.currentL.parent()
                if state.currentL == None:
                    state.currentL = state.logs
                    return 0
                graphics.drawPickLog("AddNewLog",state)

            else:
                graphics.drawPickLog("AddNewLog",state)



                
        elif isinstance(UI, str):
            if UI.lower() in ["branch","b"]:
                newLogName = askConfirmString("NameNewLogBranch")
                if newLogName != None:
                    state.currentL.branch(newLogName)
                graphics.drawPickLog("AddNewLog",state)
            elif UI.lower() in ["leaf","l"]:
                newLogName = askConfirmString("NameNewLogLeaf")
                if newLogName != None:
                    state.currentL.leaf(newLogName)
                    state.currentL = state.currentL.find(newLogName)
                    editLog(state)
                    break    
                # editLogTemplate - addDatum, 
                
                
            else:
                graphics.drawPickLog("AddNewLog",state)
        else:
            graphics.drawPickLog("AddNewLog_noLeaves",state)


        
    graphics.drawNotYetProgrammed()
    userInput()
    return 0

    
def moveLog(state):
    graphics.drawNotYetProgrammed()
    userInput()
    return 0

    
def editLog(state):
    while True:
        if not isinstance(state.currentL, main.Leaf):
            if state.currentL == None:
                state.currentL = state.logs
            graphics.drawPickLog("EditLog",state)
            UI = userInput()
            if isinstance(UI,int):
                if UI-1 < len(state.currentL.children()):
                    state.currentL = state.currentL.children()[UI-1]
                elif UI-1 == len(state.currentL.children()):
                    state.currentL = state.currentL.parent()
                    if state.currentL == None:
                        state.currentL = state.logs
                        return 0
        else:
            print state.currentL.fields()
            content = graphics.TableOfFields(state.currentL)
            print content
            graphics.drawWindow([ "Fields for "+state.currentL.key()],content,["Haven't actual done this proper, just press anything to move on"],["$"])
            userInput()
            break
                    
            
    graphics.drawNotYetProgrammed()
    userInput()
    return 0

    
def viewData(state):
    graphics.drawNotYetProgrammed()
    userInput()
    return 0

def quitProgram(state):
    while True:
        graphics.askYesNo("Are you sure you want to quit?")
        UI = userInput()
        if isinstance(UI,str):
            if UI.lower() in ["y","yes"]:
                break
            if UI.lower() in ["n","no"]:
                return 0
        if UI == 1:
            break
    state.logs.write("Logs.xml")
    return -1

def askConfirmString(key):
    questionDict = {
        "NameNewLogBranch":[["Name new branch","","Type the name of the new branch, then press enter.","$"],
                      ["Confirm branch name","Confirm that you want the new branch to be named '%s'.","Enter 'Yes' or 'Y' to confirm, or 'No' or 'N' to enter something different. Alternatively, if you don't want to create a new branch, enter 'Quit' or 'Q'.","$"]],

        "NameNewLogLeaf":[["Name new leaf","","Type the name of the new leaf, then press enter.","$"],
                      ["Confirm leaf name","Confirm that you want the new leaf to be named '%s'.","Enter 'Yes' or 'Y' to confirm, or 'No' or 'N' to enter something different. Alternatively, if you don't want to create a new branch, enter 'Quit' or 'Q'.","$"]],

        }
    askInfo, confirmInfo = questionDict[key]

    
    progress = "ask"

    while True:
        if progress == "ask":
            title,content,instruction,prompt = askInfo
            graphics.splitAndDraw(title,content,instruction,prompt)
            ans = userInput()
            if isinstance(ans, str):
                progress = "confirm"
        if progress == "confirm":
            title,content,instruction,prompt = confirmInfo
            if "%s" in content:        
                content = content % ans
            graphics.splitAndDraw(title,content,instruction,prompt)
            UI = userInput()
            if isinstance(UI, str):
                if UI.lower() in ["y","yes"]:
                    return ans
                if UI.lower() in ["q","quit"]:
                    return None
                if UI.lower() in ["n","no"]:
                    progress = "ask"
                
        


################################################################################
# RUN - ACTUAL                                                                 #
################################################################################

logs = main.read("Logs.xml")

dataTypes = {"integer": int,"float": float, "range:": tuple, "choice": main.Root,"timeStamp":"fish"}


# List of form [[name1, option],
#               [name2,[[name2a,option],[name2b,option]],
#               [name3,option]]

menu =    main.Choice( \
               [["Add new log entry", addEntry], \
                ["Add or edit a log template", \
                   [["Add log template", addNewLog], \
                    ["Edit log template", \
                       [["Edit template location within data structure", moveLog], \
                        ["Edit fields of log", editLog]]]]], \
                ["View log data",viewData], \
                ["Quit",quitProgram]])




globalButtons = {}
"""
current = selectLeaf(menu)
print "User selected:", current
"""

state = LoggerState(menu,logs)


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

