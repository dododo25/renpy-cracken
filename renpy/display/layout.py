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

    def __init__(self, width=0, height=0, **properties):
        super(Null, self).__init__(**properties)
        self.width = width
        self.height = height

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

    # We indirect all list creation through this, so that we can
    # use RevertableLists if we want.
    _list_type = list

    def __init__(self, *args, **properties):
        self.children = self._list_type()
        self.child = None
        self.offsets = self._list_type()

        for i in args:
            self.add(i)

        super(Container, self).__init__(**properties)

class Position(Container):
    """
    :undocumented:

    Controls the placement of a displayable on the screen, using
    supplied position properties. This is the non-curried form of
    Position, which should be used when the user has directly created
    the displayable that will be shown on the screen.
    """

    def __init__(self, child, style='image_placement', **properties):
        """
        @param child: The child that is being laid out.

        @param style: The base style of this position.

        @param properties: Position properties that control where the
        child of this widget is placed.
        """

        super(Position, self).__init__(style=style, **properties)
        self.add(child)

class Grid(Container):
    """
    A grid is a widget that evenly allocates space to its children.
    The child widgets should not be greedy, but should instead be
    widgets that only use part of the space available to them.
    """

    allow_underfull = None

    def __init__(self, cols, rows, padding=None,
                 transpose=False,
                 style='grid',
                 allow_underfull=None,
                 **properties):
        """
        @param cols: The number of columns in this widget.

        @params rows: The number of rows in this widget.

        @params transpose: True if the grid should be transposed.

        @params allow_underfull: Controls if grid may be underfull.
        If None - uses config.allow_underfull_grids.
        """

        if padding is not None:
            properties.setdefault('spacing', padding)

        super(Grid, self).__init__(style=style, **properties)

        cols = int(cols)
        rows = int(rows)

        self.cols = cols
        self.rows = rows

        self.transpose = transpose
        self.allow_underfull = allow_underfull

class IgnoreLayers(Exception):
    """
    Raise this to have the event ignored by layers, but reach the
    underlay. This can also be used to stop processing focuses.
    """

    pass

class MultiBox(Container):

    layer_name = None
    first = True
    order_reverse = False
    layout = None

    def __init__(self, spacing=None, layout=None, style='default', **properties):

        if spacing is not None:
            properties['spacing'] = spacing

        super(MultiBox, self).__init__(style=style, **properties)

        self._clipping = self.style.clipping

        self.default_layout = layout

        # The start and animation times for children of this
        # box.
        self.start_times = [ ]
        self.anim_times = [ ]

        # A map from layer name to the widget corresponding to
        # that layer.
        self.layers = None

        # The same, but for the raw layers.
        self.raw_layers = None

        # The scene list for this widget.
        self.scene_list = None

class SizeGroup(renpy.object.Object):

    def __init__(self):
        super(SizeGroup, self).__init__()

        self.members = [ ]
        self._width = None
        self.computing_width = False

class Window(Container):
    """
    A window that has padding and margins, and can place a background
    behind its child. `child` is the child added to this
    displayable. All other properties are as for the :ref:`Window`
    screen language statement.
    """

    window_size = (0, 0)
    current_child = None

    def __init__(self, child=None, style='window', **properties):
        super(Window, self).__init__(style=style, **properties)

        if child is not None:
            self.add(child)

class DynamicDisplayable(renpy.display.core.Displayable):
    """
    :doc: disp_dynamic

    A displayable that can change its child based on a Python
    function, over the course of an interaction.

    `function`
        A function that is called with the arguments:

        * The amount of time the displayable has been shown for.
        * The amount of time any displayable with the same tag has been shown for.
        * Any positional or keyword arguments supplied to DynamicDisplayable.

        and should return a (d, redraw) tuple, where:

        * `d` is a displayable to show.
        * `redraw` is the maximum amount of time to wait before calling the
          function again, or None to not require the function be called again
          before the start of the next interaction.

        `function` is called at the start of every interaction.

    As a special case, `function` may also be a python string that evaluates
    to a displayable. In that case, function is run once per interaction.

    ::

        # Shows a countdown from 5 to 0, updating it every tenth of
        # a second until the time expires.
        init python:

            def show_countdown(st, at):
                if st > 5.0:
                    return Text("0.0"), None
                else:
                    d = Text("{:.1f}".format(5.0 - st))
                    return d, 0.1

        image countdown = DynamicDisplayable(show_countdown)
    """

    nosave = [ 'child' ]

    _duplicatable = True
    raw_child = None
    last_st = 0
    last_at = 0

    def __init__(self, function, *args, **kwargs):
        super(DynamicDisplayable, self).__init__()

        self.child = None

        if isinstance(function, basestring):
            args = (function,)
            kwargs = { }
            function = dynamic_displayable_compat

        self.predict_function = kwargs.pop("_predict_function", None)
        self.function = function
        self.args = args
        self.kwargs = kwargs

