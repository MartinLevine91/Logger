

import main
import graphics
import json

import time

FOLLOW_PRESETS = True
RECORD_INPUTS = True
USER_INPUT_PRESETS =[1, 1, 1, None, 0, None, 0, None, 0, None, 0, None, 0]
USER_INPUT_RECORDING = []
DELAY_TIMER = 0.1




def selectNodeChild(current,userIn):

    listOfChildren = current.children()

    if isinstance(userIn,int):
        if userIn < len(listOfChildren)+1 and userIn >= 0:
            current = listOfChildren[userIn-1]
        elif userIn == len(listOfChildren)+1:
            current = current.parent()
    return current

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
        if (not FOLLOW_PRESETS) or not USER_INPUT_PRESETS:
            userIn = raw_input()
        else:
            userIn = USER_INPUT_PRESETS.pop(0)
            time.sleep(DELAY_TIMER)
            print userIn
        try:
            userIn = float(userIn)
            if abs(int(userIn + 0.5)-userIn) < 0.00001:
                userIn = int(userIn+0.5)
        except:
            try:
                # NDL 2013-07-14 -- raw_input() always returns a
                # string, so str() and the enclosing try: are
                # unnecessary.
                userIn = str(userIn)
                if not main.validString(userIn):
                    userIn = None
                if userIn == "":
                    userIn = None
            except:
                userIn = None
    except:
        userIn = None
    if RECORD_INPUTS == True:
        str_UI = str(userIn)
        if str_UI == "None":
            str_UI = ""
        USER_INPUT_RECORDING.append(userIn)
        print "Recorded input so far:", USER_INPUT_RECORDING
    if isinstance(userIn, str) and userIn.lower() == "kill program":
        main.complain("Got kill request")
    return userIn


def yesOrNo(query):
    while True:
        graphics.askYesNo(query)
        UI = userInput()
        if isinstance(UI, str):
            if match(UI, "yes"):
                return True
            elif match(UI,"no"):
                return False


def match(substring, string):
    substring=substring.lower()
    string=string.lower()
    return len(substring)>0 and string.find(substring)==0


def mainMenu(state):
    done = False
    while True:
        if hasattr(state.menu.currentChoiceList, '__call__'):
            #If have selected a function: reset the log tree, run the function, then return to the parent menu.
            state.currentL = state.logs
            output = state.menu.currentChoiceList(state)
            if output == -1:
                output = quitProgram(state, True)
            if output == -2:
                break
            state.menu.pickChoice(0)
            state.logs.write("backup/Temp_Logs.xml") 
        #Draw the menu.
        graphics.drawMainMenu(state.menu)
        #Select the option inputted by the user.
        UI = userInput()
        if isinstance(UI,int) and UI > 0:
            state.menu.pickChoice(UI)
            

def selectAddEntryLeaf(state):
    while not isinstance(state.currentL, main.Leaf):
        if state.currentL == None:
            state.currentL = state.logs
        graphics.drawPickLog("AddEntry",state)
        UI = userInput()
        if isinstance(UI,int):
            if UI-1 < len(state.currentL.children()):
                state.currentL = state.currentL.children()[UI-1]
            # Hack to take us up one level.
            elif UI-1 == len(state.currentL.children()):
                state.currentL = state.currentL.parent()
                if state.currentL == None:
                    # We went up so many levels we have to stop now.
                    state.currentL = state.logs
                    return False
    return True


def addEntry(state, log=None):
    while True:
        if not log:
            # Pick a leaf onto which an entry can be added
            if not selectAddEntryLeaf(state):
                return 0
            log = state.currentL
        output = addEntry_dataLoop(log)
        if output == -1:
            return -1
        elif output == 0:
            return 0
        elif output == 1:
            log = None
            state.currentL = None
        else:
            main.complain("Shouldn't be able to get here")

def addEntry_dataLoop(log):
    fields = log.fields()
    fieldsTable = graphics.TableOfFields(log, graphics.WINDOW_WIDTH)
    partialEntry = {}
    index = 0
    count = 0
    while True:
        # if partial = none
        if (index ==0 and not partialEntry):
            output = addEntry_dataLoop_intro(log,fields,fieldsTable)
            if isinstance(output, int):
                return output
        # enter data
        field = fields[index]
        partialEntry = addEntry_augmentPartialEntry(partialEntry, field, index, log)
        index += 1
        # break screen
        index, partialEntry, command =  addEntry_dataLoop_break(index, partialEntry, log,fields)
        if isinstance(command, int):
            return command
        count += 1
        if count == 100:
            count = 0
            state.logs.write("backup/Temp_Logs.xml")


def addEntry_dataLoop_intro(log,fields,fieldsTable):
    #intro screen draw
    titleStr = "Adding entries to %s - start new entry?" % (log.key(),)
    title = [graphics.cutTo(titleStr)]
    instStr = "To start adding an entry, press enter leaving the input blank. Starting with %s." + \
              "Alternatively enter, 'Back' to go back to leaf selection, 'Done' to stop adding " + \
              "entries or 'Quit' to save and quit the Logger."
    instStr = instStr %(fields[0].key(),)
    inst = graphics.splitToWidth(instStr)
    
    spare = graphics.WINDOW_HEIGHT - 6 - len(inst)
    maxLenFieldsTable = min(spare * 2 / 3, len(fieldsTable))
    maxLenDataTable = spare - maxLenFieldsTable

    dataTable = graphics.drawRecentData(leaf=log, maxHeight=maxLenDataTable)
    content = fieldsTable[:maxLenFieldsTable] + [graphics.WINDOW_WIDTH * "-",] + dataTable

    #input loop
    UI = False
    while True:
        graphics.drawWindow(title, content, inst, ["$ ",])
        UI = userInput()
        if isinstance(UI, str):
            if match(UI,"done"):
                #quit to menu
                return 0
            elif match(UI,"back"):
                #back to leaf selection
                return 1
            elif match(UI,"quit"):
                #quit the logger
                return -1
        elif UI == None:
            return None

