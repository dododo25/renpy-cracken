class Node:

    def __init__(self, value=None, children=None):
        self.value = value
        self.parent: Node | None = None

        if children is None:
            self.children: list[Node] | None = None
        else:
            self.children: list[Node] | None = TreeList(children, self)

    def __iter__(self):
        yield self

        if self.children and self.children:
            for child in self.children:
                if isinstance(child, Node):
                    yield from child
                else:
                    yield child

            yield TreeIterBlockEnd()

    def __repr__(self):
        return self.value

class TreeIterBlockEnd(Node):

    pass

class TreeList(list):

    def __init__(self, seq, parent: Node):
        super().__init__(seq)

        self._parent = parent

        for item in seq:
            item._parent = parent

    def append(self, obj):
        super().append(obj)

        if isinstance(obj, Node):
            obj.parent = self._parent

    def insert(self, index, obj):
        super().insert(index, obj)

        if isinstance(obj, Node):
            obj.parent = self._parent
