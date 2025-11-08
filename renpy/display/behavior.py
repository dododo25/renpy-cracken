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

# This contains various Displayables that handle events.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import renpy.display.core
import renpy.display.layout
import renpy.python

##############################################################################
# Button

class Button(renpy.display.layout.Window):

    keymap           = {}
    action           = None
    alternate        = None
    longpress_start  = None
    longpress_x      = None
    longpress_y      = None
    role_parameter   = None
    keysym           = None
    alternate_keysym = None
    locked           = False
    selected         = None
    sensitive        = None
    clicked          = None
    hovered          = None
    unhovered        = None
    focusable        = True
    role_parameter   = None
    time_policy_data = None
    _duplicatable    = False

# Reimplementation of the TextButton widget as a Button and a Text
# widget.

class ImageButton(Button):
    """
    Used to implement the guts of an image button.
    """

    state_children = None

class TimerState(renpy.python.AlwaysRollback):
    """
    Stores the state of the timer, which may need to be rolled back.
    """

    started = False
    next_event = None

class Timer(renpy.display.layout.Null):

    __version__ = 1

    started    = False
    delay      = None
    repeat     = None
    next_event = None
    function   = None
    args       = None
    kwargs     = None
    started    = False
    state      = None

class MouseArea(renpy.display.core.Displayable):

    # The offset between st and at.
    at_st_offset = 0

class OnEvent(renpy.display.core.Displayable):
    """
    This is a displayable that runs an action in response to a transform
    event. It's used to implement the screen language on statement.
    """

    event_name = None
    action     = None

class Input(renpy.text.text.Text):  # @UndefinedVariable
    """
    This is a Displayable that takes text as input.
    """

    changed = None
    prefix = None
    suffix = None
    caret_pos = 0
    old_caret_pos = 0
    pixel_width = None
    default = None
    edit_text = None
    value = None