def addEntry_dataLoop_break(index, partialEntry, log,fields):
    # draw break screen
    titleStr = "Break screen - adding new entry to %s" % (log.key(),)
    title = [graphics.cutTo(titleStr),]

    navOptions = addEntry_assessOptions(fields, index, partialEntry)
    mayGoBack, selectLimit, mayComplete = navOptions
    insts = addEntry_genInsts(index, fields, mayGoBack, -1, mayComplete)

    width = graphics.WINDOW_WIDTH
    blankLine =  [(width*" "),]
    breakLine =  [(width*"-"),]

    
    if  index < len(fields) or not mayComplete:
        miniPrev = graphics.miniDrawField(fields[index-1], log,partialEntry,"previous")
        miniNext = graphics.miniDrawField(fields[index%len(fields)], log,partialEntry,"next")

        breakScreen =   title + \
                        breakLine + 2*blankLine + \
                        [graphics.cutTo("Previous Field"),] + \
                        breakLine + miniPrev + \
                        breakLine + 2*blankLine + \
                        [graphics.cutTo("Next Field"),] + \
                        breakLine + miniNext + \
                        breakLine
    else:
        miniPrev = graphics.miniDrawField(fields[index-1], log,partialEntry,"previous")
        dataTable = graphics.drawRecentData(leaf=log, priorityCol = index-1,unfinishedEntry = partialEntry, maxHeight=2)

        breakScreen =   title + \
                        breakLine + 2*blankLine + \
                        [graphics.cutTo("Completed entry"),] + \
                        breakLine + dataTable + \
                        breakLine + 2*blankLine + \
                        [graphics.cutTo("Previous Field"),] + \
                        breakLine + miniPrev + \
                        breakLine



    spare = graphics.WINDOW_HEIGHT - len(breakScreen) - len(insts) - 2

    breakScreen =   breakScreen + \
                    spare*blankLine + \
                    insts + breakLine

# if at i = i-max and all non-optional complete then "" for done and "loop" to loop round and set i = 0

    #input loop
    UI = False
    while True:
        for line in breakScreen:
            print line
        print "$ ",
        UI = userInput()
        if isinstance(UI, str):
            if match(UI,"option"):
                #not yet programmed
                index,partialEntry,breakScreen = addEntry_dataLoop_option(index, partialEntry, log,fields, breakScreen)
            if match(UI,"quit"):
                #quit the logger (possibly saving the entry first)
                quitStr = "Are you sure you want to quit?"
                if not mayComplete:
                    quitStr = quitStr + " Doing so means throwing away this partially completed log entry."
                if yesOrNo("Are you sure you want to quit?"):
                    if mayComplete:
                        if yesOrNo("Save entry before quiting?"):
                            addEntry_saveEntry(fields, log, partialEntry)
                    return 0, {}, -1
            elif match(UI,"cancel"):
                #cancel the entry and go back to main menu
                cancelStr = "Are you sure you want to throw away this partially completed log entry and return to the menu?"
                if yesOrNo(cancelStr):
                    return 0, {}, 0
            elif match(UI,"restart"):
                #delete the entry and go to intro screen
                restartStr = "Are you sure you want to throw away this partially completed entry and start again?"
                if yesOrNo(restartStr):
                    return 0, {}, None
            elif match(UI,"done") and mayComplete:
                #save entry, go to intro screen
                addEntry_saveEntry(fields, log, partialEntry)
                return 0, {}, None
            elif match(UI,"back"):
                #re-enter last field
                return index-1, partialEntry, None
            elif match(UI,"back") and (index  == len(fields) and mayComplete):
                #re-enter last field
                return 0, partialEntry, None
        elif UI == None:
            if index < len(fields):
                #enter next field 
                return index, partialEntry, None
            elif mayComplete:
                #save entry, go to intro screen
                addEntry_saveEntry(fields, log, partialEntry)
                return 0, {}, None
            else:
                #loop around to first field
                return 0, partialEntry, None
            
def addEntry_saveEntry(fields, log, partialEntry):
    for field in fields:
        if (field.key() not in partialEntry) and field.default:
            partialEntry[field.key()] = field.default
    
    log.entry(partialEntry)
    
def addEntry_dataLoop_option(index, partialEntry, log,fields, breakScreen):
    optionsScreen = \
       ["Example Options Screen - Not yet dynamicallyt programmed                        ",
        "--------------------------------------------------------------------------------",
        "|##|H|Key               |Type      |*|Default    |Help                         |",
        "|03| |Acidity           |Range 0-10|*|           |0 for no acidity, 1 for just |",
        "|04| |Volume - in cm^3  |Float     |*|           |Make a guess...              |",
        "|05| |Time on loo - in m|Int       |*|           |From sit down to stand up.   |",
        "|06| |Time of visit     |Time Min  |*|           |Stand up time.               |",
        "|07| |Comments          |String    | |No comments|Any relavent info not caught |",
        "--------------------------------------------------------------------------------",
        "...idity|Digestion|Acidity|Volume - i|Time on lo|Time of visit      |Comments  |",
        "...     |?        |?      |?         |?         |?                  |?         |",
        "...     |9        |0      |200       |15        |2013-10-21 08:50:00|?         |",
        "...     |4        |0      |150       |10        |2013-10-22 09:05:00|Very dark |",
        "...     |10       |0      |150       |20        |?                  |?         |",
        "--------------------------------------------------------------------------------",
        "                                                                                ",
        "                                                                                ",
        "Not Yet Programmed. To select a field to enter type 'select' followed by the    ",
        "field number or followed by the beginning of the field key (i.e. 'select com'). ",
        "To change the focus of the tables, use 'focus' instead of 'select'. Type 'cont' ",
        "to continue, 'Restart' to start again, 'Cancel' to cancel this entry or 'Quit'  ",
        "to quit. Not yet programmed, type anything to continue.                         ",
        "--------------------------------------------------------------------------------"]
    for line in optionsScreen:
        print line
    print " $",
    UI = userInput()
    return index,partialEntry,breakScreen

def addEntry_goToOptions(index, fields, title):
    fieldKey = fields[index].key()
    
    content =  graphics.splitToWidth("To set '%s' for this entry, press enter leaving the input blank. To see alternate options enter 'Options'." % fieldKey)
    inst = ["",]*(18-len(content))
    graphics.drawWindow(title, content, inst, ["$ ",])
    while True:
        UI = userInput()
        if UI is None:
            return False
        elif isinstance(UI, str):
            if match(UI, "options"):
                return True
            
    
   
    

def addEntry_assessOptions (fields, index, partialEntry):
    # mayGoBack enables Back and Restart
    mayGoBack = (index >= 1)
    # How far may we navigate? The rule is: if field[N] is either set
    # or optional, we can go at least to N+1.
    i = 0
    max = len(fields)
    while i < max:
        field = fields[i]
        if field.optional or field.key() in partialEntry:
            i = i + 1
        else:
            break
    # selectLimit is maximum index to which we may navigate; if we
    # can't go anywhere it's zero.
    selectLimit = min (i, max-1)
    # mayComplete is True if every field is either set or optional.
    mayComplete = (i == max)
    #
    completed = mayComplete and (index == max-1)
    return (mayGoBack, selectLimit, mayComplete)


