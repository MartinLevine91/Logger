import main


WINDOW_HEIGHT = 24
WINDOW_WIDTH = 80

def superClear():
    for i in range(WINDOW_HEIGHT*4):
        print ""

def drawWindow(title,content,instruction,userInput):
    """
    Draws a window from lists of title, content, instruction and userInput.
    Lines must not be more than maximum width and there must not be more than
    the maximum number of rows. Any empty space will be filled up though.
    """

    
    sectionChar = "-"
    endSection = [(WINDOW_WIDTH * sectionChar),]
    newLine = [""]
    
    lineCount = len(title+content+instruction+userInput) + 3

    if lineCount > WINDOW_HEIGHT:
        print "rendering error! used too many rows"
        print "title       ", len(title)
        print "content     ", len(content)
        print "instruction ", len(instruction)
        print "userinput   ", len(userinput)
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
                 userInput

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




# drawWindow(["Title!",],["1. *","2. **","3. ***"],["Do things!", "lots of things"], ["input:"])

def drawMenuSelection(state):
    """
    Currently will fail if number of options exceeds maximum as determined
    by row limit
    """
    if isinstance(state.currentM,main.Branch):
        Title_str = "..."
        rootFinder = state.currentM
        while not isinstance(rootFinder, main.Root):
            Title_str = rootFinder.key() + "/" + Title_str
            rootFinder = rootFinder.parent()
            
        maxChars =  WINDOW_WIDTH - len("Menu selection: ~/")
        
        if len(Title_str) > maxChars:
            Title_str = "Menu selection: .." + Title_str[-maxChars:]
        else:
            Title_str = "Menu selection: ~/" + Title_str

        currentMenuOption = state.currentM
    else:
        Title_str = "..."
        rootFinder = state.currentL
        while not isinstance(rootFinder, main.Root):
            Title_str = rootFinder.key() + "/" + Title_str
            rootFinder = rootFinder.parent()
            
        maxChars =  WINDOW_WIDTH - len(state.currentM.key() + ": ~/")
        
        if len(Title_str) > maxChars:
            Title_str = state.currentM.key() + ": .." + Title_str[-maxChars:]
        else:
            Title_str = state.currentM.key() + ": ~/" + Title_str

        currentMenuOption = state.currentL


      
    
    title = [Title_str,]
    
    listOfChildren = currentMenuOption.children()
    content = []
    for i in range(len(listOfChildren)):
        content.append(str(i+1) + ". " + listOfChildren[i].key())

    content.append(str(len(listOfChildren)+1) + ". Back")
    
    instructions = ["Just pick an option from above.","And enter it below!"]
    userInput = ["Option:"]

    drawWindow(title,content,instructions,userInput)

def draw(state):
    if state.returnMode() == "Menu":
        drawMenuSelection(state)
    else:
        print "Cannot draw other modes yet."
        print cannotDrawOtherModesYet
    
    
