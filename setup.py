"""
This module creates an example LogTree called "Logs.xml"
"""

import main


logs = main.root('logs')
health = logs.branch('Health')
visit = health.leaf('Toilet Visit')
visit.field('Solidity', 'range(0,10)', None, False, '0 for completely liquid, 10 for healthy')
visit.field('Gut pain', 'range(0,10)', None, False, '0 for no pain, 10 for screaming')
visit.entry({'Solidity': 6, 'Gut pain': 3})
visit.entry({'Solidity': 3})
logs.write("Logs.xml")



