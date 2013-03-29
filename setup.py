"""
This module sets up the data structure required for run.py

> Add new log entry
> Add/edit logs
>> Add log
>> Edit log
>>> Edit location of log in data structure
>>> Edit fields for log
> View log data


"""

import main

# Create new tree
current = main.root("root")

# > Add a new log entry
current.leaf("Enter data")

# > Add/edit log templates
current = current.branch("Add/Edit log templates")

# >> Add log template
current.leaf("Add log")

# >> Edit log templates
current = current.branch("Edit log")

# >>> Edit the location of a log template in log-tree
current.leaf("Edit location of a log template in log-tree")
# >>> Edit the fields for log
current.leaf("Edit the fields in a log template")
current = current.parent()
current = current.parent()
# > View log data
current.leaf("View log data")

current.write("Menu.xml")