def addEntry_genInsts(index, fields, mayGoBack, selectLimit, mayComplete):
# if at i = i-max and all non-optional complete then "" for done and "loop" to loop round and set i = 0
    if index < len(fields) or not mayComplete:
        thisField = fields[index%len(fields)]
        thisInst = "To set '%s' for this entry, press enter leaving the input blank." % (thisField.key(),)
        doneInst = ["'Done' to save this entry"] if mayComplete else []
        loopInst = []
    else:
        thisInst = "This entry has been finished, press enter leaving the input blank to save it and start a new entry."
        doneInst = []
        loopInst = ["'Loop' to go back to the first field and continue editing this entry"]
        
    backInst = ["'Back' to reset '%s'" % (fields[index-1].key(),)] if mayGoBack else []
    selectInst = ["'Select' followed by a number below %d to reset a specific field" % (selectLimit+1,)] if selectLimit>0 else []
    restartInst = ["'Restart' to start again"] if mayGoBack else []
    optionInst = ["'Options' to see more options"]
    cancelInst = ["'Cancel' to give up"]
    quitInst = ["'Quit' to quit "]
    optionalInsts = loopInst + backInst + selectInst + restartInst + optionInst + cancelInst + doneInst + quitInst
    instCount = len(optionalInsts)
    if instCount>1:
        optionalInsts[instCount-1] = "or " + optionalInsts[instCount-1]
        optionalInsts = ", ".join(optionalInsts)
    else:
        optionalInsts = optionalInsts[0]
    return graphics.splitToWidth(thisInst + " Alternatively enter " + optionalInsts + ".")


    return (index, partialEntry)


def addEntry_augmentPartialEntry(partialEntry, field, index, log):
    "Returns (augmented) partialEntry"
    default = field.default
    key = field.key()
    titleStr = "Entering value for field '%s'." % (key,)
    helpStr = field.help
    datatype = field.datatype
    typeArgs = field.typeArgs
    choicePath = []
    choiceOptions = typeArgs

    if datatype in ("String", "Float"):
        typeString = datatype.lower()
    elif datatype == "Int":
        typeString = "integer"
    elif datatype == "Range":
        typeString = "integer from %d to %d" % (typeArgs[0],  typeArgs[1])
    elif datatype == "Time":
        accuracy = field.typeArgs[0]
        (formats, examples) = main.time_strings(accuracy)
        example_string = ', or '.join(examples)
        typeString = "date/time to the nearest %s, such as %s, or the string 'now'" % (accuracy.lower(), example_string,)
    elif datatype == "Choice":
        typeString = "integer correpsonding to your choice"
    else:
        complain ("Type was %s?" % (datatype,))

    while True:
        instStr = "Enter value - %s - for field '%s'; invalid values will be ignored." % (typeString, key)
        if key in partialEntry:
            instStr = instStr + " Alternatively, press enter leaving the input blank to reuse the current value."
        elif field.optional:
            instStr = instStr + " Alternatively, press enter leaving the input blank to use the default value."
 
        if datatype == "Choice":
            optionStrs = []
            for i in range(len(choiceOptions)):
                optionStrs += ["%d. %s" % (i+1, choiceOptions[i][0])]
            instStr = instStr + " " + ", ".join(optionStrs) + ". " + helpStr
        else:
            instStr = instStr

        title = [graphics.cutTo(titleStr),]
        dataTable = graphics.drawRecentData(leaf=log ,maxHeight=5, priorityCol=index, unfinishedEntry=partialEntry)
        miniCurr = graphics.miniDrawField(field, log, partialEntry, "current")

        instructions = graphics.splitToWidth(instStr)
        fieldHelp = graphics.splitToWidth(helpStr)

        width = graphics.WINDOW_WIDTH
        blankLine =  [(width*" "),]
        breakLine =  [(width*"-"),]

        topHalf = title + breakLine + \
                  dataTable + breakLine + \
                  miniCurr + breakLine + \
                  fieldHelp
        
        bottomHalf = breakLine + instructions + \
                     breakLine
        
        window = topHalf + \
                 (24 - len(topHalf) - len(bottomHalf))* blankLine + \
                 bottomHalf
        for line in window:
            print line
        print "$ ",
        
        UI = userInput()

        if datatype == "Time":
            if isinstance(UI, str) and UI.lower() == "now":
                value = main.now()
            else:
                value = main.parse_time(UI, formats)
        elif datatype == "Choice":
            try:
                which =int(UI) -1
            except:
                pass
            value = None
            if which in range(len(choiceOptions)):
                choicePath += [str(choiceOptions[which][0])]
                what = choiceOptions[which][1]
                if isinstance(what, str) or isinstance(what, unicode):
                    value = "~/" + "/".join(choicePath)
                elif not UI is None:
                    choiceOptions = what
        else:
            value = UI


        if main.validFieldEntry(value, datatype, typeArgs):
            partialEntry[field.key()] = value
            return partialEntry
        elif value is None and field.optional:
            partialEntry[field.key()] = field.default
            return partialEntry


def enterData_choice(field):
    default = field.default
    if main.validDatatype(field.datatype,field.typeArgs):
        default = choiceListEditor(field.typeArgs,True,"Picking default value for field '%s' - selecting choice - ")

        if main.validFieldEntry(default,field.datatype,field.typeArgs):
            field.default = default


    else:
        editField_drawAndUI("!!! ERROR setting default value for field '%s', invalid datatype." %(field.key(),),
                             "!!! Either the datatype or the associated type args are not valid, you cannot set a default until this has been fixed.",
                             fieldTable)


## views fields,entries, "" to cont
### 24 - 2 title - 2 prompt, 2 lines seperating tables/inst = 20. Fields: plus table, Data: plus table, instructions 3



## entries, field, data entry

## entries, options (i.e. go back one field, restart, quit)

