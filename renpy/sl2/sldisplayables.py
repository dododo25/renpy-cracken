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

##############################################################################
# Definitions of screen language statements.

from __future__ import print_function

import renpy.display.layout

sl2add = None

class ShowIf(renpy.display.layout.Container):
    """
    This is a displayable that wraps displayables that are
    underneath a showif statement.
    """

    def __init__(self, condition, replaces=None):
        super(ShowIf, self).__init__()

        self.condition = condition

        if replaces is None:
            if condition:
                self.pending_event = "appear"
            else:
                self.pending_event = None

            self.show_child = condition
        else:
            if self.condition and not replaces.condition:
                self.pending_event = "show"
            elif not self.condition and replaces.condition:
                self.pending_event = "hide"
            else:
                self.pending_event = replaces.pending_event

            self.show_child = replaces.show_child
