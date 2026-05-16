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

# This file contains code for initializing and managing the display
# window.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import renpy.object

class DisplayableArguments(renpy.object.Object):
    """
    Represents a set of arguments that can be passed to a duplicated
    displayable.
    """

    # The name of the displayable without any arguments.
    name = ()

    # Arguments supplied.
    args = ()

    # The style prefix in play. This is used by DynamicImage to figure
    # out the prefix list to apply.
    prefix = None

    # True if lint is in use.
    lint = False

    def __setstate__(self, new_dict):
        super().__setstate__(new_dict)

class Displayable(renpy.object.Object):
    """
    The base class for every object in Ren'Py that can be
    displayed to the screen.

    Drawables will be serialized to a savegame file. Therefore, they
    shouldn't store non-serializable things (like pygame surfaces) in
    their fields.
    """

    # Some invariants about method call order:
    #
    # per_interact is called before render.
    # render is called before event.
    #
    # get_placement can be called at any time, so can't
    # assume anything.

    # If True this displayable can accept focus.
    # If False, it can't, but it keeps its place in the focus order.
    # If None, it does not have a place in the focus order.
    focusable = None

    # This is the focus named assigned by the focus code.
    full_focus_name = None

    # A role ('selected_' or '' that prefixes the style).
    role = ''

    # The event we'll pass on to our parent transform.
    transform_event = None

    # Can we change our look in response to transform_events?
    transform_event_responder = False

    # The main displayable, if this displayable is the root of a composite
    # displayable. (This is used by SL to figure out where to add children
    # to.) If None, it is itself.
    _main = None

    # A list of the children that make up this composite displayable.
    _composite_parts = []

    # The location the displayable was created at, if known.
    _location = None

    # Does this displayable use the scope?
    _uses_scope = False

    # Arguments supplied to this displayable.
    _args = DisplayableArguments()

    # Set to true of the displayable is duplicatable (has a non-trivial
    # duplicate method), or one of its children is.
    _duplicatable = False

    # Does this displayable require clipping?
    _clipping = False

    # Does this displayable have a tooltip?
    _tooltip = None

    style = None
    focus_name = None
    default = None

    def __setstate__(self, new_dict):
        super().__setstate__(new_dict)