## When out of fields, entries, options (save and quit, save and new, don't save and quit, don't save and new)



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
            if match(UI, "branch"):
                newLogName = askConfirmString("NameNewLogBranch")
                if newLogName != None:
                    state.currentL.branch(newLogName)
                graphics.drawPickLog("AddNewLog",state)
            elif match(UI, "leaf"):
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
        # Navigate to a leaf.
        if not isinstance(state.currentL, main.Leaf):
            if state.currentL == None:
                state.currentL = state.logs
            graphics.drawPickLog("EditLog",state)
            UI = userInput()
            if isinstance(UI,int):
                if UI-1 < len(state.currentL.children()):
                    state.currentL = state.currentL.children()[UI-1]
                # Hack to take us up one level.
                elif UI-1 == len(state.currentL.children()):
                    state.currentL = state.currentL.parent()
                    if state.currentL == None:
                        # We went up so many levels we have to stop now.
                        state.currentL = state.logs
                        return 0
        else:
            # We're on a leaf. Loop (NDL 2013-07-14 -- is this correct?) picking
            # fields and editing them.
            while True:
                content = graphics.TableOfFields(state.currentL)
                instructions = graphics.splitToWidth(
                    "Pick a current field by entering its number, start a new field by "
                    "entering 'N' or 'new' or press enter 'B' or 'Back' to stop editing fields."
                    )
                graphics.drawWindow([ "Fields for " + state.currentL.key()], content, instructions, ["$"])
                UI = userInput()
                if isinstance(UI, int):
                    if UI >= 0 and UI < len(state.currentL.fields()):
                        # Edit numbered field.
                        fieldToEdit = state.currentL.fields()[UI]
                        editField(fieldToEdit, state.currentL)
                elif isinstance(UI, str):
                    if match(UI, "back"):
                        return 0
                    elif match(UI, "new"):
                        # Edit new (empty) field.
                        editField(None, state.currentL)


def editField(oldField, leaf):
    typesWithData = ["Range", "Time", "Choice"]

    if oldField is None:
        newField = main.Field.empty(leaf)
    else:
        newField = oldField.copy()

    slotToEdit = "help"

    while True:
        slotToEdit, fieldTable = editField_pickSlot(slotToEdit, oldField, newField, leaf, typesWithData)
        if isinstance(slotToEdit, int):
            if slotToEdit == 0:
                # Save newField
                # This should only happen if the field is completely valid!
                # Also, won't this delete all the old data?!
                if main.validField(newField):

                    if oldField:
                        oldField.remove()
                    newField.move(leaf = leaf)

                    return slotToEdit
                else:
                    if yesOrNo("The field %s cannot be saved in its current state, would you still "
                               "like to quit (and lose any changes you've made)?" % (newField.key(),)):
                        return slotToEdit
            else:
                return slotToEdit

        slotFunctionDict = {
            "key"       :editField_setKey,
            "datatype"  :editField_setDatatype,
            "type data" :editField_setTypeArgs,
            "hidden"    :editField_setHidden,
            "optional"  :editField_setOptional,
            "default"   :editField_setDefault,
            "help"      :editField_setHelp}


        if slotToEdit in slotFunctionDict:
            slotFunctionDict[slotToEdit](newField,fieldTable)

    graphics.drawNotYetProgrammed()
    userInput()
    return 0



def editField_pickSlot(slotToEdit, oldField, newField, leaf, typesWithData):
    "Return a string, or an int meaning a quit."
    originalSlotToEdit = slotToEdit
    i = 0

    while True:
        slotToEdit = editField_pickSlot_default(slotToEdit, newField, typesWithData)

        inst_str_whatNext = "Either pick an option or press enter with the input blank to edit %s next." % (slotToEdit,)
        inst_whatNext = graphics.splitToWidth(inst_str_whatNext)

        shift = [0,0]
        inst_whatNext = editField_pickSlot_constructOptions(inst_whatNext, newField, shift, typesWithData)

        fieldsTable = graphics.TableOfFields(leaf, graphics.WINDOW_WIDTH, oldField)
        currentSlots = (newField.key(), newField.datatype, newField.typeArgs,newField.default,
                        newField.optional,  newField.help, newField.hidden)
        fieldTable = graphics.drawField(None, currentSlots)

        # NDL 2013-07-14 -- this value isn't actually used
        # fullContent = fieldsTable + ["-" * graphics.WINDOW_WIDTH] + fieldTable

        maxLenFieldsTable = graphics.WINDOW_HEIGHT - len(inst_whatNext) - len(fieldTable) - 6
        if maxLenFieldsTable > 1:
            fullContent = fieldsTable[:maxLenFieldsTable] + ["-" * graphics.WINDOW_WIDTH] + fieldTable
        else:
            fullContent = fieldTable

        graphics.drawWindow(["Editing field '%s'" %(newField.key(),)], fullContent, inst_whatNext, ["$ "])

        slotToEdit = editField_pickSlot_askUser(shift, slotToEdit)

        if slotToEdit is not None:
            return slotToEdit, fieldTable
        else:
            slotToEdit = originalSlotToEdit

def editField_pickSlot_default(slotToEdit, field, typesWithData):
    # Part one: working from the top, check whether anything has been left unset.
    if field.key() is None:
        return "key"
    elif field.datatype is None:
        return "datatype"
    elif field.datatype in typesWithData and field.typeArgs is None:
        return "type data"
    elif field.hidden is None:
        return "hidden"
    elif field.optional is None:
        return "optional"
    elif field.optional == True and field.default is None:
        return "default"
    elif field.help is None:
        return "help"
    else:
        # Part two: next editable item after the last slotToEdit
        thingsToEdit = ["key", "datatype", "type data", "hidden", "optional", "default", "help"]
        if slotToEdit in thingsToEdit:
            i = thingsToEdit.index(slotToEdit)
            i = (i+1)%(len(thingsToEdit))
            slotToEdit = thingsToEdit[i]
            if slotToEdit == "type data" and field.datatype not in typesWithData:
                slotToEdit = "hidden"
            if slotToEdit == "default" and field.optional is False:
                slotToEdit = "help"
        return slotToEdit

def editField_pickSlot_constructOptions(inst_whatNext, field, shift, typesWithData):
    inst_whatNext += [graphics.cutTo(str(1) + ". Key")]
    inst_whatNext += [graphics.cutTo(str(2) + ". Datatype")]
    if field.datatype in typesWithData:
        shift[0]= 1
        inst_whatNext += [graphics.cutTo(str(3) + ". Type data")]
    inst_whatNext += [graphics.cutTo(str(3 + shift[0]) + ". Hidden")]
    inst_whatNext += [graphics.cutTo(str(4 + shift[0]) + ". Optional")]
    if field.optional == True:
        shift[1] = 1
        inst_whatNext += [graphics.cutTo(str(5+ shift[0]) + ". Default")]
    inst_whatNext += [graphics.cutTo(str(5 + shift[0] +shift[1]) + ". Help")]
    inst_whatNext += [graphics.cutTo("Alternatively, enter 'Done' to save and quit or 'Cancel' to quit without saving.")]
    return inst_whatNext

