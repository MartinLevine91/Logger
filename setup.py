"""
This module creates an example LogTree called "Logs.xml"
"""

import main


logs = main.root('logs')
health = logs.branch('Health')
visit = health.leaf('Toilet Visit')
visit.field('Solidity', '["Int",[]]', None, False, '0 for completely liquid, 5 for healthy, 10 for rocks',False)
visit.field('Gut pain', '["Int",[]]', None, False, '0 for no pain, 10 for screaming',False)
visit.entry({'Solidity': 6, 'Gut pain': 3})
visit.entry({'Solidity': 3})
logs.write("Logs.xml")


