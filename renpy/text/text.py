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

import math
import renpy.display.core
import renpy.display.behavior

class Blit(object):
    """
    Represents a blit command, which can be used to render a texture to a
    render. This is a rectangle with an associated alpha.
    """

    def __init__(self, x, y, w, h, alpha=1.0, left=False, right=False, top=False, bottom=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.alpha = alpha

        # True when the blit contains the left or right side of its row.
        self.left = left
        self.right = right

        # True when the blit is in the top or bottom row.
        self.top = top
        self.bottom = bottom

class DrawInfo(object):
    """
    This object is supplied as a parameter to the draw method of the various
    segments. It has the following fields:

    `surface`
        The surface to draw to.

    `override_color`
        If not None, a color that's used for this outline/shadow.

    `outline`
        The amount to outline the text by.

    `displayable_blits`
        If not none, this is a list of (displayable, xo, yo) tuples. The draw
        method adds displayable blits to this list when this is not None.
    """

    # No implementation, this is set up in the layout object.

class TextSegment(object):
    """
    This represents a segment of text that has a single set of properties
    applied to it.
    """

    def __init__(self, source=None):
        """
        Creates a new segment of text. If `source` is given, this starts off
        a copy of that source segment. Otherwise, it's up to the code that
        creates it to initialize it with defaults.
        """
        if source is not None:
            self.antialias = source.antialias
            self.vertical = source.vertical
            self.font = source.font
            self.size = source.size
            self.bold = source.bold
            self.italic = source.italic
            self.underline = source.underline
            self.strikethrough = source.strikethrough
            self.color = source.color
            self.black_color = source.black_color
            self.hyperlink = source.hyperlink
            self.kerning = source.kerning
            self.cps = source.cps
            self.ruby_top = source.ruby_top
            self.ruby_bottom = source.ruby_bottom
            self.hinting = source.hinting
            self.outline_color = source.outline_color
            self.ignore = source.ignore
        else:
            self.hyperlink = 0
            self.cps = 0
            self.ruby_top = False
            self.ruby_bottom = False
            self.ignore = False

class SpaceSegment(object):
    """
    A segment that's used to render horizontal or vertical whitespace.
    """

    def __init__(self, ts, width=0, height=0):
        """
        `ts`
            The text segment that this SpaceSegment follows.
        """
        #self.glyph = glyph = textsupport.Glyph()
        self.glyph = glyph = None

        glyph.character = 0
        glyph.ascent = 1
        glyph.line_spacing = height
        glyph.advance = width
        glyph.width = width

        if ts.hyperlink:
            glyph.hyperlink = ts.hyperlink

        self.cps = ts.cps

class DisplayableSegment(object):
    """
    A segment that's used to render displayables.
    """

    def __init__(self, ts, d, renders):
        """
        `ts`
            The text segment that this SpaceSegment follows.
        """
        self.d = d
        rend = renders[d]

        self.width, self.height = rend.get_size()

        if isinstance(d, renpy.display.behavior.CaretBlink):
            self.width = 0

        self.hyperlink = ts.hyperlink
        self.cps = ts.cps
        self.ruby_top = ts.ruby_top
        self.ruby_bottom = ts.ruby_bottom

class FlagSegment(object):
    """
    A do-nothing segment that just exists so we can flag the start and end
    of a run of text.
    """
    
    pass

class Layout(object):
    """
    Represents the layout of text.
    """

    def __init__(self, text, width, height, renders, size_only=False, splits_from=None, drawable_res=True):
        """
        `text`
            The text object this layout is associated with.

        `width`, `height`
            The height of the laid-out text.

        `renders`
            A map from displayable to its render.

        `size_only`
            If true, layout will stop once the size field is filled
            out. The object will only be suitable for sizing, as it
            will be missing the textures required to render it.

        `splits_from`
            If true, line-split information will be copied from this
            Layout (which must be another Layout of the same text).
        """

        def find_baseline():
            for g in all_glyphs:
                if g.ascent:
                    return g.y + self.yoffset

            return 0

        width = min(32767, width)
        height = min(32767, height)

        if drawable_res and (not size_only) and renpy.config.drawable_resolution_text:
            # How much do we want to oversample the text by, compared to the
            # virtual resolution.
            self.oversample = renpy.display.draw.draw_per_virt

            # Matrices to go from oversampled to virtual and vice versa.
            self.reverse = renpy.display.draw.draw_to_virt
            self.forward = renpy.display.draw.virt_to_draw

            self.outline_step = text.style.outline_scaling != "linear"
            self.pixel_perfect = True
        else:
            self.oversample = 1.0
            self.reverse = renpy.display.render.IDENTITY
            self.forward = renpy.display.render.IDENTITY
            self.outline_step = True

            self.pixel_perfect = False

        style = text.style

        self.line_overlap_split = self.scale_int(style.line_overlap_split)

        # Do we have any hyperlinks in this text? Set by segment.
        self.has_hyperlinks = False

        # Do we have any ruby in the text?
        self.has_ruby = False

        # Slow text that is not before the start segment is displayed
        # instantaneously. Text after the end segment is not displayed
        # at all. These are controlled by the {_start} and {_end} tags.
        self.start_segment = None
        self.end_segment = None

        # A list of paragraphs, represented as lists of the glyphs that
        # make up the paragraphs. This is used to copy break and timing
        # data from one Layout to another.
        self.paragraph_glyphs = [ ]

        # The virtual width and height offered to this Layout.
        self.width = width
        self.height = height

        width = self.scale_int(width)
        height = self.scale_int(height)

        # Figure out outlines and other info.
        outlines, xborder, yborder, xoffset, yoffset = self.figure_outlines(style)
        self.outlines = outlines
        self.xborder = xborder
        self.yborder = yborder
        self.xoffset = xoffset
        self.yoffset = yoffset

        # Adjust the borders by the outlines.
        width -= self.xborder
        height -= self.yborder

        # The greatest x coordinate of the text.
        maxx = 0

        # The current y, which becomes the maximum height once all paragraphs
        # have been rendered.
        y = 0

        # A list of glyphs - all the glyphs we know of.
        all_glyphs = [ ]

        # A list of (segment, glyph_list) pairs for all paragraphs.
        par_seg_glyphs = [ ]

        # A list of Line objects.
        lines = [ ]

        # The time at which the next glyph will be displayed.
        gt = 0.0

        # 2. Breaks the text into a list of paragraphs, where each paragraph is
        # represented as a list of (Segment, text string) tuples.
        #
        # This takes information from the various styles that apply to the text,
        # and so needs to be redone when the style of the text changes.

        if splits_from:
            self.paragraphs = splits_from.paragraphs
            self.start_segment = splits_from.start_segment
            self.end_segment = splits_from.end_segment
            self.has_hyperlinks = splits_from.has_hyperlinks
            self.hyperlink_targets = splits_from.hyperlink_targets
            self.has_ruby = splits_from.has_ruby
        else:
            self.paragraphs = self.segment(text.tokens, style, renders, text)

        first_indent = self.scale_int(style.first_indent)
        rest_indent = self.scale_int(style.rest_indent)

        # True if we've encountered the start and end segments respectively
        # while assigning times.
        started = self.start_segment is None
        ended = False

        for p_num, p in enumerate(self.paragraphs):

            # RTL - apply RTL to the text of each segment, then
            # reverse the order of the segments in each paragraph.
            if renpy.config.rtl:
                p, rtl = self.rtl_paragraph(p)
            else:
                rtl = False

            # 3. Convert each paragraph into a Segment, glyph list. (Store this
            # to use when we draw things.)

            # A list of glyphs in the paragraph.
            par_glyphs = [ ]

            # A list of (segment, list of glyph) pairs.
            seg_glyphs = [ ]

            for ts, s in p:
                glyphs = ts.glyphs(s, self)

                t = (ts, glyphs)
                seg_glyphs.append(t)
                par_seg_glyphs.append(t)
                par_glyphs.extend(glyphs)
                all_glyphs.extend(glyphs)

            # RTL - Reverse each line, segment, so that we can use LTR
            # linebreaking algorithms.
            if rtl:
                par_glyphs.reverse()
                for ts, glyphs in seg_glyphs:
                    glyphs.reverse()

            self.paragraph_glyphs.append(list(par_glyphs))

        line_spacing = self.scale_int(style.line_spacing)

        if style.line_spacing < 0:
            if renpy.config.broken_line_spacing:
                y += -line_spacing * len(lines)
            else:
                y += -line_spacing

            lines[-1].height = y - lines[-1].y

        min_width = self.scale_int(style.min_width)
        if min_width > maxx + self.xborder:
            maxx = min_width - self.xborder

        maxx = math.ceil(maxx)

        adjust_spacing = text.style.adjust_spacing

        if splits_from and adjust_spacing:

            target_x = self.scale_int(splits_from.size[0] - splits_from.xborder)
            target_y = self.scale_int(splits_from.size[1] - splits_from.yborder)

            target_x_delta = target_x - maxx
            target_y_delta = target_y - y

            if adjust_spacing == "horizontal":
                target_y_delta = 0.0
            elif adjust_spacing == "vertical":
                target_x_delta = 0.0

            maxx = target_x
            y = target_y

        # Figure out the size of the texture. (This is a little over-sized,
        # but it simplifies the code to not have to care about borders on a
        # per-outline basis.)
        sw, sh = size = (maxx + self.xborder, y + self.yborder)
        self.size = size

        self.baseline = find_baseline()

        # If we only care about the size, we're done.
        if size_only:
            return

        # Check for glyphs that are being drawn out of bounds, because the font
        # or anti-aliasing or whatever makes them bigger than the bounding box. If
        # we have them, grow the bounding box.

        bounds = (0, 0, maxx, y)
        for ts, glyphs in par_seg_glyphs:
            bounds = ts.bounds(glyphs, bounds, self)

        self.add_left = max(-bounds[0], 0)
        self.add_top = max(-bounds[1], 0)
        self.add_right = max(bounds[2] - maxx, 0)
        self.add_bottom = max(bounds[3] - y, 0)

        sw += self.add_left + self.add_right
        sh += self.add_top + self.add_bottom

        # A map from (outline, color) to a texture.
        self.textures = { }

        di = DrawInfo()

        for o, color, _xo, _yo in self.outlines:
            key = (o, color)

            if key in self.textures:
                continue

            if color == None:
                self.displayable_blits = [ ]
                di.displayable_blits = self.displayable_blits
            else:
                di.displayable_blits = None

            # Create the texture.

            tw = int(sw + o)
            th = int(sh + o)

            # If not a multiple of 32, round up.
            tw = (tw | 0x1f) + 1 if (tw & 0x1f) else tw
            th = (th | 0x1f) + 1 if (th & 0x1f) else th

            surf = renpy.display.pgrender.surface((tw, th), True)

            if renpy.game.preferences.high_contrast:
                if color:
                    surf.fill(color)
                else:
                    prefix = style.prefix
                    prefix_color = style.color
                    style.set_prefix("idle_")
                    idle_color = style.color
                    style.set_prefix(prefix)

                    color = (255, 255, 255, 255)

                    if idle_color != prefix_color:
                        if "hover" in prefix:
                            color = (255, 255, 224, 255)
                        elif "selected" in style.prefix:
                            color = (224, 255, 255, 255)

            di.surface = surf
            di.override_color = color
            di.outline = o

            for ts, glyphs in par_seg_glyphs:
                if ts is self.end_segment:
                    break

                ts.draw(glyphs, di, self.add_left, self.add_top, self)

        # Store the lines, so we have them for typeout.
        self.lines = lines

class Text(renpy.display.core.Displayable):

    """
    :name: Text
    :doc: text
    :args: (text, slow=None, scope=None, substitute=None, slow_done=None, mipmap=None, **properties)

    A displayable that displays text on the screen.

    `text`
        The text to display on the screen. This may be a string, or a list of
        strings and displayables.

    `slow`
        Determines if the text is displayed slowly, being typed out one character at the time.
        If None, slow text mode is determined by the :propref:`slow_cps` style property. Otherwise,
        the truth value of this parameter determines if slow text mode is used.

    `scope`
        If not None, this should be a dictionary that provides an additional scope for text
        interpolation to occur in.

    `substitute`
        If true, text interpolation occurs. If false, it will not occur. If
        None, they are controlled by :var:`config.new_substitutions`.
    """

    __version__ = 4

    _uses_scope = True
    _duplicatable = False
    locked = False

    language = None
    mask = None
    last_ctc = None

    def __init__(self, text, slow=None, scope=None, substitute=None, slow_done=None, replaces=None, mask=None, **properties):
        super(Text, self).__init__(**properties)

        # We need text to be a list, so if it's not, wrap it.
        if not isinstance(text, list):
            text = [ text ]

        # Check that the text is all text-able things.
        for i in text:
            if not isinstance(i, (basestring, renpy.display.core.Displayable)):
                if renpy.config.developer:
                    raise Exception("Cannot display {0!r} as text.".format(i))
                else:
                    text = [ "" ]
                    break

        # True if we are substituting things in.
        self.substitute = substitute

        # Do we need to update ourselves?
        self.dirty = True

        # The text, after substitutions.
        self.text = None

        # A mask, for passwords and such.
        self.mask = mask

        # Sets the text we're showing, and performs substitutions.
        self.set_text(text, scope, substitute)

        if renpy.game.less_updates or renpy.game.preferences.self_voicing:
            slow = False

        # True if we're using slow text mode.
        self.slow = slow

        # The callback to be called when slow-text mode ends.
        self.slow_done = None

        # The ctc indicator associated with this text.
        self.ctc = None

        # The index of the start and end strings in the first segment of text.
        # (None to show the whole text.)
        self.start = None
        self.end = None

        if isinstance(replaces, Text):
            self.slow = replaces.slow
            self.slow_done = replaces.slow_done
            self.ctc = replaces.ctc
            self.start = replaces.start
            self.end = replaces.end

        # The list of displayables we use.
        self.displayables = None

        self._duplicatable = self.slow

        # The list of displayables and their offsets.
        self.displayable_offsets = [ ]
