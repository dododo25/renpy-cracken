class Node(object):

    pass

class Element(Node):

    def __init__(self, type=None, value=None, level=None):
        self.type = type
        self.value = value
        self.level = level

    def __repr__(self) -> str:
        return 'Element{type=%s, value=%s}' % (self.type, self.value)

class Container(Element):

    def __init__(self, type=None, value=None, level=None, elements=[]):
        super(Container, self).__init__(type, value)

        self.elements = elements
        self.level = level

    def __repr__(self) -> str:
        return 'Container{type=%s, value=%s}' % (self.type, self.value)
