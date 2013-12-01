"""
This module creates an example LogTree called "Logs.xml"
"""
import main


logs = main.root('logs')
health = logs.branch('Health')
visit = health.leaf('Toilet Visit')
visit.field('Solidity', 'Int', None, 2, True, '0 for completely liquid, 5 for healthy, 10 for rocks.', False)
visit.field('Gut pain', 'Int', None, 5, False, '0 for no pain, 10 for screaming', False)
visit.entry({'Solidity': 6, 'Gut pain': 3})
visit.entry({'Solidity': 3})
logs.write("Logs.xml")


"""

def add_Entry(state, log = None):

        log = state.currentL
    fields = log.fields()
    fieldsTable = graphics.TableOfFields(log, graphics.WINDOW_WIDTH)

    titleStr = "Adding entries to %s" % (log.key(),)
    title = [graphics.cutTo(titleStr)]
    instStr = "To start adding an entry, press enter leaving the input blank. " + \
              "Alternatively enter 'Done' to stop adding entries or 'Quit' to save and quit the Logger."
    inst = graphics.splitToWidth(instStr)

    spare = graphics.WINDOW_HEIGHT - 6 - len(inst)
    maxLenFieldsTable = min(spare * 2 / 3, len(fieldsTable))
    maxLenDataTable = spare - maxLenFieldsTable

    dataTable = graphics.drawRecentData(leaf=log, maxHeight=maxLenDataTable, unfinishedEntry=partialEntry)
    content = fieldsTable[:maxLenFieldsTable] + [graphics.WINDOW_WIDTH * "-",] + dataTable

    UI = False
    while UI is not None:
        graphics.drawWindow(title, content, inst, ["$ ",])
        UI = userInput()
        if isinstance(UI, str):
            if match(UI,"done"):
                return 0
            elif match(UI,"quit"):
                return quitProgram(state)

    # Permission to proceed! Enter main loop: selecting a field to set and then setting it.
    index = 0
    field = fields[index]

    titleStr = "Adding new entry to %s" % (log.key(),)
    title = [graphics.cutTo(titleStr)]

    while True:
        
        

        
        # What are we allowed to do here?
        navOptions = navigateOptions(fields, index, partialEntry)
        mayGoBack, selectLimit, mayComplete = navOptions

        titleStr = "Break screen - adding new entry to %s" % (log.key(),)
        title = [graphics.cutTo(titleStr)]

        
        inst =  addEntry_genInsts(index, fields, mayGoBack, selectLimit, mayComplete)
        breakScreen = title + 2*LINE + graphics.

        spare = graphics.WINDOW_HEIGHT - 6 - len(inst)
        maxLenFieldsTable = min(spare * 2 / 3, len(fieldsTable))
        maxLenDataTable = spare - maxLenFieldsTable

        dataTable = graphics.drawRecentData(leaf=log, maxHeight=maxLenDataTable, priorityCol=index, unfinishedEntry=partialEntry)
        offset = max(index-maxLenDataTable, 0)
        content = fieldsTable[offset:maxLenFieldsTable+offset] + [graphics.WINDOW_WIDTH * "-",] + dataTable

        
        if addEntry_goToOptions(index,fields,title):
            command = parseAddEntryCommand(index, partialEntry, navOptions, title, content, inst)
        else:
            command = index, partialEntry
        if isinstance(command, str):
            if match(command, "cancel"):
                return
            elif match(command, "done"):
                log.entry(partialEntry)
                # Add another one, probably
                return addEntry(state, log)
            else:
                complain("Unexpected: %s" % (command,))
        else:
            index, partialEntry = command
            field = fields[index]
            if main.validDatatype(field.datatype, field.typeArgs):
                partialEntry = augmentPartialEntry(partialEntry, field, index, log)
                index = index + 1
                if index >= len(fields):
                    index = 0
            else:
                # NDL 2013-10-11 -- I can't help asking how this could happen. Didn't we check this stuff already?
                # MGL 2013-10-26 -- Early stages, I don't massively trust any data-checking we've done so far. 
                editField_drawAndUI("!!! ERROR setting default value for field '%s', invalid datatype." % (field.key(),),
                                    "!!! Either the datatype or the associated type args are not valid. You cannot set a default until this has been fixed.",
                                    graphics.drawField(field))

"""
