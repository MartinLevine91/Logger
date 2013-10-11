# -*- coding: utf-8 -*-
"""
STARTING SIMPLE

***CAN BUILD OPTION SCREEN***
==> Feed it list of options ["milk","cheese","yogurt","cream"], get content back
==> Feed it content, title (left part, length reducable right part),instructions, prompt


"""



import main

WINDOW_HEIGHT = 24
WINDOW_WIDTH = 80

def superClear():
    for i in range(WINDOW_HEIGHT*4):
        print ""

def cutTo(string, length = WINDOW_WIDTH):
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
                 instruction + endSection + prompt

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
    prompt = [promptStr,]

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
    instructionString = "This part of the program has not been completed yet, enter " + \
                        "any input to return to the part of the program that sent you here."
    instructions = splitToWidth(instructionString)
    prompt = ["Any input will do:",]
    drawWindow(title,content,instructions,prompt)


def splitToWidth(longStr, maxWidth = WINDOW_WIDTH):
    def splitOne(line):
        strList = []
        while len(line) > maxWidth:
            if line[0] == ' ':
                line = line[1:]
            else:
                splitAt = maxWidth
                while 0 < splitAt and splitAt > maxWidth - 10 and not line[splitAt]==' ':
                    splitAt = splitAt - 1
                newStr = line[:splitAt]
                strList.append(newStr + " " * (maxWidth-len(newStr)))
                line = line[splitAt:]
        while len(line) > 0 and line[0] == ' ':
            line = line[1:]
        if len(line) > 0:
            strList.append(line + " " * (maxWidth-len(line)))
        return strList
    return sum(map(splitOne, longStr.splitlines()), [])


def askYesNo(question):
    title = splitToWidth(question,WINDOW_WIDTH)
    content = ["",]
    instructionString = "Answer the question in the title, with a 'Yes' or 'Y' for yes " + \
                        "and a 'No' or 'N' for no. Capitilsation doesn't matter and "   + \
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
        "AddEntry":[WINDOW_WIDTH,"Selecting log to add entries to",[], "Navigate the Node structure and select the log you would like to add to.","$ "],


        }

    maxWidth,openingTitleString,extraOptions,instructionString,prompt = logInfoDict[key]

    titleString = findNodeTitle(state.currentL,openingTitleString,maxWidth)

    drawNodeSelection(state.currentL, maxWidth,titleString,extraOptions,instructionString,prompt)


def TableOfFields(leaf, maxWidth = WINDOW_WIDTH, fieldBeingEdited = None):
    """

         1         2         3         4         5         6         7         8
12345678901234567890123456789012345678901234567890123456789012345678901234567890
|##|H|Key            |Type      |*|Default       |Help                         |
                      Range 0-10| |
                      Time Min  |
                      Time Hour |
                      Time Day  |
                      Time Mon  |
                      Time Year |
                      Choices...|

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
        if field.hidden == True:
            hidden = "H"
        elif field.hidden == "?":
            hidden = "?"
        else:
            hidden = " "

        print "field: ", field
        key = field.key()
        print "key: ", key

        dataType = field.datatype
        typeArgs = field.typeArgs

        try:
            if dataType == "Range":
                rng = str(typeArgs[0]) + "-" + str(typeArgs[1])
                if len(rng) < 5:
                    dataType = "Range " + rng
                else:
                    dataType = "Rng " + rng

            elif dataType == "Time":
                print "TIME"
                print typeArgs
                print "TIME"
                dataType = "Time " + {"Minute":"Min", "Hour":"Hour", "Day":"Day", "Month":"Mon", "Year":"Year"}[typeArgs[0]]
        except:
            dataType = "?" + dataType

        default = field.default
        if default == None:
            default = ""

        optional = field.optional

        if not optional:
            optional = "*"
            default = ""
        else:
            if optional == True:
                optional = " "
            else:
                optional = "?"

        fieldHelp = field.help
        if fieldHelp == None:
            fieldHelp = ""
        longRow = [hidden,key,dataType,optional,str(default),fieldHelp]
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
        helpLen = defLenHelp
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

# NDL 2013-07-14 -- currently only one caller to drawField, and it hardwires field to None
def drawField(field, fieldAsTable = None, maxWidth = WINDOW_WIDTH,maxHeight = 8):
    """
