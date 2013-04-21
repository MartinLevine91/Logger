"""
This module sets up the data structure required for run.py

> Add new log entry
> Add/edit log template
>> Add log template
>> Edit log template
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
current = current.branch("Add or Edit log templates")

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


logs = main.root('logs')
health = logs.branch('Health')
visit = health.leaf('Toilet Visit')
visit.field('Solidity', 'range(0,10)', None, False, '0 for completely liquid, 10 for healthy')
visit.field('Gut pain', 'range(0,10)', None, False, '0 for no pain, 10 for screaming')
visit.entry({'Solidity': 6, 'Gut pain': 3})
visit.entry({'Solidity': 3})
logs.write("Logs.xml")