def editField_pickSlot_askUser(shift, default):
    "Return a string, or None meaning try again, or an int meaning a quit."
    UI = userInput()
    if isinstance(UI, str):
        if UI.lower() in ["done", "d"]:
            return 0
        if UI.lower() in ["cancel", "c"]:
            return -1
    elif isinstance(UI, int):
        if UI > 0 and UI <= (6 + shift[0] + shift[1]):
            if shift == [0,0]:
                return ["key", "datatype", "hidden", "optional", "help"][UI-1]
            elif shift == [1, 0]:
                return ["key", "datatype", "type data", "hidden", "optional", "help"][UI-1]
            elif shift == [0, 1]:
                return ["key", "datatype", "hidden", "optional", "default", "help"][UI-1]
            elif shift == [1, 1]:
                return ["key", "datatype", "type data", "hidden", "optional", "default", "help"][UI-1]
            else:
                # NDL 2013-07-14 -- Surely an error?
                pass
    elif UI == None:
        return default
    else:
        return None
# current -> newField
# field   -> oldField



# FIELD SLOT SETTERS

def editField_drawAndUI(titleStr, instStr, fieldTable):
    fullInst = graphics.splitToWidth(instStr)
    maxLenFieldTable = graphics.WINDOW_HEIGHT - len(fullInst) - 5
    fullContent = fieldTable[:maxLenFieldTable]
    title = graphics.splitToWidth(titleStr)
    graphics.drawWindow(title, fullContent, fullInst, ["$"])
    return userInput()

def editField_drawAndUI_optionList(title, head, choices, tail, fieldTable):
    inst = ['%s\n' % (head,)] if head else []
    for i in range(len(choices)):
        inst.append(graphics.cutTo((str(i+1) + ". " + choices[i])))
    inst = inst + [tail] if tail else inst
    UI = editField_drawAndUI(title, ''.join(inst), fieldTable)
    return UI

def editField_setKey(field, fieldTable):
    key = field.key()
    while True:
        UI = editField_drawAndUI("Editing key for field '%s'" %(key,),
                             "Enter new key, or press enter leaving the input blank to leave the key as it was.",
                             fieldTable)
        if isinstance(UI, str):
            key = UI
            break
        elif UI == None:
            if key == None:
                if editField_confirmLeaveBlank('key'):
                    break
            else:
                # This should leave key as it was, as per instructions given above.
                break
    if key:
        field._key = key

def editField_setDatatype(field, fieldTable):
    typeList = ["String", "Int", "Float", "Range", "Choice", "Time"]

    datatype = field.datatype
    typeArgs = field.typeArgs
    default = field.default
    while True:
        UI = editField_drawAndUI_optionList("Picking datatype for field '%s'" % (field.key(),),
                    "Choose from the following options for datatype:",
                    typeList,
                    "Alternatively press enter leaving the input blank to leave datatype as it was.",
                    fieldTable)

        if isinstance(UI, int):
            if UI > 0 and UI <= len(typeList):
                if typeList[UI-1] != datatype:
                    datatype = typeList[UI-1]
                    typeArgs = None
                    default = None
                break
        elif UI == None:
            if datatype == None:
                if editField_confirmLeaveBlank('datatype'):
                    break
            else:
                break
    field.datatype = datatype
    field.typeArgs = typeArgs
    field.default = default


def editField_setTypeArgs(field, fieldTable):
    datatype = field.datatype
    if datatype == "Range":
        editField_setTypeArgs_range(field, fieldTable)
    elif datatype == "Choice":
        editField_setTypeArgs_choice(field, fieldTable)
    elif datatype == "Time":
        editField_setTypeArgs_time(field, fieldTable)
    else:
        # Shouldn't get here
        main.complain("%s has no type data" %(datatype,))

    if not main.validFieldEntry(field.default,datatype,field.typeArgs):
        field.default = None

def editField_setTypeArgs_range(field, fieldTable):
    def requestExtremum(which):
        return editField_drawAndUI("Setting %s for field '%s'" % (which, field.key(),),
                               "Enter the %s value for the range or press enter leaving the input blank to leave it as is." % (which,),
                               fieldTable)

    typeArgs = field.typeArgs
    if typeArgs == None:
        rMin = "?"
        rMax = "?"
    else:
        rMin, rMax = typeArgs

    cont = "min"
    while True:
        if cont == "min":
            UI = requestExtremum('minimum')
            if isinstance(UI, int):
                rMin = UI
                if isinstance(rMax, int):
                    typeArgs = [rMin,rMax]
                else:
                    typeArgs = [rMin,"?"]
                cont = "max"
            elif UI is None:
                cont = "max"
        if cont == "max":
            UI = requestExtremum('maximum')
            if isinstance(UI, int):
                rMax = UI
                if isinstance(rMin, int):
                    typeArgs = [rMin,rMax]
                else:
                    typeArgs = ["?",rMax]

                if isinstance(rMin, int):
                    if rMin < rMax:
                        cont = "False"
                    else:
                        cont = "min"
                else:
                    cont = "min"
            elif UI is None:
                cont = "False"
        if cont == "False":
            if isinstance(rMin, int) and isinstance(rMax,int) and rMin < rMax:
                field.typeArgs = [rMin,rMax]
                break
            else:
                instStr = "The current values or min and max are invalid. Until this is fixed " + \
                          "you won't be able to enter data in this field. Enter 'min' to change " \
                          "min, 'max' to change max or leave the input blank to exit anyway."
                UI = editField_drawAndUI("Leave min and max for '%s' unedited?" %(field.key(),), instStr, fieldTable)

                if isinstance(UI, str):
                    if UI.lower() in ["min", "max"]:
                        cont = UI.lower()
                elif UI is None:
                    break

def editField_setTypeArgs_time(field, fieldTable):
    typeList = field.typeArgs
    if typeList:
        time = typeList[0]
    else:
        time = None
    possibles = ["Second","Minute","Hour","Day","Month","Year"]
    while True:
        UI = editField_drawAndUI_optionList("Setting time precision for field '%s'" % (field.key(),),
                    "Choose from the following options for time precision:",
                    possibles,
                    "Alternatively press enter leaving the input blank to leave precision as it was.",
                    fieldTable)
        if isinstance(UI, int):
            if UI > 0 and UI <= len(possibles):
                time = possibles[UI-1]
                break
        elif UI is null:
            return

    if time:
        field.typeArgs = [time]

def editField_setTypeArgs_choice(field,fieldTable):
    choice = main.Choice(field.typeArgs)
    if choice.choiceList == None:
        choice = main.Choice([])
    titlePreStr = "Editing field %s - editing choice list - " % (field.key(),)
    choiceListEditor(choice, False, titlePreStr)
    field.typeArgs = choice.choiceList

    # ML 2013-07-20 Working on choice navigation before continuing this.

