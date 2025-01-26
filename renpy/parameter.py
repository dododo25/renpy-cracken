
# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.object

class Parameter(object):
    """
    The default value (if any) of this class of parameters is a string,
    evaluable to the actual default value. This is how most Ren'Py callables
    work (labels, transforms directly defined using the transform statement,
    and screens), where the actual value is computed at the time of the call.
    """

    name = None

    """
    Accepted values:
    
    POSITIONAL_ONLY = 0\n
    POSITIONAL_OR_KEYWORD = 1\n
    VAR_POSITIONAL = 2\n
    KEYWORD_ONLY = 3\n
    VAR_KEYWORD = 4
    """
    kind = None

    default = None

class ValuedParameter(Parameter):
    """
    This is a more python-classic parameter, in which the default value is the
    final object itself, already evaluated.
    """

class Signature(object):
    """
    This class is used to store information about parameters (to a label, screen, ATL...)
    It has the same interface as inspect.Signature for the most part.
    """

    parameters = None

class ArgumentInfo(renpy.object.Object):

    __version__ = 1

    arguments             = None
    starred_indexes       = None
    doublestarred_indexes = None
