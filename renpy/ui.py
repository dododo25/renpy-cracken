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

import renpy.object

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

    def __init__(self, name):
        self.name = name

class Many(Addable):
    """
    A widget that takes many children.
    """

    def __init__(self, displayable, imagemap, style_prefix):
        self.displayable = displayable
        self.imagemap = imagemap
        self.style_prefix = style_prefix

class One(Addable):
    """
    A widget that expects exactly one child.
    """

    def __init__(self, displayable, style_prefix):
        self.displayable = displayable
        self.style_prefix = style_prefix

class Detached(Addable):
    """
    Used to indicate a widget is detached from the stack.
    """

    def __init__(self, style_prefix):
        self.style_prefix = style_prefix

class ChildOrFixed(Addable):
    """
    If one widget is added, then it is added directly to our
    parent. Otherwise, a fixed is added to our parent, and all
    the widgets are added to that.
    """

    def __init__(self, style_prefix):
        self.queue = [ ]
        self.style_prefix = style_prefix

class Wrapper(renpy.object.Object):

    def __init__(self, function, one=False, many=False, imagemap=False, replaces=False, style=None, **kwargs):
        # The name assigned to this wrapper. This is used to serialize us correctly.
        self.name = None

        # The function to call.
        self.function = function

        # Should we add one or many things to this wrapper?
        self.one = one
        self.many = many or imagemap
        self.imagemap = imagemap

        # Should the function be given the replaces parameter,
        # specifiying the displayable it replaced?
        self.replaces = replaces

        # Default keyword arguments to the function.
        self.kwargs = kwargs

        # Default style (suffix).
        self.style = style

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

    def __init__(self, label, value, location=None, block_all=None, sensitive=True, args=None, kwargs=None):
        self.label = label
        self.value = value
        self.location = location
        self.sensitive = sensitive

        if block_all is None:
            self.block_all = renpy.config.fix_rollback_without_choice
        else:
            self.block_all = block_all

        # The arguments passed to a menu choice.
        self.args = args
        self.kwargs = kwargs

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

    alpha = True
    cache_param = True

    def __init__(self, insensitive, idle, selected_idle, hover, selected_hover, selected_insensitive, alpha, cache):
        self.insensitive = renpy.easy.displayable(insensitive)
        self.idle = renpy.easy.displayable(idle)
        self.selected_idle = renpy.easy.displayable(selected_idle)
        self.hover = renpy.easy.displayable(hover)
        self.selected_hover = renpy.easy.displayable(selected_hover)
        self.selected_insensitive = renpy.easy.displayable(selected_insensitive)

        self.alpha = alpha

        self.cache_param = cache
        self.cache = renpy.display.imagemap.ImageMapCache(cache)