def editField_setHidden(field,fieldTable):
    titleStr = "Setting hidden for field '%s'" % (field.key(),)
    instStr = "To set hidden as true, enter 't' or 'true', to set hidden as false enter 'f' or 'false'. Alternately, press enter leaving the input blank to leave hidden as is. Hidden fields are not visible entering logs, but past data is not lost and the field can be unhidden at any time."
    while True:
        UI =  editField_drawAndUI(titleStr, instStr, fieldTable)
        if isinstance(UI, str):
            if match(UI, 'true'):
                field.hidden = True
                break
            elif match(UI, 'false'):
                field.hidden = False
                break
        elif UI == None:
            break
    return 0


def editField_setOptional(field,fieldTable):
    titleStr = "Setting optional for field '%s'" % (field.key(),)
    instStr = "To set optional as true, enter 't' or 'true', to set optional as false enter 'f' or 'false'. Alternately, press enter leaving the input blank to leave optional as is. Optional fields have a default value which they are set to unless specified otherwise."
    while True:
        UI =  editField_drawAndUI(titleStr, instStr, fieldTable)
        if isinstance(UI, str):
            if match(UI, 'true'):
                field.optional = True
                break
            elif match(UI, 'false'):
                field.optional = False
                break
        elif UI == None:
            break
    return 0

def editField_setDefault(field,fieldTable):
    datatype = field.datatype

    datatypeDict = {
        "String": editField_setDefault_easy,
        "Int"   : editField_setDefault_easy,
        "Float" : editField_setDefault_easy,
        "Range" : editField_setDefault_easy,
        "Choice": editField_setDefault_choice,
        "Time"  : editField_setDefault_time}

    return datatypeDict[datatype](field,fieldTable)


def editField_setDefault_easy(field,fieldTable):
    default = field.default
    if main.validDatatype(field.datatype,field.typeArgs):
        while True:
            UI = editField_drawAndUI("Setting default value for field '%s'." %(field.key(),),
                             "Enter new default value, or press enter leaving the input blank to leave the default as is. Invalid values will be ignored.",
                             fieldTable)
            if main.validFieldEntry(UI, field.datatype,field.typeArgs):
                default = UI
                break
            elif UI == None:
                break

        if main.validFieldEntry(default, field.datatype,field.typeArgs):
            field.default = default
    else:
        editField_drawAndUI("!!! ERROR setting default value for field '%s', invalid datatype." %(field.key(),),
                             "!!! Either the datatype or the associated type args are not valid, you cannot set a default until this has been fixed.",
                             fieldTable)

def editField_setDefault_choice(field,fieldTable):
    default = field.default
    if main.validDatatype(field.datatype,field.typeArgs):
        default = choiceListEditor(field.typeArgs,True,"Picking default value for field '%s' - selecting choice - ")

        if main.validFieldEntry(default,field.datatype,field.typeArgs):
            field.default = default


    else:
        editField_drawAndUI("!!! ERROR setting default value for field '%s', invalid datatype." %(field.key(),),
                             "!!! Either the datatype or the associated type args are not valid, you cannot set a default until this has been fixed.",
                             fieldTable)

def editField_setDefault_time(field, fieldTable):
    accuracy = field.typeArgs[0]
    (formats, examples) = main.time_strings(accuracy)
    example_string = ', or '.join(examples)
    titleStr = "Setting default time for field '%s'" % (field.key(),)
    problem = None
    # NDL 2013-09-12 extra points for bothering about singular case (ie only one form)...
    instStr = "To set the detault time to the nearest %s, enter a string in one of the following forms: %s. " % (accuracy.lower(), example_string,) + \
              "Alternatively press enter leaving the input blank to leave the default as it was."
    while True:
        if problem:
            instStr_with_problem = problem + '\n' + instStr
        else:
            instStr_with_problem = instStr
        UI = editField_drawAndUI(titleStr, instStr_with_problem, fieldTable)
        if isinstance(UI, str):
            default = main.parse_time(UI, formats)
            if isinstance(default, str):
                # oops, try again?
                problem = '%s to nearest %s' % (default, accuracy.lower())
            else:
                field.default = default
                return
        elif UI == None:
            break
    return 0

def editField_setHelp(field,fieldTable):
    helpStr = field.help
    fieldTable = graphics.drawField(field,None,graphics.WINDOW_WIDTH, graphics.WINDOW_HEIGHT)
    while True:
        UI = editField_drawAndUI("Editing help for field '%s'" %(field.key(),),
                             "Enter new help string, or press enter leaving the input blank to leave the help string as is.",
                             fieldTable)
        if isinstance(UI, str):
            helpStr = UI
            break
        elif UI == None:
            if helpStr == None:
                if editField_confirmLeaveBlank('help'):
                    break
            else:
                # NDL 2013-07-15 -- This is not allowed.
                # Martin 2013-07-18 -- ?? Yes it is. This should leave key as it was, as per instructions given above.
                break
    if helpStr:
        field.help = helpStr



def editField_confirmLeaveBlank(what):
    return yesOrNo("Do you wish to leave the %s blank? If you do so you won't be able to save the field." % (what,))


def viewData(state):
    graphics.drawNotYetProgrammed()
    userInput()
    return 0

def quitProgram(state, alreadySure = False):
    if alreadySure or  yesOrNo("Are you sure you want to quit?"):
        state.logs.write("Logs.xml")
        nowStr = str(main.now().previous(days = 0))
        backUpStr = "backup/Logs_" + nowStr[:10]
        print backUpStr
        state.logs.write(backUpStr)
        return -2
    else:
        return 0


def askConfirmString(key, titleInsert = None):
    questionDict = {
        "NameNewLogBranch":[["Name new branch","","Type the name of the new branch, then press enter.","$"],
                      ["Confirm branch name","Confirm that you want the new branch to be named '%s'.","Enter 'Yes' or 'Y' to confirm, or 'No' or 'N' to enter something different. Alternatively, if you don't want to create a new branch, enter 'Quit' or 'Q'.","$"]],

        "NameNewLogLeaf":[["Name new leaf","","Type the name of the new leaf, then press enter.","$"],
                      ["Confirm leaf name","Confirm that you want the new leaf to be named '%s'.","Enter 'Yes' or 'Y' to confirm, or 'No' or 'N' to enter something different. Alternatively, if you don't want to create a new leaf, enter 'Quit' or 'Q'.","$"]],

        "NameNewChoice":[["Name new choice","","Type the name of the new choice, then press enter.","$"],
                      ["Confirm choice name","Confirm that you want the new choice to be named '%s'.","Enter 'Yes' or 'Y' to confirm, or 'No' or 'N' to enter something different. Alternatively, if you don't want to create a new choice, enter 'Quit' or 'Q'.","$"]],

        "NameNewChildChoice":[["Name new sub-choice of %s","","Type the name of the new choice, then press enter.","$"],
                      ["Confirm sub-choice name","Confirm that you want the new choice to be named '%s'.","Enter 'Yes' or 'Y' to confirm, or 'No' or 'N' to enter something different. Alternatively, if you don't want to rename the choice, enter 'Quit' or 'Q'.","$"]],

        "RenameChoice":[["Rename the choice %s","","Type the new name of the choice, then press enter.","$"],
                      ["Confirm rename name","Confirm that you want the choice to be named '%s'.","Enter 'Yes' or 'Y' to confirm, or 'No' or 'N' to enter something different. Alternatively, if you don't want to rename the choice, enter 'Quit' or 'Q'.","$"]],
        }


    askInfo, confirmInfo = questionDict[key]

    if titleInsert:
        if "%s" in askInfo[0]:
            askInfo[0] = askInfo[0] % (titleInsert,)
        if "%s" in confirmInfo[0]:
            confirmInfo[0] = confirmInfo[0] % (titleInsert,)


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
                if match(UI, "yes"):
                    return ans
                elif match(UI, "quit"):
                    return None
                elif match(UI, "no"):
                    progress = "ask"



