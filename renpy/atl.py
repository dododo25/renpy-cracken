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

class RawStatement(object):

    constant = None
    loc      = None

    def __setstate__(self, state):
        self.__dict__.update(state[1])

# This represents a Raw ATL block.
class RawBlock(RawStatement):

    # Should we use the animation timebase or the showing timebase?
    animation = False

    # A list of RawStatements in this block.
    statements = None

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

# This lets us have an ATL transform as our child.
class RawContainsExpr(RawStatement):

    expression = None

# This allows us to have multiple ATL transforms as children.
class RawChild(RawStatement):

    children = []

# Implementation of the repeat statement.
class RawRepeat(RawStatement):

    repeats = None

# Parallel statement.
class RawParallel(RawStatement):

    blocks = []

# The choice statement.
class RawChoice(RawStatement):

    choices = []

# The Time statement.
class RawTime(RawStatement):

    time = None

# The On statement.
class RawOn(RawStatement):

    handlers = {}

# Event statement.
class RawEvent(RawStatement):

    name = None

class RawFunction(RawStatement):

    expr = None
