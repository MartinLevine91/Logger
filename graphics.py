"""
STARTING SIMPLE

***CAN BUILD OPTION SCREEN***
==> Feed it list of options ["milk","cheese","yogurt","cream"], get content back
==> Feed it content, title (left part, length reducable right part),instructions, prompt




"""




import main
import json

WINDOW_HEIGHT = 24
WINDOW_WIDTH = 80

def superClear():
    for i in range(WINDOW_HEIGHT*4):
        print ""

def cutTo(string,length):
    if len(string) > length:
        string = string [:length]
    elif len(string) < length:
        string = string + " " *(length - len(string))
    return string

def drawWindow(title,content,instruction,prompt):
    """
    Draws a window from lists of title, content, instruction and userInput.
    Lines must not be more than maximum width and there must not be more than
    the maximum number of rows. Any empty space will be filled up though.
    """    
    sectionChar = "-"
    endSection = [(WINDOW_WIDTH * sectionChar),]
    newLine = [""]

    lineCount = len(title+content+instruction+prompt) + 3

    if lineCount > WINDOW_HEIGHT:
        print "rendering error! used too many rows"
        print "title       ", len(title)
        print "content     ", len(content)
        print "instruction ", len(instruction)
        print "userinput   ", len(prompt)
        print "divide lines", 3
        print "             ____"
        print "sum =       ", lineCount
        print
        print "max =", WINDOW_HEIGHT
        print error 
    else:
        output = title + endSection + \
                 content + (WINDOW_HEIGHT - lineCount)*newLine + endSection + \
                 instruction + endSection +\
                 prompt

        for i in range(WINDOW_HEIGHT):
            line = output[i]
            if len(line) > WINDOW_WIDTH:
                print "rendering error, line " + str(i) + "used too many cols"
                print "line in quesiton:"
                print endSection[0]
                print line
                print endSection[0]
                print error
            elif i != WINDOW_HEIGHT -1:
                fullLine = line + " "*(WINDOW_WIDTH-len(line))
                print fullLine
        print output[WINDOW_HEIGHT-1],



def splitAndDraw(titleStr,contentStr,instructionStr,promptStr,maxWidth = WINDOW_WIDTH):
    title = splitToWidth(titleStr, maxWidth)
    content = splitToWidth(contentStr, maxWidth)
    instruction = splitToWidth(instructionStr, maxWidth)
    prompt = splitToWidth(promptStr, maxWidth)

    drawWindow(title,content,instruction,prompt)

def drawMainMenu(menu):
    """
    Currently will fail if number of options exceeds maximum as determined
    by row limit
    """

#Draw the title:    
    Title_str = findChoiceTitle(menu,"Menu selection",WINDOW_WIDTH)
    title = [Title_str,]

#List the choices
    listOfChoices = menu.currentChoiceList
    content = []
    for i in range(len(listOfChoices)):
        content.append(str(i+1) + ". " + listOfChoices[i][0])

    if len(menu.keyList) > 0:
        content.append(str(len(listOfChoices)+1) + ". Back")
    
    instructions = ["Just pick an option from above.","And enter it below!"]
    prompt = ["Option:"]

    drawWindow(title,content,instructions,prompt)


def findChoiceTitle(choiceToSearchThrough,openingString,maxWidth):
    
    Title_str = ""
    titleFinder = choiceToSearchThrough.choiceList
    
    for i in range(len(choiceToSearchThrough.keyList)):
        Title_str = Title_str + titleFinder[choiceToSearchThrough.keyList[i]][0] +"/"
        titleFinder = titleFinder[choiceToSearchThrough.keyList[i]][1]



    maxChars =  maxWidth - len(openingString) - 4
    
    if len(Title_str) > maxChars:
        Title_str = openingString + ": .." + Title_str[-(maxChars-2):]
    else:
        Title_str = openingString + ": ~/" + Title_str

    
    return Title_str

def findNodeTitle(currentN,openingString,maxWidth):
    Title_str = "..."
    
    rootFinder = currentN
    while not isinstance(rootFinder, main.Root):
        Title_str = rootFinder.key() + "/" + Title_str
        rootFinder = rootFinder.parent()
        
    maxChars =  maxWidth - len(openingString + ": ~/")
    
    if len(Title_str) > maxChars:
        Title_str = openingString + ": .." + Title_str[-maxChars:]
    else:
        Title_str = openingString + ": ~/" + Title_str
    return Title_str

    
def drawNotYetProgrammed():
    title = ["Not yet programmed.",]
    content = ["",]
    instructionString = "This part of the program has not been completed yet, enter" + \
                        "any input to return to the part of the program that sent you here."
    instructions = splitToWidth(instructionString, WINDOW_WIDTH)
    prompt = ["Any input will do:",]
    drawWindow(title,content,instructions,prompt)

    