"""
navigate choice will exist in two places:
- edit field, type args  - No arg selection, add choice "save & quit"
- add log entry - basically as below, arg selection only way out.


As there are just those two, probably the best solution is not to abstract much but to add some logic and different titles. First neaten it up though.


Okay, so should abstract the graphics.


Give title, the choice, list of Qs, instr



"""
# At no point have I dealt with the prospect of things that cannot be fit on the screen (i.e. a choice list that has 50 items on the first tier) This'll need to be fixed before too long.



def choiceListEditor(choice, pickChoice = True, titlePreStr = "Choice List Editor - "):
    """
   Title format:

Editing field _________ - editing choice list - ~/a/b

Adding to log _________ - selecting choice for field __________ - ~/a/b
    """

    if choice == None:
        choice = main.Choice([])


    possibleOptions = [
        "Back",
        "Add a choice to this list",
        "Add a sub-choice to one of the choices on this list",
        "Change the name of one of the choices on this list",
        "Delete one of the choices on this list, along with any sub-choices",
        "Add a sub-choice to %s",
        "Change the name of %s",
        "Delete %s, along with any sub-choices",
        "Finish editing choice list"]

    while True:

        currentOptions = [False,
                          False,
                          False,
                          False,
                          False,
                          False,
                          False,
                          False,
                          (not pickChoice)]

        listOfOptions = []
        """
draw and ask
interpret
do thing
        """
        print "!"
        print choice.choiceList
        print "!"

        if choice.choiceList == []:
            # Deal with empty choice list.

            # Set avaialble options, build graphics, and ask for UI

            currentOptions[1] = True

            for i in range(len(possibleOptions)):
                if currentOptions[i]:
                    listOfOptions.append(possibleOptions[i])

            titleStr = titlePreStr + choice.filePath()

            if pickChoice:
                instStr = "This choice list is currently empty, so your only option is to create a new choice."
            else:
                instStr = "This choice list is currently empty, so either create a new choice or quit editing."

            n, UI = choiceListEditor_drawAndUI(titleStr, choice, listOfOptions, instStr)

            # Respond to UI
            if isinstance(UI,int):
                if UI == 1:
                    newName = askConfirmString("NameNewChoice")
                    if newName:
                        choice.choiceList = [[newName,newName]]
                        choice.keyList = []
                        choice.updateCurrentList()
                if UI == 2 and not pickChoice:
                    break

        elif not isinstance(choice.currentChoiceList,list):


            # Set avaialble options, build graphics, and ask for UI
            currentOptions[0] = True
            currentOptions[5:8] = [True,]*3

            for i in range(len(possibleOptions)):
                if currentOptions[i]:
                    listOfOptions.append(possibleOptions[i])


            if pickChoice:
                instStr = "Press enter to confirm your selection of %s, or select from one of the options above." % (str(choice.currentChoiceList),)
                titleStr = titlePreStr + choice.filePath() + " - confirm selection"

            else:
                instStr = "Select from the options above."
                titleStr = titlePreStr + choice.filePath()


            n, UI = choiceListEditor_drawAndUI(titleStr, choice, listOfOptions, instStr)
            if n != 0:
                main.complain("huh")

            #Respond to UI
            if UI == None and pickChoice:
                print "Have picked %s" % (str(choice.currentChoiceList),)
                return choice.currentChoiceList
            elif isinstance(UI,int):
                if UI == 1:
                    choice.pickChoice(1)
                elif UI == 2:
                    newName = askConfirmString("NameNewChildChoice", choice.currentChoiceList)
                    if newName:
                        key = choice.keyList[-1]
                        choice.keyList.pop()
                        choice.updateCurrentList()
                        choice.currentChoiceList[key][1] = [[newName, newName]]
                        choice.pickChoice(key+1)
                elif UI == 3:
                    newName = askConfirmString("RenameChoice", choice.currentChoiceList)
                    if newName:
                        key = choice.keyList[-1]
                        choice.keyList.pop()
                        choice.updateCurrentList()
                        choice.currentChoiceList[key] = [newName, newName]
                        choice.pickChoice(key+1)
                elif UI == 4:
                    while True:
                        graphics.askYesNo("Are you sure you want to delete %s and all sub-choices?" %(choice.currentChoiceList,))
                        UI = userInput()
                        if isinstance(UI,str):
                            key = choice.keyList[-1]
                            choice.keyList.pop()
                            choice.updateCurrentList()
                            if UI.lower() in ["y","yes"]:
                                if len(choice.currentChoiceList) > 1:
                                    choice.currentChoiceList.pop(key)
                                elif len(choice.keyList) > 0:
                                    key = choice.keyList[-1]
                                    choice.keyList.pop()
                                    choice.updateCurrentList()
                                    choice.currentChoiceList[key][1] = choice.currentChoiceList[key][0]
                                    choice.pickChoice(key+1)

                                else:
                                    choice.choiceList = []
                                break
                            if UI.lower() in ["n","no"]:
                                break
                elif UI == 5 and not pickChoice:
                    break
        else:
             # Set avaialble options, build graphics, and ask for UI
            if len(choice.keyList)> 0:
                shift = 1
                currentOptions[0] = True
            else:
                shift = 0
            currentOptions[1:5] = [True,]*4

            for i in range(len(possibleOptions)):
                if currentOptions[i]:
                    listOfOptions.append(possibleOptions[i])

            titleStr = titlePreStr + choice.filePath()
            instStr = "Select from the options above."

            n, UI = choiceListEditor_drawAndUI(titleStr, choice, listOfOptions, instStr)

            #Respond to UI
            if isinstance(UI, int):
                if UI > 0 and UI < n + 1 + shift:
                    choice.pickChoice(UI)
                elif UI == n + 1 + shift:
                    newName = askConfirmString("NameNewChoice")
                    if newName:
                        choice.addChoice_sibling(newName,newName)
                elif UI == n + 2 + shift:
                    while True:
                        titleStr = titlePreStr + choice.filePath() + " - adding sub-choice"
                        instStr = "Select a choice to add a sub-choice to."
                        listOfOptions = ["Do not add a sub-choice",]

                        n, UI = choiceListEditor_drawAndUI(titleStr, choice, listOfOptions, instStr)

                        if isinstance(UI, int):
                            if UI > 0 and UI < n + 1:
                                key = UI
                                newName = askConfirmString("NameNewChildChoice", choice.currentChoiceList[UI-1][0])
                                if newName:
                                    choice.addChoice_child(key,newName,newName)
                                break
                            elif UI == n + 1:
                                break
                elif UI == n + 3 + shift:
                    while True:
                        titleStr = titlePreStr + choice.filePath() + " - renaming choice"
                        instStr = "Select a choice to rename."
                        listOfOptions = ["Do not rename a choice.",]

                        n, UI = choiceListEditor_drawAndUI(titleStr, choice, listOfOptions, instStr)

                        if isinstance(UI, int):
                            if UI > 0 and UI < n + 1:
                                key = UI
                                newName = askConfirmString("RenameChoice", choice.currentChoiceList[UI-1][0])
                                if newName:
                                    if isinstance(choice.currentChoiceList[UI-1][1], list):
                                        choice.changeName(UI, newName)
                                    else:
                                        choice.currentChoiceList[UI-1] = [newName, newName]
                                break
                            elif UI == n + 1:
                                break
                elif UI == n + 4 + shift:
                    while True:
                        titleStr = titlePreStr + choice.filePath() + " - deleting choice"
                        instStr = "Select a choice to delete."
                        listOfOptions = ["Do not delete a choice.",]

                        n, key = choiceListEditor_drawAndUI(titleStr, choice, listOfOptions, instStr)

                        if isinstance(key, int):
                            if key > 0 and key < n + 1:
                                while True:
                                    graphics.askYesNo("Are you sure you want to delete %s and all sub-choices?" %(choice.currentChoiceList[key-1][0],))
                                    UI = userInput()
                                    if isinstance(UI,str):
                                        if UI.lower() in ["y","yes"]:
                                            if len(choice.currentChoiceList) > 1:
                                                choice.currentChoiceList.pop(key-1)
                                            elif len(choice.keyList) > 0:
                                                key = choice.keyList[-1]
                                                choice.keyList.pop()
                                                choice.updateCurrentList()
                                                choice.currentChoiceList[key][1] = choice.currentChoiceList[key][0]
                                                choice.pickChoice(key+1)

                                            else:
                                                choice.choiceList = []
                                            break
                                        if UI.lower() in ["n","no"]:
                                            break
                                break
                            elif key == n + 1:
                                break
                elif UI == n + 5 + shift:

                    break



