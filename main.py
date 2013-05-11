# main.py
#
# Functionality:
#
# * DONE Store data reliably
# * Export data for post-processing
# * DONE Define tree of keys
# * DONE Each leaf stores entries, each entry has a number of fields
# * SEMI-DONE Define datatypes for fields
# * Datatypes to include int, range, choice (plus subchoices?), text, timestamp
#   DONE Timestamp (minute): now, yesterday, ... !! check this is DST-safe !!
#   NOT MY PROBLEM Navigate by single keystrokes
# * Change descriptions and add  / delete fields, on the fly
#   Hidden data (for redundant information) - ie when a field has been removed ("hidden") from that leaf
#   NOT MY PROBLEM Easy save-and-quit
#
# Attributes:
#   DONE (Python) Low memory footprint
#   DONE (Python) Maintainable by Martin
#   Strategy for updating the tree once there's data in it

# Test (should not error; the new file should be the same as the old
# one):
# >>> import main
# >>> main.read('play.xml').write('play2.xml')
# >>>

# Interface:
#
# 1. Constructors
#
# root(key = 'Everything') makes a new root. Key is a string.
#
# self.branch(key) makes a new branch. Self is a branch (or root); key
# is a string (not already in use as one of self's keys).
#
# self.leaf(key) makes a new leaf. Self is a branch (or root); key is
# a string (not already in use as one of self's keys).
#
# self.field(key, datatype, default = None, optional = None, help =
# None, hidden = False) describes a new field. Self is a leaf; key and datatype must
# be strings.
#
# self.entry(table) adds the given table to self's entries. Self is a
# leaf; table must be a Python dictionary.
#
# self.move(parent=None, key=None) changes parent or key (or both) of
# branch or leaf. Similarly self.move(self, leaf=None, key=None) for a
# field.
#
# self.remove() removes a branch, leaf or field from its parent.
#
# self.remove_entry(key) removes an entry from its leaf.
#
#
# 2. Introspection
#
# self.key() returns the key of a branch, leaf or field.
#
# self.parent() returns the parent node of a branch or leaf, or the
# leaf of an entry.
#
# self.children() returns a list of self's child nodes; self is a
# branch.
#
# self.find(key) returns the child of that branch (or the field of
# that leaf) which has the given key. If key not found, returns None.
#
# self.entries() returns the entries of that leaf as a list of python
# Dictionaries.
#
# self.fields() returns the fields of that leaf as a list.
#
#
# 3. I/O
#
# self.write(file) writes the tree out to an xml file. Self must be a
# root.
#
# read(file) reads a tree out of an xml file and returns an instance
# of Root.
#
#
# 4. Time utilities
#
# now() returns a Time instance representing the current date/time.
#
# str(Time) returns a string (such as 'Sun Jun 20 23:21:00 1993')
# corresponding to such a Time.
#
# self.previous(days=None, hours=None, minutes=None) returns a new
# Time which varies from self (another Time) by the stated
# ammounts. If you give hours but not minutes, the Time will be
# rounded back to the start of the hour; if you give days but not
# hours the Time will be rounded back to the start of the day. For
# example, t.previous(days=0) would give the midnight just gone; and
# t.previous(hours=1, minutes=0) gives precisely one hour ago.

bug = [
"                            .    . ",
"                             )  (  ",   
"       _ _ _ _ _ _ _ _ _ _ _(.--.) ",   
"     {{ { { { { { { { { { { ( '_') ",
"      >>>>>>>>>>>>>>>>>>>>>>>`--'> "]

import xml.etree.ElementTree as etree
import time
import json

def complain(what):
    for line in bug:
        print line
    raise Exception(what)


class Node():
    def parent(self):
        return self._parent

    def key(self):
        return self._key

    def move(self, parent=None, key=None):
        if isinstance(parent, Branch):
            if key is None:
                key = self._key
            if parent.find(key):
                complain('New parent %s already has a child called %s' % (parent, key))
            else:
                self._parent._children.remove(self)
                parent._children.append(self)
                self._parent = parent
                self._key = key
        elif parent is None:
            if key is not None:
                if self._parent.find(key):
                    complain('%s already has a child called %s' % (self._parent, key))
                else:
                    self._key = key
        else:
            complain('New parent %s for %s isn\'t a branch.' % (parent, self))

    def remove(self):
        self._parent._children.remove(self)