Draws a field in 8 lines (or more)
1   Key:
2   Type:
3   Type data:
4   Hidden:     Optional:
5   Default:
6   Help:
7
8
key,datatype,hidden,optional,help
    """
    if field != None:
        key = field.key()
        datatype = field.datatype
        typeArgs = field.typeArgs
        hidden = field.hidden
        optional = field.optional
        default = field.default
        helpStr= field.help
    else:
        key,datatype,typeArgs,default,optional,helpStr,hidden = fieldAsTable

    if key == None:
        key = "..."
    if datatype == None:
        datatype = "..."
        typeArgs = "..."
    if helpStr == None:
        helpStr = "..."
    if default == None:
        default = "..."

    firstHalf = maxWidth/2
    secondHalf = maxWidth - firstHalf

    fieldList = []
    fieldList += splitToWidth("Key: " + key, maxWidth)

    fieldList += splitToWidth("Type: " + datatype, maxWidth)

    if datatype not in ['Range','Choice','Time']:
        fieldList += splitToWidth("No type data.",maxWidth)

    elif datatype == 'Range':
        if typeArgs in[None, []]:
            typeArgs = ["?", "?"]

        typeDataStr = cutTo("Min: " + str(typeArgs[0]),firstHalf) + \
                      cutTo("Max: " + str(typeArgs[1]),secondHalf)
        fieldList.append(typeDataStr)
    elif datatype == 'Choice':
        choices = main.Choice(typeArgs)
        typeDataStr = "Choices: " + str(choices.setOfAllChoices())[len("set(["):-len('])')]
        if len(typeDataStr) > maxWidth:
            typeDataStr = typeDataStr[:maxWidth-4] + "'..."
        fieldList.append(typeDataStr)
    elif datatype == 'Time':
        if typeArgs == ["?",]:
            fieldList += splitToWidth("Accurate to the nearest: " + typeArgs[0])

    if hidden == True:
        hStr = "T"
    elif hidden == False:
        hStr = "F"
    elif hidden == None:
        hStr = "?"
    else:
        print "!!!!!!!!"
        print hidden
        print "!!!!!!!!"
        main.complain("invalid value for hidden")

    if optional == True:
        oStr = "T"
    elif optional == False:
        oStr = "F"
    elif optional == None:
        oStr = "?"

    HO_str = cutTo("Hidden: " + hStr,firstHalf ) + cutTo(" Optional: " + oStr,secondHalf)
    fieldList.append(HO_str)

    if optional:
        fieldList += splitToWidth("Default: " + str(default))

    helpList = ["Help: "] + splitToWidth('"' + helpStr, maxWidth)

    fieldList += helpList
    fieldList = fieldList[:maxHeight]
    fieldList[-1] = fieldList[-1][:-1] + '"'

    return fieldList


def drawRecentData(leaf, priorityCol = None,unfinishedEntry = None, maxHeight = WINDOW_HEIGHT, maxWidth= WINDOW_WIDTH, drawHidden = False, drawDeleted = False):

    # Get field list

    data = leaf.entries()
    if isinstance(unfinishedEntry,dict):
        data.append(unfinishedEntry)

    if drawDeleted and not drawHidden:
        main.complain("Really? Didn't account for this...")

    fieldList = []
    fields = leaf.fields()
    for field in fields:
        if drawHidden or (field.hidden == False):
            fieldList.append(field.key())

    if drawDeleted:
        deletedFieldSet = set([])
        for entry in data:
            deletedFieldeSet = deletedFieldSet.union(set(entry.keys()))
        deletedFieldList = list(deletedFieldSet)
        deletedFieldList.sort()

        for field in deletedFieldList:
            if field not in fieldList:
                fieldList.append(field)

    # Get data into the lists
    rows = []
    rows.append(fieldList)
    for entry in data:
        row = []
        for field in fieldList:
            if field in entry:
                row.append(entry[field])
            else:
                row.append(None)
        rows.append(row)

    if isinstance(priorityCol,int):
        priorityDict = {priorityCol:20}
    else:
        priorityDict = {}
        priorityCol = 0

    if isinstance(unfinishedEntry,dict):
        data.remove(unfinishedEntry)          # otherwise it just keeps growing
    return drawTableFromListOfLists(rows, "Full", 10,priorityDict,maxWidth,priorityCol,maxHeight,"Top",False)



"""
Okay, so to do this table, first write a general table writer from listoflists
Once basic done, add the following features:
*Optional to display title
*MaxWidth (first general, then col by col)
*Priority col (as in centre around if it there's not room for the whole table even at minWidths)
*maxheight, priority height






Okay, so there is a confusion here between different options. Minimum widths and priority col work on different systems.
I could double them up, but don't think it's worth it


for each col:


The maximum natural width => N
The setting for maxwidth  => +
The width of the column   => W

W is maximized under the following constraints:

W < N
W < +





maxWidth (global or dict)
actualLength (global or dict)
minWidth (global or dict)



priority col

expand equally from both directions, if you hit one side, stop and expand the other way.

___!!!!!????????!!!!!__________
0120123401234567012340123456789
preLength - spare = 8-5 = 3
postLength - spare =







"""
def drawTableFromListOfLists(data,title,maxWidth_global,maxWidth_dict, maxTotalWidth,centralCol,maxHeight,cutFrom,highlightBottomRow=False):
    maxLength = {}


    height = len(data)
    if title == "None":
        maxHeight += 1

    highlightLength = 0
    if highlightBottomRow:
        highlightLength = 2

    if maxHeight - highlightLength < 2:
        main.complain("That's not exactly a table now is it.")
    if height > maxHeight- highlightLength:
        if cutFrom == "Bottom":
            data = data[:(maxHeight-highlightLength)]
        elif cutFrom == "Top":
            data = [data[0],] + data[-(maxHeight-highlightLength)+1:]



    for k in range(len(data)):
        if k !=0 or title == "Full":
            row = data[k]
            for i in range(len(row)):
                    if i not in maxLength:
                        maxLength[i] = 0
                    cell = row[i]
                    if not cell == None:
                        maxLength[i] = max(len(str(cell)),maxLength[i])
                    if i in maxWidth_dict:
                        maxWidth = maxWidth_dict[i]
                    else:
                        maxWidth = maxWidth_global
                    maxLength[i] = min(maxLength[i],maxWidth)


    rows = []

    for rowList in data:
        rowText = "|"
        for i in range(len(rowList)):
            if not rowList[i] == None:
                rowText += cutTo(str(rowList[i]),maxLength[i]) + "|"
            else:
                rowText += cutTo("?",maxLength[i]) + "|"

        rows.append(rowText)

    cut, add = findCut(maxLength, centralCol, maxTotalWidth)
    for i in range(len(rows)):
        rows[i] = add[0] + rows[i][cut[0]:cut[1]] + add[1]


    if title == "None":
        rows = rows[1:]

    if highlightBottomRow:
        rows = rows[:-1] + [len(rows[0])*"-", rows[-1], len(rows[0])*"-"]
    return rows


def findCut(maxLength, centralCol, maxTotalWidth):

    preLength = 1

    for i in range(centralCol):
        preLength += maxLength[i] + 1

    centralLength = maxLength[centralCol]

    postLength = 1
    for i in range(centralCol+1,max(maxLength)+1):
        postLength += maxLength[i] + 1


    if centralLength > maxTotalWidth - 6:
        main.complain("haven't accounted for this...")
    if preLength + centralLength + postLength <= maxTotalWidth:
        return((0,maxTotalWidth),("",""))
    if preLength * 2 + centralLength + 3 <= maxTotalWidth:
        return((0,maxTotalWidth-3),("","..."))
    if postLength * 2 + centralLength + 3 <= maxTotalWidth:
        return((-maxTotalWidth+3,preLength + centralLength + postLength),("...",""))
    else:
        spare_R = (maxTotalWidth - centralLength - 6)/2
        spare_L = (maxTotalWidth - centralLength - 6) - spare_R
        print "!"

        return((preLength-spare_L, spare_R-postLength),( "...","..."))





