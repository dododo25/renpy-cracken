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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import renpy.ast
import renpy.object

class ATLTransformBase(renpy.object.Object):
    """
    This is intended to be subclassed by ATLTransform. It takes care of
    managing ATL execution, which allows ATLTransform itself to not care
    much about the contents of this file.
    """

    __version__ = 1

    parameters    = []
    atl_st_offset = 0
    nosave        = ['parent_transform']

    parent_transform           = None
    predict_block              = None
    atl                        = None
    atl_state                  = None
    context                    = None
    block                      = None
    properties                 = None
    done                       = None
    transform_event            = None
    last_transform_event       = None
    last_child_transform_event = None
    raw_child                  = None

class RawStatement(renpy.ast.Node, object):

    constant = None
    loc      = None

    def __setstate__(self, state):
        self.__dict__.update(state)

# This represents a Raw ATL block.
class RawBlock(RawStatement):

    # Should we use the animation timebase or the showing timebase?
    animation = False

    # A list of RawStatements in this block.
    statements = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.statements:
            self.nchildren = renpy.ast.TreeList(self.statements, self)

    def __str__(self):
        return 'block:'

# This can become one of four things:
#
# - A pause.
# - An interpolation (which optionally can also reference other
# blocks, as long as they're not time-dependent, and have the same
# arity as the interpolation).
# - A call to another block.
# - A command to change the image, perhaps with a transition.
#
# We won't decide which it is until runtime, as we need the
# values of the variables here.
class RawMultipurpose(RawStatement):

    warp_function = None
    warper        = None
    duration      = None
    properties    = []
    expressions   = []
    splines       = []
    revolution    = None
    circles       = '0'

    def __setstate__(self, state):
        super().__setstate__(state)

        self.nexclude = not (self.warper or self.warp_function)

        if not (self.warper or self.warp_function):
            self._prepare_children()

    def __str__(self):
        if not (self.warper or self.warp_function):
            return 'contains:'

        if self.warper:
            value = '%s %s' % (self.warper, self.duration)
        else:
            value = 'warp %s %s' % (self.warp_function, self.duration)

        if self.splines:
            value += ''.join(
                map(lambda item: ' %s %s knot %s' % (item[0], item[1][-1], ' knot '.join(item[1][:-1])),
                    self.splines))

        if self.expressions:
            value += ' ' + ' '.join(
                map(lambda item: item[0] + ('with ' + item[1] if item[1] is not None else ''), self.expressions))

        if self.properties:
            value += ' ' + ' '.join(map(lambda item: ' '.join(item), self.properties))

        if self.revolution:
            value += ' ' + self.revolution

        if self.circles and self.circles != '0':
            value += ' circles %s' % self.circles

        return value

    def _prepare_children(self):
        self.nchildren = renpy.ast.TreeList([], self)

        for k, v in self.expressions:
            value = k

            if v:
                value += ' with %s' % v

            if value.startswith('outlines'):
                children = RawMultipurpose._list_to_str(value[8:].strip())

                if len(children) == 1:
                    self.children.append(renpy.ast.ValuedNode('outlines [ %s ]' % children[0]))
                else:
                    new_node = renpy.ast.ValuedNode('outlines [')
                    new_node.nchildren = renpy.ast.TreeList(children, new_node)

                    self.nchildren.append(new_node)
                    self.nchildren.append(renpy.ast.ValuedNode(']'))
            else:
                self.nchildren.append(renpy.ast.ValuedNode(value))

        for k, v in self.properties:
            value = k

            if v:
                value += ' %s' % v

            self.nchildren.append(renpy.ast.ValuedNode(value))

    @staticmethod
    def _list_to_str(line):
        res = []

        trimmed = line[1:-1]

        left = 0
        right = 1

        counter = 0

        while right < len(trimmed):
            if counter == 0 and trimmed[right] == ',':
                res.append(trimmed[left:right].strip())
                left, right = right + 1, right + 1

            if trimmed[right] in '[(':
                counter += 1
            elif trimmed[right] in '])':
                counter -= 1

            right += 1

        if left < len(trimmed):
            res.append(trimmed[left:].strip())

        return res

# This lets us have an ATL transform as our child.
class RawContainsExpr(RawStatement):

    expression = None

    def __str__(self):
        return 'contains %s' % self.expression

# This allows us to have multiple ATL transforms as children.
class RawChild(RawStatement):

    children = []

    def __setstate__(self, state):
        super().__setstate__(state)

        self.nexclude = True

        if self.children:
            self.nchildren = renpy.ast.TreeList(self.children, self)

# Implementation of the repeat statement.
class RawRepeat(RawStatement):

    repeats = None

    def __str__(self):
        value = 'repeat'

        if self.repeats:
            value += ' %s' % self.repeats

        return value

# Parallel statement.
class RawParallel(RawStatement):

    blocks = []

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.blocks:
            self.nchildren = renpy.ast.TreeList(self.blocks, self)

    def __str__(self):
        return 'parallel:'

# The choice statement.
class RawChoice(RawStatement):

    choices = []

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.choices:
            self.nchildren = renpy.ast.TreeList(list(map(lambda item: item[1], self.choices)), self)

    def __str__(self):
        return 'choice:'

# The Time statement.
class RawTime(RawStatement):

    time = None

    def __str__(self):
        return 'time %s' % self.time

# The On statement.
class RawOn(RawStatement):

    handlers = {}

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.handlers:
            self.nchildren = renpy.ast.TreeList(list(self.handlers.values())[0].statements, self)

    def __str__(self):
        return 'on %s:' % ', '.join(self.handlers.keys())

# Event statement.
class RawEvent(RawStatement):

    name = None

    def __str__(self):
        value = 'event'

        if self.name:
            value += ' %s' % self.name

        return value

class RawFunction(RawStatement):

    expr = None

    def __str__(self):
        value = 'function'

        if self.expr:
            value += ' %s' % self.expr

        return value
