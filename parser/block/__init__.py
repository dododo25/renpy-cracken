class Node(object):

    pass

class Element(Node):

    def __init__(self, type=None, value=None, level=None):
        self.type = type
        self.value = value
        self.level = level

    def __repr__(self) -> str:
        return 'Element{type=%s, value=\'%s\'}' % (self.type, self.value)

    def __eq__(self, o):
        if o.__class__ != self.__class__:
            return False

        return o.value == self.value

class Container(Element):

    def __init__(self, type=None, value=None, level=None, children=()):
        super(Container, self).__init__(type, value, level)
        self.children = tuple(children)

    def __eq__(self, o):
        if o.__class__ != self.__class__:
            return False

        return o.value == self.value and o.children == self.children

    def __repr__(self) -> str:
        return 'Container{type=%s, value=\'%s\'}' % (self.type, self.value)