def choiceListEditor_drawAndUI(titleStr, choice, otherOptions, instStr):
    title = graphics.splitToWidth(titleStr)

    listOfOptions = []

    if choice.choiceList == []:
        n = 0
    elif isinstance(choice.currentChoiceList,list):
        n = len(choice.currentChoiceList)
        for i in range(n):
            listOfOptions.append(choice.currentChoiceList[i][0])
    else:
        n = 0

    listOfOptions += otherOptions

    content = []
    for i in range(len(listOfOptions)):
        optionStr = str(i+1) + ". " + str(listOfOptions[i])
        if "%s" in optionStr:
            optionStr = optionStr % (str(choice.currentChoiceList))
        content += graphics.splitToWidth(optionStr)


    inst = graphics.splitToWidth(instStr)

    graphics.drawWindow(title, content,inst,["$"])
    return n, userInput()







"""
def editField_drawAndUI(title, text, fieldTable):
    splitText = graphics.splitToWidth(text)
    maxLenFieldTable = graphics.WINDOW_HEIGHT - len(splitText) - 5
    fullContent = fieldTable[:maxLenFieldTable]
    graphics.drawWindow([title], fullContent, splitText, ["$"])
    return userInput()

def editField_drawAndUI_optionList(title, head, choices, tail, fieldTable):
    inst = ['%s\n' % (head,)] if head else []
    for i in range(len(choices)):
        inst.append(graphics.cutTo((str(i+1) + ". " + choices[i])))
    inst = inst + [tail] if tail else inst
    UI = editField_drawAndUI(title, ''.join(inst), fieldTable)
    return UI

"""




################################################################################
# RUN - ACTUAL                                                                 #
################################################################################





logs = main.read("Logs.xml")



# List of form [(name1, option),
#               (name2,[(name2a,option),(name2b,option)],
#               (name3,option)]

menu = main.Choice(
    [("Add new log entry", addEntry),                                    # not yet
     ("Add or edit a log template",
      [("Add log template", addNewLog),
       ("Edit log template",
        [("Edit template location within data structure", moveLog),      # not yet
         ("Edit fields of log", editLog)])]),
     ("View log data", viewData),                                        # not yet
     ("Quit", quitProgram)])



state = LoggerState(menu,logs)

mainMenu(state)



"""
Things that need doing before alpha:

save - need to have back-ups writes of most recent save of each day

Things that need doing at some point:

- Lists longer than one screen height need to be handled in some fashion.
  Probably with navigation between sets of around ten.
- Very long strings also need some kind of navigation to be viewed properly.
- Print out two lines of "-" after every UI entered and before each new screen.
  (To make it easier to seperate debug info from UI)



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




def addEntry_parseCommand(index, partialEntry, navOptions, title, content, inst):
    mayGoBack, selectLimit, mayComplete = navOptions
    while True:
        graphics.drawWindow(title, content, inst, ["$ ",])
        UI = userInput()
        if UI is None:
            break
        elif isinstance(UI, str):
            if mayGoBack and match(UI, "back"):
                index = index - 1
                break
            elif mayGoBack and match(UI, "restart"):
                if yesOrNo("Confirm: would you like to start this entry again?"):
                    partialEntry = {}
                    index = 0
                    break
            elif match(UI, "cancel"):
                if yesOrNo("Confirm: would you like to abandon this new entry?"):
                    return "cancel"
            elif mayComplete and match(UI, "done"):
                return "done"
            elif selectLimit>0:
                splut = UI.split()
                if len(splut) == 2 and match(splut[0], "select"):
                    try:
                        where = int(splut[1])
                        if where <= selectLimit:
                            index = where
                            break
                    except:
                        pass



"""



 
