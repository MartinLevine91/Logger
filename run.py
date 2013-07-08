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
import json


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
                if userIn == "":
                    userIn = None
            except:
                userIn = None
    except:
        userIn = None
    if isinstance(userIn, str) and userIn.lower() == "kill program":
        main.complain("Got kill request")
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
            #If a log template hasn't already been selected, navigate to one.        
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
            #Give options to add or edit a field.
            while True:
                
                content = graphics.TableOfFields(state.currentL)
                instructions = graphics.splitToWidth(
                    "Pick a current field by entering it's number, start a new field by entering 'N' or 'new' or press enter 'B' or 'Back' to stop editing fields."
                    )
                graphics.drawWindow([ "Fields for "+state.currentL.key()],content,instructions,["$"])
                UI = userInput()
                if isinstance(UI, int):
                    if UI >= 0 and UI < len(state.currentL.fields()):
                        editField(currentL,state.currentL.fields()[UI])
                    else:
                        content = graphics.TableOfFields(state.currentL)
                        instructions = graphics.splitToWidth(
                            "Pick a current field by entering its number, start a new field by entering 'N' or 'new' or press enter 'B' or 'Back' to stop editing fields."
                            )
                        graphics.drawWindow([ "Fields for "+state.currentL.key()],content,instructions,["$"])
                        UI = userInput()
                elif isinstance(UI, str):
                    if UI.lower() in ["b", "back"]:
                        return 0
                    elif UI.lower() in ["n","new"]:
                        editField(graphics.TableOfFields(state.currentL))
                
                
            break
                    
            
    graphics.drawNotYetProgrammed()
    userInput()
    return 0

def editField(currentL,field = None):



#        key,[dataType ,typeDate],default,optional,helpStr,hidden = fieldAsTable
    key = None
    datatype = None
    typeData = None
    optional = None
    default = None
    helpStr = None
    hidden = False


    if field != None:
        key = field.key()

        datatype_str = field.datatype
        datatype_lst = json.loads(datatype_str)
        
        datatypeList = json.loads(datatype_str)
        datatype = datatypeList[0]
        typeData = datatypeList[1]
        hidden = field.hidden
        optional = field.optional
        default = field.default
        helpStr = field.help
    
    nextToEdit = "help"


    


    while True:
        
        fieldsTable = graphics.TableOfFields(state.currentL, graphics.WINDOW_WIDTH, field, [key,datatype,typeData,default,optional,helpStr,hidden])

        fieldTable = graphics.drawField(None,[key,datatype,typeData,default,optional,helpStr,hidden])
        fullContent = fieldsTable + ["-" * graphics.WINDOW_WIDTH] + fieldTable

        thingsToEdit = ["key","datatype","type data","hidden","optional","default","help"]
        if nextToEdit in thingsToEdit:
            i = thingsToEdit.index(nextToEdit)
            i = (i+1)%(len(thingsToEdit))
            nextToEdit = thingsToEdit[i]
            if nextToEdit == "type data":
                if datatype not in ["Range","Time","Choice"]:
                   nextToEdit = "hidden"     
            if nextToEdit == "default":
                if optional == False:
                   nextToEdit = "help"
            


        if key == None:
            nextToEdit = "key"
        elif datatype == None:
            nextToEdit = "datatype"
        elif datatype in ["Range","Time","Choice"] and typeData == None:
            nextToEdit = "type data"
        elif hidden == None:
            nextToEdit = "hidden"
        elif optional == None:
            nextToEdit = "optional"
        elif optional == True and default == None:
            nextToEdit = "default"
        elif helpStr == None:
            nextToEdit = "help"


        



        inst_str_whatNext  = "Either pick an option or press enter with the input blank to edit %s next." %(nextToEdit,)

        inst_whatNext = graphics.splitToWidth(inst_str_whatNext,graphics.WINDOW_WIDTH)

        shift = [0,0]
        
        inst_whatNext += [graphics.cutTo(str(1) + ". Key",graphics.WINDOW_WIDTH)]
        inst_whatNext += [graphics.cutTo(str(2) + ". Datatype",graphics.WINDOW_WIDTH)]
        if datatype in ["Range","Time","Choice"]:
            shift[0]= 1
            inst_whatNext += [graphics.cutTo(str(3) + ". Type data",graphics.WINDOW_WIDTH)]
        inst_whatNext += [graphics.cutTo(str(3 + shift[0]) + ". Hidden",graphics.WINDOW_WIDTH)]
        inst_whatNext += [graphics.cutTo(str(4 + shift[0]) + ". Optional",graphics.WINDOW_WIDTH)]

        if optional == True:
            shift[1] = 1
            inst_whatNext += [graphics.cutTo(str(5+ shift[0]) + ". Default",graphics.WINDOW_WIDTH)]
        inst_whatNext += [graphics.cutTo(str(5 + shift[0] +shift[1]) + ". Help",graphics.WINDOW_WIDTH)]

        inst_whatNext += [graphics.cutTo("Alternatively, enter 'Done' to save and quit or 'Cancel to quit without saving.",graphics.WINDOW_WIDTH)]