class Branch(Node):
    def __init__(self, key, parent):
        if parent and not isinstance(parent, Branch):
            complain('Branch parent %s is not a branch.' % (parent,))
        elif not isinstance(key, str):
            complain('Branch key %s is not a string.' % (key,))
        else:
            self._children = []
            self._key = key
            self._parent = parent

    def __repr__(self):
        children = self._children
        length = len(children)
        key = self._key
        name = self.__class__.__name__
        if length == 1:
            return '<%s %s (1 child) 08%x>' % (name, key, id(self))
        else:
            return '<%s %s (%d children) 08%x>' % (name, key, length, id(self))

    def children(self):
        return self._children

    def find(self, key):
        for child in self._children:
            if child._key == key:
                return child
        return None

    def branch(self, key):
        if self.find(key):
            complain('Branch %s already has a child called %s.' % (self._key, key))
        branch = Branch(parent = self, key = key)
        self._children.append(branch)
        return branch

    def leaf(self, key):
        if self.find(key):
            complain('Leaf %s already has a child called %s.' % (self._key, key))
        leaf = Leaf(parent = self, key = key)
        self._children.append(leaf)
        return leaf

    def xml(self):
        name = self.__class__.__name__
        xml = etree.Element(name, {'key': self._key})
        for child in self._children:
            xml.append(child.xml())
        return xml

    @classmethod
    def parse(cls, elt, parent, parse_children):
        return parse_children(parent.branch)


class Root(Branch):
    def remove(self):
        complain('Cannot remove root.')

    def move(self, parent=None, key=None):
        if parent is not None:
            complain('Cannot move node.')
        self._key = key

    def write(self, file):
        etree.ElementTree(self.xml()).write(file)

    @classmethod
    def parse(cls, elt, parent, parse_children):
        if parent:
            complain('Root cannot have parent %r' % (parent,))
        else:
            return parse_children(root)


class Leaf(Node):
    def __init__(self, key, parent):
        if not isinstance(parent, Branch):
            complain('Leaf parent %s is not a branch.' % (parent,))
        elif not isinstance(key, str):
            complain('Left key %s is not a string.' % (key,))
        else:
            # fields is an list whose items each describe one entry
            self._fields = []
            # each entry is a table which keys field names against their values
            self._entries = []
            self._key = key
            self._parent = parent

    def __repr__(self):
        entries = self._entries
        length = len(entries)
        key = self._key
        if length == 1:
            return '<Leaf %s (1 entry) 08%x>' % (key, id(self))
        else:
            return '<Leaf %s (%d entries) 08%x>' % (key, length, id(self))

    def remove_entry(self, entry):
        self._entries.remove(entry)

    def fields(self):
        return self._fields

    def entries(self):
        return self._entries

    def find(self, key):
        for field in self._fields:
            if field._key == key:
                return field
        return None

    def field(self, key, datatype, default = None, optional = None, help = None, hidden = False):
        if self.find(key):
            complain('Leaf %s already has a field called %s.' % (self._key, key))
        field = Field(self, key, datatype, default, optional, help, hidden)
        self._fields.append(field)
        return field

    def entry(self, table):
        if not isinstance(table, dict):
            complain('Leaf table %s is not a dictionary.' % (table,))
        else:
            self._entries.append(table)
            return table

    def xml(self):
        xml = etree.Element('Leaf', {'key': self._key})
        for field in self._fields:
            xml.append(field.xml())
        for entry in self._entries:
            d = etree.Element('Entry')
            for key in entry:
                v = etree.Element('Value', {'key': key})
                v.text = str(entry[key])
                d.append(v)
            xml.append(d)
        return xml

    @classmethod
    def parse(cls, elt, parent, parse_children):
        return parse_children(parent.leaf)


