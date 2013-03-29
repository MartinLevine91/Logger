# main.py
#
# Functionality:
#
# * DONE Store data reliably
# * Export data for post-processing
# * DONE Define tree of keys
# * DONE Each leaf stores data, each datum has a number of fields
# * SEMI-DONE Define data-types for fields
# * Data types to include range, choice, text, timestamp
#   NOT MY PROBLEM Navigate by single keystrokes
# * Change descriptions and add  / delete fields, on the fly
#   Hidden fields (for redundant information)
#   NOT MY PROBLEM Easy save-and-quit
#
# Attributes:
#   DONE (Python) Low memory footprint
#   DONE (Python) Maintainable by Martin
#   Strategy for updating the tree once there's data in it

# >>> import main
# >>> main.read('play.xml').write('play2.xml')
# >>>

import xml.etree.ElementTree as etree

def complain(what):
    raise Exception(what)

class Node():
    pass

class Branch(Node):
    def __init__(self, key, parent):
        if parent and not isinstance(parent, Branch):
            complain('Branch parent %s is not a branch.' % (parent,))
        elif not isinstance(key, str):
            complain('Branch key %s is not a string.' % (key,))
        else:
            self.children = []
            self.key = key
            self.parent = parent

    def __repr__(self):
        children = self.children
        length = len(children)
        key = self.key
        name = self.__class__.__name__
        if length == 1:
            return '<%s %s (1 child) 08%x>' % (name, key, id(self))
        else:
            return '<%s %s (%d children) 08%x>' % (name, key, length, id(self))

    def child_type(self):
        if self.children:
            return self.children[0].__class__.__name__

    def find(self, key):
        for child in self.children:
            if child.key == key:
                return child
        return None

    def branch(self, key):
        if self.child_type() == 'Leaf':
            children = self.children
            if len(children) == 1:
                fmt = 'May not add a branch to parent %r whose other child is a leaf.'
            else:
                fmt = 'May not add a branch to parent %r whose other children are leaves.'
            complain(fmt % (self,))
        if self.find(key):
            complain('Branch %s already has a child called %s.' % (self.key, key))
        branch = Branch(parent = self, key = key)
        self.children.append(branch)
        return branch

    def leaf(self, key):
        if self.child_type() == 'Branch':
            children = self.children
            if len(children) == 1:
                fmt = 'May not add a leaf to parent %r whose other child is a branch.'
            else:
                fmt = 'May not add a leaf to parent %r whose other children are branches.'
            complain(fmt % (self,))
        if self.find(key):
            complain('Leaf %s already has a child called %s.' % (self.key, key))
        leaf = Leaf(parent = self, key = key)
        self.children.append(leaf)
        return leaf

    def xml(self):
        name = self.__class__.__name__
        xml = etree.Element(name, {'key': self.key})
        for child in self.children:
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
    root = etree.parse(file).getroot()
    return parse(root, None)


class Leaf(Node):
    def __init__(self, key, parent):
        if not isinstance(parent, Branch):
            complain('Leaf parent %s is not a branch.' % (parent,))
        elif not isinstance(key, str):
            complain('Left key %s is not a string.' % (key,))
        else:
            # fields is an list whose items each describe one datum
            self.fields = []
            # each datum is a table which keys field names against their values
            self.data = []
            self.key = key
            self.parent = parent

    def __repr__(self):
        data = self.data
        length = len(data)
        key = self.key
        if length == 1:
            return '<Leaf %s (1 datum) 08%x>' % (key, id(self))
        else:
            return '<Leaf %s (%d data) 08%x>' % (key, length, id(self))

    def find(self, key):
        for field in self.fields:
            if field.key == key:
                return field
        return None

    def field(self, key, datatype, default, optional, help):
        if self.find(key):
            complain('Leaf %s already has a field called %s.' % (self.key, key))
        field = Field(self, key, datatype, default, optional, help)
        self.fields.append(field)
        return field

    def datum(self, table):
        self.data.append(table)
        return table

    def xml(self):
        xml = etree.Element('Leaf', {'key': self.key})
        for field in self.fields:
            xml.append(field.xml())
        for datum in self.data:
            d = etree.Element('Datum')
            for key in datum:
                v = etree.Element('Value', {'key': key})
                v.text = str(datum[key])
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
        else:
            self.leaf = leaf
            self.key = key
            # value if this field isn't set in a particular datum
            self.default = default
            # number, range, text, choice, timestamp - enforced during data entry
            self.datatype = datatype
            # also enforced only by data entry
            self.optional = optional
            # currently a shortish string, might add more text, images or whatever later
            self.help = help

    def __repr__(self):
        return '<Field %s, for %s 0x%x>' %  (self.key, self.leaf.key, id(self))

    def xml(self):
        xml = etree.Element('Field', {'key': self.key, 'datatype': self.datatype})
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


class Datum:
    @classmethod
    def parse(cls, elt, parent, parse_children):
        return parse_children(lambda(key): parent.datum({}))

class Value:
    @classmethod
    def parse(cls, elt, parent, parse_children):
        try:
            value = int(elt.text)
        except ValueError:
            value = elt.text
        parent[elt.attrib['key']] = value


def new_root(key = 'Everything'):
    return Root(key, None)

root = new_root()

def test():
    root = new_root('Test')
    health = root.branch('Health')
    visit = health.leaf('Toilet Visit')
    visit.field('Solidity', 'range(0,10)', None, False, '0 for completely liquid, 10 for healthy')
    visit.field('Gut pain', 'range(0,10)', None, False, '0 for no pain, 10 for screaming')
    visit.datum({'Solidity': 6, 'Gut pain': 3})
    visit.datum({'Solidity': 3})
    return root
