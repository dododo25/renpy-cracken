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

# This file contains functions that can be used to display a UI on the
# screen.  The UI isn't implemented here (rather, in
# renpy.display). Instead, these functions provide a simple interface
# that allows a user to procedurally create a UI.

# All functions in the is file should be documented in the wiki.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import renpy.object

_key = None

##############################################################################
# Special classes that can be subclassed from the outside.

class Action(renpy.object.Object):
    """
    This can be passed to the clicked method of a button or hotspot. It is
    called when the action is selected. The other methods determine if the
    action should be displayed insensitive or disabled.
    """

    # Alt text.
    alt = None

class BarValue(renpy.object.Object):
    """
    This can be passed to the value method of bar and hotbar.
    """

    # Alt text.
    alt = "Bar"

    force_step = False

##############################################################################
# Things we can add to. These have two methods: add is called with the
# widget we're adding. close is called when the thing is ready to be
# closed.

class Addable(object):
    # A style_prefix associates with this addable.
    style_prefix = None

class Layer(Addable):

    name = None

class Many(Addable):
    """
    A widget that takes many children.
    """

    displayable  = None
    imagemap     = None
    style_prefix = None

class One(Addable):
    """
    A widget that expects exactly one child.
    """

    displayable  = None
    style_prefix = None

class Detached(Addable):
    """
    Used to indicate a widget is detached from the stack.
    """

    style_prefix = None

class ChildOrFixed(Addable):
    """
    If one widget is added, then it is added directly to our
    parent. Otherwise, a fixed is added to our parent, and all
    the widgets are added to that.
    """

    queue = []
    style_prefix = None

class Wrapper(renpy.object.Object):

    name     = None
    function = None
    one      = False
    many     = False
    imagemap = False
    replaces = False
    style    = None
    kwargs   = None
    style    = None

class ChoiceActionBase(Action):
    """
    Base class for choice actions. The choice is identified by a label
    and value. The class will automatically determine the rollback state
    and supply correct "sensitive" and "selected" information to the
    widget.
    If a location is supplied, it will check whether the choice was
    previously visited and mark it so if it is chosen.
    """

    sensitive = True
    label     = None
    value     = None
    location  = None
    sensitive = None
    block_all = None
    args      = None
    kwargs    = None

class ChoiceReturn(ChoiceActionBase):
    """
    :doc: blockrollback

    A menu choice action that returns `value`, while managing the button
    state in a manner consistent with fixed rollback. (See block_all for
    a description of the behavior.)


    `label`
        The label text of the button. For imagebuttons and hotspots this
        can be anything. This label is used as a unique identifier of
        the options within the current screen. Together with `location`
        it is used to store whether this option has been chosen.

    `value`
        The value this is returned when the choice is chosen.

    `location`
        A unique location identifier for the current choices screen.

    `block_all`
        If false, the button is given the selected role if it was
        the chosen choice, and insensitive if it was not selected.

        If true, the button is always insensitive during fixed
        rollback.

        If None, the value is taken from the :var:`config.fix_rollback_without_choice`
        variable.

        When true is given to all items in a screen, it will
        become unclickable (rolling forward will still work). This can
        be changed by calling :func:`ui.saybehavior` before the call
        to :func:`ui.interact`.
    """

class ChoiceJump(ChoiceActionBase):
    """
    :doc: blockrollback

    A menu choice action that returns `value`, while managing the button
    state in a manner consistent with fixed rollback. (See block_all for
    a description of the behavior.)


    `label`
        The label text of the button. For imagebuttons and hotspots this
        can be anything. This label is used as a unique identifier of
        the options within the current screen. Together with `location`
        it is used to store whether this option has been chosen.

    `value`
        The location to jump to.

    `location`
        A unique location identifier for the current choices screen.

    `block_all`
        If false, the button is given the selected role if it was
        the chosen choice, and insensitive if it was not selected.

        If true, the button is always insensitive during fixed
        rollback.

        If None, the value is taken from the :var:`config.fix_rollback_without_choice`
        variable.

        When true is given to all items in a screen, it will
        become unclickable (rolling forward will still work). This can
        be changed by calling :func:`ui.saybehavior` before the call
        to :func:`ui.interact`.
    """

class Imagemap(object):
    """
    Stores information about the images used by an imagemap.
    """

    alpha                = True
    cache_param          = True
    insensitive          = None
    idle                 = None
    selected_idle        = None
    hover                = None
    selected_hover       = None
    selected_insensitive = None
    alpha                = None
    cache_param          = None
    cache                = None
