# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file contains the AST for the Ren'Py script language. Each class
# here corresponds to a statement in the script language.

# NOTE:
# When updating this file, consider if lint.py or warp.py also need
# updating.

################################################################################
# Custom types
################################################################################

class TreeNode(object):

    # Custom parameter
    nchildren = None

    # Custom parameter
    # Indicates that this object should be removed from the resulting tree
    nexclude = False

    # Custom parameter
    # A reference to another node, that holds this object
    nparent = None

    def __iter__(self):
        yield self

        if self.nchildren:
            for child in self.nchildren:
                if isinstance(child, TreeNode):
                    yield from child
                else:
                    yield child

        yield TreeIterBlockEnd()

class TreeIterBlockEnd(TreeNode):

    pass

class RootNode(TreeNode):

    def __init__(self, children=None):
        super(TreeNode, self).__init__()

        if children is None:
            children = []

        self.nchildren = TreeList(children + [EmptyLine()], self)
        self.nexclude  = False
        self.nparent   = None

class SwitchNode(TreeNode):

    def __setstate__(self, state):
        super().__setstate__(state)

        self.nchildren = TreeList(main_node=self)
        self.nexclude  = True

    def prepare_part(self, index, condition, children):
        if index == 0:
            return SwitchNode.Part('if %s:' % condition, children)
        elif condition and condition != 'True':
            return SwitchNode.Part('elif %s:' % condition, children)
        else:
            return SwitchNode.Part('else:', children)

    class Part(TreeNode):

        def __init__(self, condition, children):
            super().__init__()

            self.value = condition
            self.nchildren = TreeList(children, self)

        def __str__(self):
            return self.value

class EmptyLine(TreeNode):

    def __str__(self):
        return ''

class ValuedNode(TreeNode):

    def __init__(self, value, children=None, exclude=None):
        super(TreeNode, self).__init__()

        self.value     = value
        self.nchildren = children
        self.nexclude  = exclude

    def __str__(self):
        return str(self.value)

class TreeList(list):

    def __init__(self, seq=(), main_node=None):
        super().__init__(seq)

        self.__parent_node = main_node

        for item in seq:
            if isinstance(item, TreeNode):
                item.nparent = self.__parent_node

    def append(self, obj):
        super().append(obj)

        if isinstance(obj, TreeNode):
            obj.nparent = self.__parent_node

    def insert(self, index, obj):
        super().insert(index, obj)

        if isinstance(obj, TreeNode):
            obj.nparent = self.__parent_node