#User inputs, if they input None, then do this.

        
        maxLenFieldsTable = graphics.WINDOW_HEIGHT - len(inst_whatNext) - len(fieldTable) - 6
        if maxLenFieldsTable > 1:
            fullContent = fieldsTable[:maxLenFieldsTable] + ["-" * graphics.WINDOW_WIDTH] + fieldTable
        else:
            fullContent = fieldTable


        
        graphics.drawWindow(["Editing field '%s'" %(key,)],fullContent,inst_whatNext,["$ "])        
        UI = userInput()

        getNewInput = False
        if isinstance(UI, str):
            if UI.lower() in ["done","d"]:
                graphics.drawNotYetProgrammed()
                userInput()
                return 0
            if UI.lower() in ["cancel","c"]:
                return 0
            else:
                getNewInput = True
        elif isinstance(UI, int):
            if UI > 0 and UI <= (6 + shift[0] + shift[1]):
                if shift[0] == 0 and shift[1] == 0:
                    nextToEdit = ["key","datatype","hidden","optional","help"][UI-1]
                elif shift[0] == 1 and shift[1] == 0:
                    nextToEdit = ["key","datatype","type data","hidden","optional","help"][UI-1]
                elif shift[0] == 0 and shift[1] == 1:
                    nextToEdit = ["key","datatype","hidden","optional","default","help"][UI-1]
                elif shift[0] == 1 and shift[1] == 1:
                    nextToEdit = ["key","datatype","type data","hidden","optional","default","help"][UI-1]
                else:
                    getNewInput = True
        elif UI != None:
            getNewInput = True


        print getNewInput
        print nextToEdit
        if not getNewInput:
            if nextToEdit == "key":
                
                cont = True
                while cont:
                    inst_string = "Enter new key, or press enter leaving the input blank to leave the key as it was." 
                    inst = graphics.splitToWidth(inst_string,graphics.WINDOW_WIDTH)
                    maxLenFieldTable = graphics.WINDOW_HEIGHT - len(inst) - 5
                    fullContent = fieldTable[:maxLenFieldTable]

                    graphics.drawWindow(["Editing key for field '%s'" %(key,)],fullContent,inst,["$"])
                    UI = userInput()
                    print "UI: ", UI 
                    if isinstance(UI, str):
                        key = UI
                        cont = False
                    elif UI == None:
                        if key == None:
                            while True:
                                graphics.askYesNo("Do you wish to leave the key blank? If you do so you won't be able to save the field")
                                UI = userInput()
                                if isinstance(UI,str):
                                    if UI.lower() in ["y","yes"]:
                                        cont = False
                                        break
                                    if UI.lower() in ["n","no"]:
                                        break
                        else:
                            cont = False
            elif nextToEdit == "datatype":
                cont = True
                inst_string_1 = "Choose from the following options for datatype:"
                inst = graphics.splitToWidth(inst_string_1,graphics.WINDOW_WIDTH)
                typeList = ["String","Int","Float","Range","Choice","Time"]
                for i in range(len(typeList)):
                    inst.append(graphics.cutTo((str(i+1) + ". " + typeList[i]),graphics.WINDOW_WIDTH))
                inst_string_2 = "Alternatively press enter leaving the input blank to leave datatype as it was."
                inst = inst + graphics.splitToWidth(inst_string_2,graphics.WINDOW_WIDTH)

                maxLenFieldTable = graphics.WINDOW_HEIGHT - len(inst) - 5
                fullContent = fieldTable[:maxLenFieldTable]

                while cont:
                                
                    graphics.drawWindow(["Picking datatype for field '%s'" %(key,)],fullContent,inst,["$"])
                    UI = userInput()
                    if isinstance(UI, int):
                        if UI > 0 and UI <= len(typeList):
                            if typeList[UI-1] != datatype:
                                datatype = typeList[UI-1]
                                typeData = None
                            cont = False
                    elif UI == None:
                        if datatype == None:
                            while True:
                                graphics.askYesNo("Do you wish to leave the datatype blank? If you do so you won't be able to save the field")
                                UI = userInput()
                                if isinstance(UI,str):
                                    if UI.lower() in ["y","yes"]:
                                        cont = False
                                        break
                                    if UI.lower() in ["n","no"]:
                                        break
                        else:
                            cont = False         
            elif nextToEdit == "type data":
                print "Here"
                if datatype == "Range":
                    if typeData == None:
                        rMin = "?"
                        rMax = "?"
                    else:
                        print typeData
                        rMin, rMax = typeData
                        
                    cont = "min"
                    while True:
                        if cont == "min":
                            instStr = "Enter the minimum value for the range or press enter leaving the input blank to leave it as is."
                            inst = graphics.splitToWidth(instStr,graphics.WINDOW_WIDTH)
                            
                            maxLenFieldTable = graphics.WINDOW_HEIGHT - len(inst) - 5
                            fullContent = fieldTable[:maxLenFieldTable]

                            graphics.drawWindow(["Setting minimum for field '%s'" %(key,)],fullContent,inst,["$"])
                            UI = userInput()
                            if isinstance(UI, int):
                                rMin = UI
                                if isinstance(rMax, int):
                                    typeData = [rMin,rMax]
                                else:
                                    typeData = [rMin,"?"]
                                cont = "max"
                            elif isinstance(UI, None):
                                cont = "max"
                        if cont == "max":
                            instStr = "Enter the maximum value for the range or press enter leaving the input blank to leave it as is."
                            inst = graphics.splitToWidth(instStr,graphics.WINDOW_WIDTH)
                            
                            maxLenFieldTable = graphics.WINDOW_HEIGHT - len(inst) - 5
                            fullContent = fieldTable[:maxLenFieldTable]

                            graphics.drawWindow(["Setting maximum for field '%s'" %(key,)],fullContent,inst,["$"])
                            UI = userInput()
                            if isinstance(UI, int):
                                rMax = UI
                                if isinstance(rMin, int):
                                    typeData = [rMin,rMax]
                                else:
                                    typeData = ["?",rMax]
                                if rMin < rMax:
                                    cont = "False"
                                else:
                                    cont = "min"
                            elif isinstance(UI, None):
                                cont = "False"
                        if cont == "False":
                            if isinstance(rMin, int) and isinstance(rMax,int) and rMin < rMax:
                                typeData = [rMin,rMax]
                                break
                            else:
                                instStr = "The current values or min and max are invalid. Until this is fixed you won't be able to enter data in this field. Enter 'min' to change min, 'max' to change max or leave the input blank to exit anyway."
                    
                                maxLenFieldTable = graphics.WINDOW_HEIGHT - len(inst) - 5
                                fullContent = fieldTable[:maxLenFieldTable]

                                graphics.drawWindow(["Leave min and max for '%s' unedited?" %(key,)],fullContent,inst,["$"])
                                UI = userInput()
                                if isinstance(UI, str):
                                    if UI.lower() in ["min", "max"]:
                                        cont = UI.lower()
                                elif isinstance(UI, None):
                                    break

                    pass
                elif datatype == "Choice":
                    pass
                elif datatype == "Time":
                    pass
                else:
                    main.complain("%s has no type data" %(datatype,))

                    


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
                

def getData(dataType_str,title,content):
    dataFunctionDict = {
        "String":getString,
        "Int":getInt,
        "Float":getFloat,
        "Range":getRange,
        "Choice":getChoice,
        "Time":getTime}

    if not main.validDatatype(dataType_str):
        main.complain("Invalid data type, cannot get data.")
    else:
        dataType = json.loads(datatype_str)
        return dataFunctionDict[dataType[0]](title, content,dataType)



    

def getString(title, content,dataType):
    

    pass
def getInt(title, content,dataType):
    pass
def getFloat(title, content,dataType):
    pass
def getRange(title, content,dataType):
    pass
def getChoice(title, content,dataType):
    pass
def getTime(title, content,dataType):
    pass


################################################################################
# RUN - ACTUAL                                                                 #
################################################################################


logs = main.read("Logs.xml")



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