class Field():
    def __init__(self, leaf, key, datatype, default=None, optional=False, help=None, hidden = False):
        if not isinstance(leaf, Leaf):
            complain('Field leaf %s is not a leaf.' % (leaf,))
        elif not isinstance(key, str):
            complain('Field key %s is not a string.' % (key,))
        elif not isinstance(datatype, str):
            complain('Field datatype %s is not a string.' % (datatype,))
        elif not validDatatype(datatype):
            complain('Field datatype %s is not a valid datatype.' % (datatype,))
        else:
            self._leaf = leaf
            self._key = key
            # number, range, text, choice, timestamp - enforced during data entry
            self.datatype = datatype
            # value if this field isn't set in a particular entry
            self.default = default
            # also enforced only by data entry
            self.optional = optional
            # currently a shortish string, might add more text, images or whatever later
            self.help = help
            # true or false            
            self.hidden = hidden

    def __repr__(self):
        return '<Field %s, for %s 0x%x>' %  (self._key, self._leaf._key, id(self))

    def key(self):
        return self._key

    def parent(self):
        return self._leaf

    def move(self, leaf=None, key=None):
        if isinstance(leaf, Node):
            if key is None:
                key = self._key
            if leaf.find(key):
                complain('New parent %s already has a field called %s' % (leaf, key))
            else:
                self._leaf._fields.remove(self)
                leaf._fields.append(self)
                self._leaf = leaf
                self._key = key
        elif leaf is None:
            if key is not None:
                if self._leaf.find(key):
                    complain('%s already has a field called %s' % (self._leaf, key))
                else:
                    self._key = key
        else:
            complain('New leaf %s for %s isn\'t a node.' % (leaf, self))

    def remove(self):
        self._leaf._fields.remove(self)

    def xml(self):
        xml = etree.Element('Field', {'key': self._key, 'datatype': self.datatype})
        if self.optional:
            xml.set('optional', 'yes')
            if self.default:
                xml.set('default', self.default)
        if self.help:
            xml.set('help', self.help)
        return xml

    @classmethod
    def parse(cls, elt, parent, parse_children):
        attrib = elt.attrib
        def get(k):
            if k in attrib:
                return attrib[k]
        field = parent.field(*(map(get,('key', 'datatype', 'default', 'optional', 'help'))))
        field.optional = field.optional == 'yes'
        return field

def read(file):
    class Entry:
        @classmethod
        def parse(cls, elt, parent, parse_children):
            return parse_children(lambda(key): parent.entry({}))

    class Value:
        @classmethod
        def parse(cls, elt, parent, parse_children):
            try:
                value = int(elt.text)
            except ValueError:
                value = elt.text
            parent[elt.attrib['key']] = value

    def parse(elt, parent):
        attrib = elt.attrib
        if 'key' in attrib:
            key = attrib['key']
        else:
            key = None
        def parse_children(constructor):
            instance = constructor(key)
            for child in elt:
                parse(child, instance)
            return instance
        try:
            return names[elt.tag].parse(elt, parent, parse_children)
        except KeyError:
            complain('Element tag %s unknown.' % (elt,))

    names = dict(globals(), **locals())                 # a shameful hack
    root = parse(etree.parse(file).getroot(), None)
    if isinstance(root, Root):
        return root
    else:
        complain('Root %s is not a root.' % (root,))


def root(key = 'Everything'):
    return Root(key, None)

class Time:
    def __init__(self, time, roundto=60):
        self.time = int(time / roundto) * roundto

    def __repr__(self):
        return '<Time %d>' %  (self.time,)

    def __str__(self):
        return time.asctime(time.localtime(self.time))

    def previous(self, days=None, hours=None, minutes=None):
        delta = 0
        if days: delta = delta + days * 86400
        if hours: delta = delta + hours * 3600
        if minutes: delta = delta + minutes * 60
        new = self.time - delta
        if hours is None and days is not None:
            # Round back to midnight
            maybe = Time(new, 86400)
            # Check for summertime changes - the above rounding may have been bogus
            hours = time.localtime(maybe.time).tm_hour
            if hours == 0:
                return maybe
            elif hours == 1:
                return Time(maybe.time - 3600)
            else:
                complain('Lost in time. And lost in space. And meaning.')
        elif minutes is None and hours is not None:
            return Time(new, 3600)
        else:
            return Time(new)

