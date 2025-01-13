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

        if renpy.game.context().init_phase:
            compile_queue.append(self)

    def _handles_event(self, event):

        if (event == "replaced") and (self.atl_state is None):
            return True

        if (self.block is not None) and (self.block._handles_event(event)):
            return True

        if self.child is None:
            return False

        return self.child._handles_event(event)

    def get_block(self):
        """
        Returns the compiled block to use.
        """

        if self.block:
            return self.block
        elif self.predict_block and renpy.display.predict.predicting:
            return self.predict_block
        else:
            return None

    def take_execution_state(self, t):
        """
        Updates self to begin executing from the same point as t. This
        requires that t.atl is self.atl.
        """

        super(ATLTransformBase, self).take_execution_state(t)

        self.atl_st_offset = None
        self.atl_state = None

        if self is t:
            return
        elif not isinstance(t, ATLTransformBase):
            return
        elif t.atl is not self.atl:
            return

        # Important to do it this way, so we use __eq__. The exception handling
        # optimistically assumes that uncomparable objects are the same.
        try:
            if not (t.context == self.context):
                return
        except:
            pass

        self.done = t.done
        self.block = t.block
        self.atl_state = t.atl_state
        self.transform_event = t.transform_event
        self.last_transform_event = t.last_transform_event
        self.last_child_transform_event = t.last_child_transform_event

        self.st = t.st
        self.at = t.at
        self.st_offset = t.st_offset
        self.at_offset = t.at_offset
        self.atl_st_offset = t.atl_st_offset

        if self.child is renpy.display.motion.null:

            if t.child and t.child._duplicatable:
                self.child = t.child._duplicate(None)
            else:
                self.child = t.child

            self.raw_child = t.raw_child

    def __call__(self, *args, **kwargs):

        _args = kwargs.pop("_args", None)

        context = self.context.context.copy()

        for k, v in self.parameters.parameters:
            if v is not None:
                context[k] = renpy.python.py_eval(v)

        positional = list(self.parameters.positional)
        args = list(args)

        child = None

        if not positional and args:
            child = args.pop(0)

        # Handle positional arguments.
        while positional and args:
            name = positional.pop(0)
            value = args.pop(0)

            if name in kwargs:
                raise Exception('Parameter %r is used as both a positional and keyword argument to a transition.' % name)

            context[name] = value

        if args:
            raise Exception("Too many arguments passed to ATL transform.")

        # Handle keyword arguments.
        for k, v in kwargs.items():

            if k in positional:
                positional.remove(k)
                context[k] = v
            elif k in context:
                context[k] = v
            elif k == 'child':
                child = v
            else:
                raise Exception('Parameter %r is not known by ATL Transform.' % k)

        if child is None:
            child = self.child

        # Create a new ATL Transform.
        parameters = renpy.ast.ParameterInfo({ }, positional, None, None)

        rv = renpy.display.motion.ATLTransform(
            atl=self.atl,
            child=child,
            style=self.style_arg,
            context=context,
            parameters=parameters,
            _args=_args,
            )

        rv.parent_transform = self
        rv.take_state(self)

        return rv

    def compile(self): # @ReservedAssignment
        """
        Compiles the ATL code into a block. As necessary, updates the
        properties.
        """

        constant = (self.atl.constant == GLOBAL_CONST)

        if not constant:
            for p in self.parameters.positional:
                if p not in self.context.context:
                    raise Exception("Cannot compile ATL Transform at %s:%d, as it's missing positional parameter %s." % (
                        self.atl.loc[0],
                        self.atl.loc[1],
                        self.parameters.positional[0],
                        ))

        if constant and self.parent_transform:
            if self.parent_transform.block:
                self.block = self.parent_transform.block
                self.properties = self.parent_transform.properties
                self.parent_transform = None
                return self.block

        old_exception_info = renpy.game.exception_info

        block = self.atl.compile(self.context)

        if all(
            isinstance(statement, Interpolation) and statement.duration == 0
            for statement in block.statements
        ):
            self.properties = []
            for interp in block.statements:
                self.properties.extend(interp.properties)

        if not constant and renpy.display.predict.predicting:
            self.predict_block = block
        else:
            self.block = block
            self.predict_block = None

        renpy.game.exception_info = old_exception_info

        if constant and self.parent_transform:
            self.parent_transform.block = self.block
            self.parent_transform.properties = self.properties
            self.parent_transform = None

        return block

    def execute(self, trans, st, at):

        if self.done:
            return None

        block = self.get_block()
        if block is None:
            block = self.compile()

        events = [ ]

        # Hide request.
        if trans.hide_request:
            self.transform_event = "hide"

        if trans.replaced_request:
            self.transform_event = "replaced"

        # Notice transform events.
        if renpy.config.atl_multiple_events:
            if self.transform_event != self.last_transform_event:
                events.append(self.transform_event)
                self.last_transform_event = self.transform_event

        # Propagate transform_events from children.
        if (self.child is not None) and self.child.transform_event != self.last_child_transform_event:
            self.last_child_transform_event = self.child.transform_event

            if self.child.transform_event is not None:
                self.transform_event = self.child.transform_event

        # Notice transform events, again.
        if self.transform_event != self.last_transform_event:
            events.append(self.transform_event)
            self.last_transform_event = self.transform_event

        if self.transform_event in renpy.config.repeat_transform_events:
            self.transform_event = None
            self.last_transform_event = None

        old_exception_info = renpy.game.exception_info

        if (self.atl_st_offset is None) or (st - self.atl_st_offset) < 0:
            self.atl_st_offset = st

        if self.atl.animation:
            timebase = at
        else:
            timebase = st - self.atl_st_offset

        action, arg, pause = block.execute(trans, timebase, self.atl_state, events)

        renpy.game.exception_info = old_exception_info

        if action == "continue" and not renpy.display.predict.predicting:
            self.atl_state = arg
        else:
            self.done = True

        return pause

    def predict_one(self):
        self.atl.predict(self.context)

    def visit(self):
        block = self.get_block()

        if block is None:
            block = self.compile()

        return self.children + block.visit()

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
