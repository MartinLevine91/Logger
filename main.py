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
#   Timestamp (minute): now, yesterday, ... !! check this is DST-safe !!
#   NOT MY PROBLEM Navigate by single keystrokes
# * Change descriptions and add  / delete fields, on the fly
#   Hidden fields (for redundant information)
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
# new_root(key = 'Everything') makes a new root. Key is a string.
#
# self.branch(key) makes a new branch. Self is a branch (or root); key
# is a string (not already in use as one of self's keys).
#
# self.leaf(key) makes a new leaf. Self is a branch (or root); key is
# a string (not already in use as one of self's keys).
#
# self.field(key, datatype, default = None, optional = None, help =
# None) describes a new field. Self is a leaf; key and datatype must
# be strings.
#
# self.entry(table) adds the given table to self's entries. Self is a
# leaf; table must be a Python dictionary.
#
# 2. Introspection
#
# self.key() returns the key of a branch, leaf or field.
#
# self.parent() returns the parent node of a branch or leaf.
#
# self.children() returns a list of self's child nodes; self is a
# branch.
#
# self.find(key) returns the child of that branch (or the field of
# that leaf) which has the given key. If key not found, returns None.
#
# self.entries() returns the entries of that leaf as a list of python Dictionaries.
#
# self.fields() returns the fields of that leaf as a list.
#
# 3. I/O
#
# self.write(file) writes the tree out to an xml file. Self must be a
# root.
#
# read(file) reads a tree out of an xml file and returns an instance
# of Root.

import xml.etree.ElementTree as etree

def complain(what):
    raise Exception(what)

class Node():
    def parent(self):
        return self._parent

    def key(self):
        return self._key

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
    def write(self, file):
        etree.ElementTree(self.xml()).write(file)

    @classmethod
    def parse(cls, elt, parent, parse_children):
        if parent:
            complain("Root cannot have parent %r" % (parent,))
        else:
            return parse_children(new_root)


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

    def fields():
        return self._fields

    def entries():
        return self._entries

    def find(self, key):
        for field in self._fields:
            if field._key == key:
                return field
        return None

    def field(self, key, datatype, default = None, optional = None, help = None):
        if self.find(key):
            complain('Leaf %s already has a field called %s.' % (self._key, key))
        field = Field(self, key, datatype, default, optional, help)
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
    def __init__(self, leaf, key, datatype, default=None, optional=None, help=None):
        if not isinstance(leaf, Leaf):
            complain('Field leaf %s is not a leaf.' % (leaf,))
        elif not isinstance(key, str):
            complain('Field key %s is not a string.' % (key,))
        elif not isinstance(datatype, str):
            complain('Field datatype %s is not a string.' % (datatype,))
        else:
            self.leaf = leaf
            self._key = key
            # number, range, text, choice, timestamp - enforced during data entry
            self.datatype = datatype
            # value if this field isn't set in a particular entry
            self.default = default
            # also enforced only by data entry
            self.optional = optional
            # currently a shortish string, might add more text, images or whatever later
            self.help = help

    def __repr__(self):
        return '<Field %s, for %s 0x%x>' %  (self._key, self.leaf._key, id(self))

    def key(self):
        return self._key

    def xml(self):
        xml = etree.Element('Field', {'key': self._key, 'datatype': self.datatype})
        if self.optional:
            xml.set('optional', True)
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
        return parent.field(get('key'), get('datatype'), get('default'), get('optional'), get('help'))


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


def read(file):
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
            return globals()[elt.tag].parse(elt, parent, parse_children)
        except KeyError:
            complain('Element tag %s unknown.' % (elt,))
    root = parse(etree.parse(file).getroot(), None)
    if isinstance(root, Root):
        return root
    else:
        complain('Root %s is not a root.' % (root,))


def new_root(key = 'Everything'):
    return Root(key, None)

root = new_root()

def test():
    root = new_root('Test')
    health = root.branch('Health')
    visit = health.leaf('Toilet Visit')
    visit.field('Solidity', 'range(0,10)', None, False, '0 for completely liquid, 10 for healthy')
    visit.field('Gut pain', 'range(0,10)', None, False, '0 for no pain, 10 for screaming')
    visit.entry({'Solidity': 6, 'Gut pain': 3})
    visit.entry({'Solidity': 3})
    return root