class IgnoresEvents(Container):

    def __init__(self, child, **properties):
        super(IgnoresEvents, self).__init__(**properties)
        self.add(child)

class Side(Container):

    possible_positions = set([ 'tl', 't', 'tr', 'r', 'br', 'b', 'bl', 'l', 'c'])

    def __init__(self, positions, style='side', **properties):
        super(Side, self).__init__(style=style, **properties)

        if isinstance(positions, basestring):
            positions = positions.split()

        seen = set()

        for i in positions:
            if not i in Side.possible_positions:
                raise Exception("Side used with impossible position '%s'." % (i,))

            if i in seen:
                raise Exception("Side used with duplicate position '%s'." % (i,))

            seen.add(i)

        self.positions = tuple(positions)
        self.sized = False

class Alpha(renpy.display.core.Displayable):

    def __init__(self, start, end, time, child=None, repeat=False, bounce=False,
                 anim_timebase=False, time_warp=None, **properties):
        super(Alpha, self).__init__(**properties)

        self.start = start
        self.end = end
        self.time = time
        self.child = renpy.easy.displayable(child)
        self.repeat = repeat
        self.anim_timebase = anim_timebase
        self.time_warp = time_warp

class AdjustTimes(Container):

    def __init__(self, child, start_time, anim_time, **properties):
        super(AdjustTimes, self).__init__(**properties)

        self.start_time = start_time
        self.anim_time = anim_time

        self.add(child)

class MatchTimes(Container):
    """
    A displayable that changes the `target` so that the times given to
    this target match the times this displayable was rendered at.

    `target`
        This must be an AdjustTimes displayable, that's a child of this
        MatchTimes displayable.
    """

    def __init__(self, child, target, **properties):
        super(MatchTimes, self).__init__(**properties)

        self.target = target

        self.add(child)

class Tile(Container):
    """
    :doc: disp_imagelike
    :name: Tile

    Tiles `child` until it fills the area allocated to this displayable.

    ::

        image bg tile = Tile("bg.png")

    """

    def __init__(self, child, style='tile', **properties):
        super(LiveTile, self).__init__(style=style, **properties)

        self.add(child)

class Flatten(Container):
    """
    :doc: disp_imagelike

    This flattens `child`, which may be made up of multiple textures, into
    a single texture.

    Certain operations, like the alpha transform property, apply to every
    texture making up a displayable, which can yield incorrect results
    when the textures overlap on screen. Flatten creates a single texture
    from multiple textures, which can prevent this problem.

    Flatten is a relatively expensive operation, and so should only be used
    when absolutely required.
    """

    def __init__(self, child, **properties):
        super(Flatten, self).__init__(**properties)

        self.add(child)

class AlphaMask(Container):
    """
    :doc: disp_imagelike

    This displayable takes its colors from `child`, and its alpha channel
    from the multiplication of the alpha channels of `child` and `mask`.
    The result is a displayable that has the same colors as `child`, is
    transparent where either `child` or `mask` is transparent, and is
    opaque where `child` and `mask` are both opaque.

    The `child` and `mask` parameters may be arbitrary displayables. The
    size of the AlphaMask is the size of `child`.

    Note that this takes different arguments from :func:`im.AlphaMask`,
    which uses the mask's red channel.
    """

    def __init__(self, child, mask, **properties):
        super(AlphaMask, self).__init__(**properties)

        self.mask = renpy.easy.displayable(mask)
        self.add(self.mask)
        self.add(child)
        self.null = None
