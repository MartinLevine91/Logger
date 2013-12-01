def show(listOfLines):
    for line in listOfLines:
        print line

def display(listOfViews):
    if len(listOfViews) in [1,2,3,4]:
        for i in range(len(listOfViews)):
            for j in range(len(listOfViews[i])):
                listOfViews[i][j] = listOfViews[i][j][:80] + (80-len(listOfViews[i][j]))*" "
            listOfViews[i] = listOfViews[i][:24] + (24-len(listOfViews[i]))*[80*" ",]
        if len(listOfViews) == 1:
            for i in range(len(listOfViews[0])):
                print listOfViews[0][i]
        elif len(listOfViews) == 2:
            for i in range(len(listOfViews[0])):
                print listOfViews[0][i] + " * " + listOfViews[1][i]
        elif len(listOfViews) == 3:
            for i in range(len(listOfViews[0])):
                print listOfViews[0][i] + " * " + listOfViews[1][i]
            print 163*"*"
            for i in range(len(listOfViews[2])):
                print listOfViews[2][i]            
        elif len(listOfViews) == 4:
            for i in range(len(listOfViews[0])):
                print listOfViews[0][i] + " * " + listOfViews[1][i]
            print 163*"*"
            for i in range(len(listOfViews[2])):
                print listOfViews[2][i] + " * " + listOfViews[3][i]
    else:
        raise exception("bad list of views")



def split(string,length=80):
    listOfLines = []
    while len(string) > 0:
        line = string[:80]
        line += " "*(80-len(line))
        listOfLines.append(line)
        string = string[80:]
    return listOfLines


STRING_DATA_ENTRY = \
"Entering value for field 'Time of visit'.                                       " + \
"--------------------------------------------------------------------------------" + \
"|##|H|Key               |Type      |*|Default    |Help                         |" + \
"|00| |Gut pain          |Range 0-10|*|           |0 for no pain, 10 for screami|" + \
"|01| |Solidity          |Range 0-7 |*|           |Bristol Solidity Scale: 1. Se|" + \
"|02| |Digestion         |Range 0-10|*|           |0 for whole undigested pieces|" + \
"|03| |Acidity           |Range 0-10|*|           |0 for no acidity, 1 for just |" + \
"|04| |Volume - in cm^3  |Float     |*|           |Make a guess...              |" + \
"|05| |Time on loo - in m|Int       |*|           |From sit down to stand up.   |" + \
"|06| |Time of visit     |Time Min  |*|           |Stand up time.               |" + \
"|07| |Comments          |String    | |No comments|Any relavent info not caught |" + \
"--------------------------------------------------------------------------------" + \
"...idity|Digestion|Acidity|Volume - i|Time on lo|Time of visit      |Comments  |" + \
"...     |?        |?      |?         |?         |?                  |?         |" + \
"...     |9        |0      |200       |15        |2013-10-21 08:50:00|?         |" + \
"...     |4        |0      |150       |10        |2013-10-22 09:05:00|Very dark |" + \
"...     |10       |0      |150       |20        |?                  |?         |" + \
"                                                                                " + \
"--------------------------------------------------------------------------------" + \
"Enter value - date/time to the nearest minute, such as 09:32, or 2013-09-11     " + \
"09:32, or the string 'now' - for field 'Time of visit'; invalid values will be  " + \
"ignored. Stand up time.                                                         " + \
"--------------------------------------------------------------------------------" + \
"$  09:50                                                                        "

OpenScreen = [
"Adding entries to Toilet Visit                                                  ",   
"--------------------------------------------------------------------------------",
"|##|H|Key               |Type      |*|Default    |Help                         |",
"|00| |Gut pain          |Range 0-10|*|           |0 for no pain, 10 for screami|",
"|01| |Solidity          |Range 0-7 |*|           |Bristol Solidity Scale: 1. Se|",
"|02| |Digestion         |Range 0-10|*|           |0 for whole undigested pieces|",
"|03| |Acidity           |Range 0-10|*|           |0 for no acidity, 1 for just |",
"|04| |Volume - in cm^3  |Float     |*|           |Make a guess...              |",
"|05| |Time on loo - in m|Int       |*|           |From sit down to stand up.   |",
"|06| |Time of visit     |Time Min  |*|           |Stand up time.               |",
"|07| |Comments          |String    | |No comments|Any relavent info not caught |",
"--------------------------------------------------------------------------------",
"|Gut pain|Solidity|Digestion|Acidity|Volume - i|Time on lo|Time of vi|Comment...",
"|3       |6       |?        |?      |?         |?         |?         |?      ...",
"|?       |3       |?        |?      |?         |?         |?         |?      ...",
"|4       |3.5     |9        |0      |200       |15        |2013-10-21|?      ...",
"|2.5     |2       |4        |0      |150       |10        |2013-10-22|Very da...",
"|4       |5       |10       |0      |150       |20        |2013-11-04|?      ...",
"|?       |?       |?        |?      |?         |?         |?         |?      ...",
"--------------------------------------------------------------------------------",
"To start adding an entry, press enter leaving the input blank. Alternatively    ",
"enter 'Done' to stop adding entries or 'Quit' to save and quit the Logger.      ",
"--------------------------------------------------------------------------------",
"$                                                                               "]






