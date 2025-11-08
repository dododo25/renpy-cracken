# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains displayables that move, zoom, rotate, or otherwise
# transform displayables. (As well as displayables that support them.)
import renpy.object

from renpy.display.layout import Container

class TransformState(renpy.object.Object):

    nearest = None
    xoffset = None
    yoffset = None
    inherited_xpos = None
    inherited_ypos = None
    inherited_xanchor = None
    inherited_yanchor = None
    transform_anchor = False
    additive = 0.0
    debug = None
    events = True
    crop_relative = False
    xpan = None
    ypan = None
    xtile = 1
    ytile = 1
    last_angle = None

class Transform(Container):
    """
    Documented in sphinx, because we can't scan this object.
    """

    __version__ = None
    transform_event_responder = True

    # Proxying things over to our state.
    nearest = None
    alpha = None
    additive = None
    rotate = None
    rotate_pad = None
    transform_anchor = None
    zoom = None
    xzoom = None
    yzoom = None

    xpos = None
    ypos = None
    xanchor = None
    yanchor = None

    xalign = None
    yalign = None

    around = None
    alignaround = None
    angle = None
    radius = None

    xaround = None
    yaround = None
    xanchoraround = None
    yanchoraround = None

    pos = None
    anchor = None
    align = None

    crop = None
    crop_relative = None
    corner1 = None
    corner2 = None
    size = None

    delay = None

    xoffset = None
    yoffset = None
    offset = None

    subpixel = None

    xcenter = None
    ycenter = None

    xpan = None
    ypan = None

    xtile = None
    ytile = None

    debug = None
    events = None

    # Compatibility with old versions of the class.
    active = False
    children = False
    arguments = None

    # Default before we set this.
    child_size = None

class ATLTransform(renpy.atl.ATLTransformBase, Transform):
    pass