def splitToWidth(longStr,maxWidth = WINDOW_WIDTH):
    strList = []
    while len(longStr) > maxWidth:
        strList.append(longStr[:maxWidth])
        longStr = longStr[maxWidth:]
    strList.append(longStr)
    return strList


def askYesNo(question):
    title = [question,]
    content = ["",]
    instructionString = "Answer the question in the title, with a 'Yes' or 'Y' for yes" + \
                         " and a 'No' or 'N' for no. Capitilsation doesn't matter and " + \
                         "all invalid answers will be ignored."
    instructions = splitToWidth(instructionString, WINDOW_WIDTH)
    prompt = ["Y or N: "]
    drawWindow(title,content,instructions,prompt)

def drawNodeSelection(currentN, maxWidth, titleString,extraOptions,instructionString,prompt):

    """
    Currently will fail if number of options exceeds maximum as determined
    by row limit
    """
    

    currentMenuOption = currentN
        
    title = [titleString,]
    
    listOfChildren = currentMenuOption.children()
    content = []
    numKids = len(listOfChildren)
    for i in range(numKids):
        content.append(str(i+1) + ". " + listOfChildren[i].key())


    for i in range(len(extraOptions)):  
        content.append(str(numKids + i + 1) +". " + extraOptions[i])
    

    content.append(str(numKids + len(extraOptions)+1) + ". Back")
    
    instructions = splitToWidth(instructionString, maxWidth)

    
    drawWindow(title,content,instructions,[prompt,])

def drawPickLog(key,state):
# Key if for a dictionary in this function which contains all the data for drawing
# the graphics for the function that called with the key, that informaiton should 
# include:
# * max Width
# * title openingString
# * a list of extra options i.e. ["Add branch here.","Add leaf here."]
# * instructions
# * prompt
    logInfoDict = {
        "AddNewLog":[WINDOW_WIDTH,"Placing new log",[], "Select the location for your new log template, navigate the Node structure until you're ready to add either a branch or a leaf. Enter 'branch' or 'leaf' to add a node to the tree.","$ "],
        "AddNewLog_noLeaves":[WINDOW_WIDTH,"Placing new log",[], "Select the location for your new log template, navigate the Node structure until you're ready to add either a branch or a leaf. Enter 'branch' or 'leaf' to add a node to the tree. Oops, you just selected a leaf, you cannot attach new branches or leaves to existing leaves.","$ "],
        "EditLog":[WINDOW_WIDTH,"Selecting log to edit",[], "Navigate the Node structure and select the log template you would like to edit.","$ "],


        }
    
    maxWidth,openingTitleString,extraOptions,instructionString,prompt = logInfoDict[key]

    titleString = findNodeTitle(state.currentL,openingTitleString,maxWidth)

    drawNodeSelection(state.currentL, maxWidth,titleString,extraOptions,instructionString,prompt)

    