OpenScreen_inst = [
"To start adding an entry, press enter leaving the input blank. Alternatively    ",
"enter 'Done' to stop adding entries or 'Quit' to save and quit the Logger.      "]

STRING_MINI_FIELD_TABLE_PREV = \
"Key: Solidity           Type: Range 0-7    No Default.                          " + \
"Current value: 1                           Prev value: 5                        "

STRING_MINI_FIELD_TABLE_NEXT = \
" Key: Time of visit     Time Min        No Default.                             " + \
"Help: From sit down to stand up.        Prev value: 2013-10-22 09:05:00         "

STRING_MINI_FIELD_TABLE_CURR = \
" Key: Time of visit                     Type: Range 0-7                         " + \
"Prev value: 2013-10-22 09:05:00         No Default.                             "



Old_DataEntryView = split(STRING_DATA_ENTRY)



LineBreak = [Old_DataEntryView[1],]
FieldsTable = Old_DataEntryView[2:11]
DataTable = Old_DataEntryView[12:17]
EmptyLine = [Old_DataEntryView[17],]
Help = Old_DataEntryView[19:22]
Prompt = [Old_DataEntryView[-1],]

MiniFieldTable_Prev = split(STRING_MINI_FIELD_TABLE_PREV)
MiniFieldTable_Next = split(STRING_MINI_FIELD_TABLE_NEXT)
MiniFieldTable_Curr = split(STRING_MINI_FIELD_TABLE_CURR)


Help_Field = [
"Stand up time.                                                                  ",]
Help_Type = [
"Enter value - date/time to the nearest minute, such as 09:32, or 2013-09-11     ",
"09:32, or the string 'now' - for field 'Time of visit'; invalid values will be  ",
"ignored.                                                                        ",]
EnteringData = \
                split("Entering value for field 'Time of visit'.") + \
                LineBreak + \
                DataTable + \
                LineBreak + \
                MiniFieldTable_Curr + \
                LineBreak + \
                Help_Field + \
                EmptyLine*6 + \
                LineBreak + \
                Help_Type + \
                LineBreak + \
                Prompt
n=4

MidScreen_Instructions = [
"To set 'Time of visit' for this entry, press enter leaving the input blank.     ",
"Alternatively enter 'Back' to reset 'Solidity', 'Restart' to start again,       ",
"'Options' to see more options, 'Cancel' to cancel this entry or 'Quit' to quit. "]


MidScreen = \
                split("Break screen") + \
                LineBreak + \
                EmptyLine*2 + \
                split("Previous Field") + \
                LineBreak + \
                MiniFieldTable_Prev + \
                LineBreak + \
                EmptyLine*2 + \
                split("Next Field") + \
                LineBreak + \
                MiniFieldTable_Next + \
                LineBreak + \
                EmptyLine*3 + \
                MidScreen_Instructions + \
                LineBreak + \
                Prompt

OptionScreen_Instructions = [
"Not Yet Programmed. To select a field to enter type 'select' followed by the    ",
"field number or followed by the beginning of the field key (i.e. 'select com'). ",
"To change the focus of the tables, use 'focus' instead of 'select'. Type 'cont' ",
"to continue, 'Restart' to start again, 'Cancel' to cancel this entry or 'Quit'  ",
"to quit.                                                                        ",]

OptionScreen = \
                split("Options Screen") + \
                LineBreak + \
                [FieldsTable[0],] + \
                FieldsTable[-5:] + \
                LineBreak + \
                DataTable + \
                LineBreak + \
                EmptyLine*2 + \
                OptionScreen_Instructions + \
                LineBreak + \
                Prompt


display([Old_DataEntryView,EnteringData,EnteringData,Old_DataEntryView])

