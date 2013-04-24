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


def drawNotYetProgrammed():
    title = ["Not yet programmed.",]
    content = ["",]
    instructionString = "This part of the program has not been completed yet, enter any input to return to the part of the program that sent you here."
    instructions = splitToWidth(instructionString, WINDOW_WIDTH)
    prompt = ["Press the any key:",]
    drawWindow(title,content,instructions,prompt)

    

def splitToWidth(longStr,maxWidth):
    strList = []
    while len(longStr) > maxWidth:
        strList.append(longStr[:maxWidth])
        longStr = longStr[maxWidth:]
    strList.append(longStr)
    return strList