def now():
    return Time(time.mktime(time.localtime()))


def validDatatype(datatype_str):
# Datatypes should be a string of the form "['Datatypename',[listofinfofordatatype]]"

    try:
        datatype_lst = json.loads(datatype_str)
    except:
        return False
    if not isinstance(datatype_lst,list):
        return False
    
    elif datatype_lst[0] not in ["String","Int","Float","Range","Choice","Time"]:
        return False

    elif datatype_lst[0] in ["String","Int","Float"]:
        return True

    elif datatype_lst[0] == "Range":
        if not isinstance(datatype_lst[1], list):
            return False
        elif isinstance(datatype_lst[1][0], int) and  isinstance(datatype_lst[1][1], int):
            if datatype_lst[1][0] < datatype_lst[1][1]:
                return True
        return False
    elif datatype_lst[0] == "Choice":
        try:
            if isinstance(choiceList,list):
                
                choiceList = Choice(datatype_lst[1])
                if len(datatype_lst[1]) > 0:
                    choiceList.pickChoice(1)
                return True
            else:
                return False
        except:
            return False
    elif datatype_lst[0] == "Time":
        if datatype_lst[1] in ["Minute","Hour","Day","Month","Year"]:
            return True
        else:
            return False
    complain("Datatype validation went horribly wrong")




class Choice:
# List of form [[name1, option],
#               [name2,[[name2a,option],[name2b,option]],
#               [name3,option]]
# list[

    def __init__(self, choiceList):
        self.choiceList = choiceList
        self.currentChoiceList = choiceList
        self.keyList = []
        self.name = ""

    def setOfAllChoices(self, listOfChoices = None):
        if listOfChoices == None:
            listOfChoices = self.choiceList
        choiceSet = set([])
        if not isinstance(listOfChoices, list):
            choiceSet.add(listOfChoices)
            return choiceSet
        for choice in listOfChoices:
            newSet = self.setOfAllChoices(choice[1])
            choiceSet = choiceSet.union(newSet)
        return choiceSet
    
    def updateCurrentList(self):
        currentChoiceList = self.choiceList
        self.name = ""
        for key in self.keyList:
            self.name = currentChoiceList[key][0]
            currentChoiceList = currentChoiceList[key][1]
        self.currentChoiceList = currentChoiceList
        
        
    def pickChoice(self,key):
        # Pick a choice, indexing from one. If currently on a leaf choice, it assumes the wanted choice is "back"        
        if isinstance(self.currentChoiceList,list):
            if key-1 < len(self.currentChoiceList):
                self.keyList.append(key-1)
            elif key-1 == len(self.currentChoiceList) and len(self.keyList) > 0:
                self.keyList.pop()
            self.updateCurrentList()
        else:
            self.keyList.pop()
            self.updateCurrentList()

    def addChoice(self,newName,newOption):
        if isinstance(currentChoiceList[0],list):
            #add a sibling option            
            self.currentChoiceList.append([newName,newOption])
        else:
            complain("Something's wrong with a use of 'addChoice'")

    def changeName(self,newName):
        if isinstance(currentChoiceList[0], str):
            currentChoiceList[0] = newName
        else:
            print error

    def changeOption(self,newOption):
        if isinstance(currentChoiceList[0], str):
            currentChoiceList[1] = newOption
        else:
            print error


def test():
    this = root('Test')
    health = this.branch('Health')
    visit = health.leaf('Toilet Visit')
    visit.field('Solidity', '["int",[]]', None, False, '0 for completely liquid, 10 for healthy')
    visit.field('Gut pain', '["int",[]]', None, False, '0 for no pain, 10 for screaming')
    visit.entry({'Solidity': 6, 'Gut pain': 3})
    visit.entry({'Solidity': 3})
    return this