def TableOfFields(leaf,maxWidth =WINDOW_WIDTH):
    """

         1         2         3         4         5         6         7         8
12345678901234567890123456789012345678901234567890123456789012345678901234567890
|##|H|Key            |Type      |*|Default       |Help                         |
                      Range 0-10 
                      Time Min
                      Time Hour
                      Time Day
                      Time Mon
                      Time Year
                      Choices... 
                      
Min and default widths for variable width fields:


Key: 3, 15
Type: 4, 10
Other: 4+8
Default: 7, 14
help: 4, 29


Min = 48
default = 80

Go through Keys, Types, Defaults and Helps finding maxWidth. If maxWidth is more
than allowed width for that column, then truncate to maxWidth, if it is less,
distribute the extra width.


Will break if there isn't room for K,T,O at default, D,H at min.



    """
    if not isinstance(leaf,main.Leaf):
        main.complain("Can't make a table of fields unless you feed TableOfFields a leaf")

    if maxWidth < 48:
        main.complain("TableOfFields requires a minimum width of 48 chars to run in all cases")


    fields = leaf.fields()
    print "Fields", type(fields), fields
    
    fullWidthTable = []

    for field in fields:
        if field.hidden:
            hidden = "H"
        else:
            hidden = " "
        
        key = field.key()
        
        dataTypeLst =  json.loads(field.datatype)

        if dataTypeLst[0] in ["String","Int","Float","Choice"]:
            dataType = dataTypeLst[0]
        elif dataTypeLst[0] == "Range":
            rng = str(dataTypeLst[1][0]) + "-" + str(dataTypeLst[1][1])
            if len(rng) < 5:
                dataType = "Range " + rng
            else:
                dataType = "Rng " + rng
        elif dataTypeLst[0] == "Time":
            dataType = "Time " + {"Minute":"Min","Hour":"Hour","Day":"Day","Month":"Mon","Year":"Year"}[dataTypeLst[1]]
        else:
            main.complain("datatype processing error, Table of fields")

        optional = field.optional
        print optional
        if optional:
            optional = "*"
        else:
            optional = " "

        default = field.default
        if default == None:
            default = ""
        
        fieldHelp = field.help
        if fieldHelp == None:
            fieldHelp = ""
        longRow = [hidden,key,dataType,optional,default,fieldHelp]
        fullWidthTable.append(longRow)
    """
Finding col widths...

M = max
m = min
D = default

#+ >= #

K,T,D,H = M,M,M,M
K,T,D,H = M,M,D+,D+
K,T,D,H = D+,M,D,D
K,T,D,H = D,M,m+,m+
K,T,D,H = D,D+,m,m
K,T,D,H = D,D,m,m


find, m, M, D for K,T,D,H
set m < D,M  (this is done through starting vals for maxLen
set M >= D, lower D to M otherwise

>= M,M,M,M = M,M,M,M
elif >= M,M,D,D = M,M,D+,D+
>=

    """
    minLenKey = 3
    minLenType = 4
    minLenDef = 7
    minLenHelp = 4

    defLenKey = 15
    defLenType = 10
    defLenDef = 14
    defLenHelp = 29

    maxLenKey = minLenKey
    maxLenType = minLenType
    maxLenDef = minLenDef
    maxLenHelp = minLenHelp
    
    for longRow in fullWidthTable:
        maxLenKey = max(maxLenKey, len(longRow[1]))
        maxLenType = max(maxLenType, len(longRow[2]))                        
        maxLenDef = max(maxLenDef, len(longRow[4]))
        maxLenHelp = max(maxLenHelp, len(longRow[5]))

    defLenKey = min(defLenKey,maxLenKey)
    defLenType = min(defLenType,maxLenType)
    defLenDef = min(defLenDef,maxLenDef)
    defLenHelp = min(defLenHelp,defLenHelp)

    # K,T,D,H = M,M,M,M
    if maxWidth >= (maxLenKey + maxLenType + maxLenDef + maxLenHelp + 12):
        keyLen = maxLenKey
        typeLen = maxLenType
        defLen = maxLenDef
        helpLen = maxLenHelp

    # K,T,D,H = M,M,D+,D+
    elif maxWidth >= (maxLenKey + maxLenType + defLenDef + defLenHelp + 12):
        keyLen = maxLenKey
        typeLen = maxLenType
        spareLen = maxWidth - 12 -keyLen - typeLen
        defLen = spareLen/3
        helpLen = spareLen - defLen
        if defLen > maxLenDef:
            defLen = maxLenDef
            helpLen = spareLen - defLen
        elif helpLen > maxLenHelp:
            helpLen = maxLenHelp
            defLen = spareLen - helpLen

    # K,T,D,H = D+,M,D,D
    elif maxWidth >= (defLenKey + maxLenType + defLenDef + defLenHelp + 12):
        typeLen = maxLenType
        defLen = defLenDef
        helpLen = defHelpLen
        keyLen = maxWidth - typeLen - defLen - helpLen - 12

    # K,T,D,H = D,M,m+,m+
    elif maxWidth >= (defLenKey + maxLenType + minLenDef + minLenHelp + 12):
        keyLen = defLenKey
        typeLen = maxLenType
        spareLen = maxWidth - 12 -keyLen - typeLen

        if spareLen/3 < minLenDef:
            defLen = minLenDef
            helpLen = spareLen - defLen
        else:
            defLen = spareLen/3
            helpLen = spareLen-defLen

    # K,T,D,H = D,D+,m,m
    elif maxWidth >= (defLenKey + defLenType + minLenDef + minLenHelp + 12):
        keyLen = defLenKey
        helpLen = minLenHelp
        defLen = minLenDef
        typeLen = maxWidth - keyLen - helpLen - defLen - 12

    #cut columns to width and form table with each row as a string

    titleRow = "|##|H|%s|%s|*|%s|%s|" % (cutTo("Key",keyLen),cutTo("Type",typeLen), \
                                        cutTo("Default",defLen),cutTo("Help",helpLen))

    fieldTable = []
    fieldTable.append(titleRow)
    for i in range(len(fullWidthTable)):
        #longRow = [hidden,key,dataType,optional,default,fieldHelp]
        #|##|H|Key            |Type      |*|Default       |Help     |
        longRow = fullWidthTable[i]
        
        rowStr = "|"
        
        i_str = str(i)
        if len(i_str) == 1:
            i_str = "0" + i_str

        # Field number        
        rowStr += i_str + "|"
        # Hidden?
        rowStr += longRow[0] + "|"
        # Key
        rowStr += cutTo(longRow[1],keyLen) + "|"
        # Type
        rowStr += cutTo(longRow[2],typeLen) + "|"
        # Optional
        rowStr += longRow[3] + "|"
        # Default
        rowStr += cutTo(longRow[4],defLen) + "|"
        # Help 
        rowStr += cutTo(longRow[5],helpLen) + "|"

        fieldTable.append(rowStr)
    
    return fieldTable
        

