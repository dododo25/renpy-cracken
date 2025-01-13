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

import renpy.object
import renpy.ast

# This is the context used when compiling an ATL statement. It stores the
# scopes that are used to evaluate the various expressions in the statement,
# and has a method to do the evaluation and return a result.
class Context(object):

    def __init__(self, context):
        self.context = context

    def __eq__(self, other):
        if not isinstance(other, Context):
            return False

        return self.context == other.context

    def __ne__(self, other):
        return not (self == other)

# This is intended to be subclassed by ATLTransform. It takes care of
# managing ATL execution, which allows ATLTransform itself to not care
# much about the contents of this file.
class ATLTransformBase(renpy.object.Object):

    # Compatibility with older saves.
    parameters = renpy.ast.ParameterInfo([ ], [ ], None, None)
    parent_transform = None
    atl_st_offset = 0

    # The block, as first compiled for prediction.
    predict_block = None

    nosave = [ 'parent_transform' ]

    def __init__(self, atl, context, parameters):
        # The constructor will be called by atltransform.

        if parameters is None:
            parameters = ATLTransformBase.parameters

        # The parameters that we take.
        self.parameters = parameters

        # The raw code that makes up this ATL statement.
        self.atl = atl

        # The context in which execution occurs.
        self.context = Context(context)

        # The code after it has been compiled into a block.
        self.block = None

        # The same thing, but only if the code was compiled into a block
        # for prediction purposes only.
        self.predict_block = None

        # The properties of the block, if it contains only an
        # Interpolation.
        self.properties = None

        # The state of the statement we are executing. As this can be
        # shared between more than one object (in the case of a hide),
        # the data must not be altered.
        self.atl_state = None

        # Are we done?
        self.done = False

        # The transform event we are going to process.
        self.transform_event = None

        # The transform event we last processed.
        self.last_transform_event = None

        # The child transform event we last processed.
        self.last_child_transform_event = None

        # The child, without any transformations.
        self.raw_child = None

        # The parent transform that was called to create this transform.
        self.parent_transform = None

        # The offset between st and when this ATL block first executed.
        if renpy.config.atl_start_on_show:
            self.atl_st_offset = None
        else:
            self.atl_st_offset = 0

class RawStatement(object):

    constant = None

    def __init__(self, loc):
        super(RawStatement, self).__init__()
        self.loc = loc

# The base class for compiled ATL Statements.
class Statement(renpy.object.Object):

    def __init__(self, loc):
        super(Statement, self).__init__()
        self.loc = loc

# This represents a Raw ATL block.
class RawBlock(RawStatement):

    # Should we use the animation timebase or the showing timebase?
    animation = False

    def __init__(self, loc, statements, animation):
        super(RawBlock, self).__init__(loc)

        # A list of RawStatements in this block.
        self.statements = statements
        self.animation = animation

# A compiled ATL block.
class Block(Statement):

    def __init__(self, loc, statements):
        super(Block, self).__init__(loc)

        # A list of statements in the block.
        self.statements = statements

        # The start times of various statements.
        self.times = [ ]

        for i, s in enumerate(statements):
            if isinstance(s, Time):
                self.times.append((s.time, i + 1))

        self.times.sort()

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

    def __init__(self, loc):
        super(RawMultipurpose, self).__init__(loc)

        self.warper = None
        self.duration = None
        self.properties = [ ]
        self.expressions = [ ]
        self.splines = [ ]
        self.revolution = None
        self.circles = "0"

# This lets us have an ATL transform as our child.
class RawContainsExpr(RawStatement):

    def __init__(self, loc, expr):
        super(RawContainsExpr, self).__init__(loc)
        self.expression = expr

# This allows us to have multiple ATL transforms as children.
class RawChild(RawStatement):

    def __init__(self, loc, child):
        super(RawChild, self).__init__(loc)
        self.children = [ child ]

# This changes the child of this statement, optionally with a transition.
class Child(Statement):

    def __init__(self, loc, child, transition):
        super(Child, self).__init__(loc)

        self.child = child
        self.transition = transition

# This causes interpolation to occur.
class Interpolation(Statement):

    def __init__(self, loc, warper, duration, properties, revolution, circles, splines):
        super(Interpolation, self).__init__(loc)

        self.warper = warper
        self.duration = duration
        self.properties = properties
        self.splines = splines

        # The direction we revolve in: cw, ccw, or None.
        self.revolution = revolution

        # The number of complete circles we make.
        self.circles = circles

# Implementation of the repeat statement.
class RawRepeat(RawStatement):

    def __init__(self, loc, repeats):
        super(RawRepeat, self).__init__(loc)
        self.repeats = repeats

class Repeat(Statement):

    def __init__(self, loc, repeats):
        super(Repeat, self).__init__(loc)
        self.repeats = repeats

# Parallel statement.
class RawParallel(RawStatement):

    def __init__(self, loc, block):
        super(RawParallel, self).__init__(loc)
        self.blocks = [ block ]

class Parallel(Statement):

    def __init__(self, loc, blocks):
        super(Parallel, self).__init__(loc)
        self.blocks = blocks

# The choice statement.
class RawChoice(RawStatement):

    def __init__(self, loc, chance, block):
        super(RawChoice, self).__init__(loc)
        self.choices = [ (chance, block) ]

class Choice(Statement):

    def __init__(self, loc, choices):
        super(Choice, self).__init__(loc)
        self.choices = choices

# The Time statement.
class RawTime(RawStatement):

    def __init__(self, loc, time):
        super(RawTime, self).__init__(loc)
        self.time = time

class Time(Statement):

    def __init__(self, loc, time):
        super(Time, self).__init__(loc)
        self.time = time

# The On statement.
class RawOn(RawStatement):

    def __init__(self, loc, names, block):
        super(RawOn, self).__init__(loc)

        self.handlers = { }

        for i in names:
            self.handlers[i] = block

class On(Statement):

    def __init__(self, loc, handlers):
        super(On, self).__init__(loc)
        self.handlers = handlers

# Event statement.
class RawEvent(RawStatement):

    def __init__(self, loc, name):
        super(RawEvent, self).__init__(loc)
        self.name = name

class Event(Statement):

    def __init__(self, loc, name):
        super(Event, self).__init__(loc)
        self.name = name

class RawFunction(RawStatement):

    def __init__(self, loc, expr):
        super(RawFunction, self).__init__(loc)
        self.expr = expr

class Function(Statement):

    def __init__(self, loc, function):
        super(Function, self).__init__(loc)
        self.function = function
