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

    



    

