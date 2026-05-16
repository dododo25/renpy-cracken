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

# This file contains classes that handle layout of displayables on
# the screen.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import renpy.display.core

class Null(renpy.display.core.Displayable):
    """
    :doc: disp_imagelike
    :name: Null

    A displayable that creates an empty box on the screen. The size
    of the box is controlled by `width` and `height`. This can be used
    when a displayable requires a child, but no child is suitable, or
    as a spacer inside a box.

    ::

        image logo spaced = HBox("logo.png", Null(width=100), "logo.png")

    """

    width  = None
    height = None

    def __setstate__(self, new_dict):
        super().__setstate__(new_dict)

class Container(renpy.display.core.Displayable):
    """
    This is the base class for containers that can have one or more
    children.

    @ivar children: A list giving the children that have been added to
    this container, in the order that they were added in.

    @ivar child: The last child added to this container. This is also
    used to access the sole child in containers that can only hold
    one child.

    @ivar offsets: A list giving offsets for each of our children.
    It's expected that render will set this up each time it is called.

    @ivar sizes: A list giving sizes for each of our children. It's
    also expected that render will set this each time it is called.

    """

    children = None
    child    = None
    offsets  = None

class Window(Container):
    """
    A window that has padding and margins, and can place a background
    behind its child. `child` is the child added to this
    displayable. All other properties are as for the :ref:`Window`
    screen language statement.
    """

    window_size = (0, 0)
    current_child = None

class MultiBox(Container):

    layer_name     = None
    first          = None
    order_reverse  = None
    layout         = None
    default_layout = None
    start_times    = None
    anim_times     = None
    layers         = None
    raw_layers     = None
    scene_list     = None

class Grid(Container):
    """
    A grid is a widget that evenly allocates space to its children.
    The child widgets should not be greedy, but should instead be
    widgets that only use part of the space available to them.
    """

    allow_underfull = None
    rows            = None
    cols            = None
    transpose       = None
    allow_underfull = None

class Side(Container):

    possible_positions = set([ 'tl', 't', 'tr', 'r', 'br', 'b', 'bl', 'l', 'c'])

    positions = None
    sized     = False
