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

# This file contains code that handles the execution of python code
# contained within the script file. It also handles rolling back the
# game state to some time in the past.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

##############################################################################
# Code that implements the store.

class RevertableList(list):

    def __init__(self, *args):
        list.__init__(self, *args)

class RevertableDict(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

class RevertableSet(set):

    def __setstate__(self, state):
        if isinstance(state, tuple):
            self.update(state[0].keys())
        else:
            self.update(state)

    def __init__(self, *args):
        set.__init__(self, *args)

class RevertableObject(object):

    pass

class AlwaysRollback(RevertableObject):
    """
    This is a revertible object that always participates in rollback.
    It's used when a revertable object is created by an object that
    doesn't participate in the rollback system.
    """

    pass
