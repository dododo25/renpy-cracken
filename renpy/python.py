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

import random
import renpy.object

##############################################################################
# Code that implements the store.

# Deleted is a singleton object that's used to represent an object that has
# been deleted from the store.
class StoreDeleted(object):

    pass

class StoreModule(object):
    """
    This class represents one of the modules containing the store of data.
    """

    # Set our dict to be the StoreDict. Then proxy over setattr and delattr,
    # since Python won't call them by default.

    def __init__(self, d):
        object.__setattr__(self, "__dict__", d)

class StoreDict(dict):
    """
    This class represents the dictionary of a store module. It logs
    sets and deletes.
    """

    def __init__(self):
        # The value of this dictionary at the start of the current
        # rollback period (when begin() was last called).
        self.old = None

        # The set of variables in this StoreDict that changed since the
        # end of the init phase.
        self.ever_been_changed = set()

class StoreBackup():
    """
    This creates a copy of the current store, as it was at the start of
    the current statement.
    """

    def __init__(self):
        # The contents of the store for each store.
        self.store = { }

        # The contents of old for each store.
        self.old = { }

        # The contents of ever_been_changed for each store.
        self.ever_been_changed = { }

# Code that computes reachable objects, which is used to filter
# the rollback list before rollback or serialization.
class NoRollback(object):
    """
    :doc: norollback class

    Instances of classes inheriting from this class do not participate in
    rollback. Objects reachable through an instance of a NoRollback class
    only participate in rollback if they are reachable through other paths.
    """

    pass

class CompressedList(object):
    """
    Compresses the changes in a queue-like list. What this does is to try
    to find a central sub-list for which has objects in both lists. It
    stores the location of that in the new list, and then elements before
    and after in the sub-list.

    This only really works if the objects in the list are unique, but the
    results are efficient even if this doesn't work.
    """

    def __init__(self, old, new):
        # Pick out a pivot element near the center of the list.
        new_center = (len(new) - 1) // 2
        new_pivot = new[new_center]

        # Find an element in the old list corresponding to the pivot.
        old_half = (len(old) - 1) // 2

        for i in range(0, old_half + 1):
            if old[old_half - i] is new_pivot:
                old_center = old_half - i
                break

            if old[old_half + i] is new_pivot:
                old_center = old_half + i
                break
        else:
            # If we couldn't, give up.
            self.pre = old
            self.start = 0
            self.end = 0
            self.post = [ ]

            return

        # Figure out the position of the overlap in the center of the two lists.
        new_start = new_center
        new_end = new_center + 1

        old_start = old_center
        old_end = old_center + 1

        len_new = len(new)
        len_old = len(old)

        while new_start and old_start and (new[new_start - 1] is old[old_start - 1]):
            new_start -= 1
            old_start -= 1

        while (new_end < len_new) and (old_end < len_old) and (new[new_end] is old[old_end]):
            new_end += 1
            old_end += 1

        # Now that we have this, we can put together the object.
        self.pre = list.__getitem__(old, slice(0, old_start))
        self.start = new_start
        self.end = new_end
        self.post = list.__getitem__(old, slice(old_end, len_old))

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

    def __getstate__(self):
        rv = ({ i : True for i in self},)
        return rv

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

class RollbackRandom(random.Random):
    """
    This is used for Random objects returned by renpy.random.Random.
    """

    pass

class DetRandom(random.Random):
    """
    This is renpy.random.
    """

    def __init__(self):
        super(DetRandom, self).__init__()
        self.stack = [ ]

class Rollback(renpy.object.Object):
    """
    Allows the state of the game to be rolled back to the point just
    before a node began executing.

    @ivar context: A shallow copy of the context we were in before
    we started executing the node. (Shallow copy also includes
    a copy of the associated SceneList.)

    @ivar objects: A list of tuples, each containing an object and a
    token of information that, when passed to the rollback method on
    that object, causes that object to rollback.

    @ivar store: A list of updates to store that will cause the state
    of the store to be rolled back to the start of node
    execution. This is a list of tuples, either (key, value) tuples
    representing a value that needs to be assigned to a key, or (key,)
    tuples that mean the key should be deleted.

    @ivar checkpoint: True if this is a user-visible checkpoint,
    false otherwise.

    @ivar purged: True if purge_unreachable has already been called on
    this Rollback, False otherwise.

    @ivar random: A list of random numbers that were generated during the
    execution of this element.
    """

    __version__ = 5

    identifier = None
    not_greedy = False

    def __init__(self):
        super(Rollback, self).__init__()

        self.context = None

        self.objects = [ ]
        self.purged = False
        self.random = [ ]
        self.forward = None

        # A map of maps name -> (variable -> value)
        self.stores = { }

        # A map from store name to the changes to ever_been_changed that
        # need to be reverted.
        self.delta_ebc = { }

        # If true, we retain the data in this rollback when a load occurs.
        self.retain_after_load = False

        # True if this is a checkpoint we can roll back to.
        self.checkpoint = False

        # True if this is a hard checkpoint, where the rollback counter
        # decreases.
        self.hard_checkpoint = False

        # True if this is a not-greedy checkpoint, which should end
        # rollbacks that occur in greedy mode.
        self.not_greedy = False

        # A unique identifier for this rollback object.
        self.identifier = None

class RollbackLog(renpy.object.Object):
    """
    This class manages the list of Rollback objects.

    @ivar log: The log of rollback objects.

    @ivar current: The current rollback object. (Equivalent to
    log[-1])

    @ivar rollback_limit: The number of steps left that we can
    interactively rollback.

    Not serialized:

    @ivar mutated: A dictionary that maps object ids to a tuple of
    (weakref to object, information needed to rollback that object)
    """

    __version__ = 5

    nosave = [ 'old_store', 'mutated', 'identifier_cache' ]
    identifier_cache = None
    force_checkpoint = False

    def __init__(self):
        super(RollbackLog, self).__init__()

        self.log = [ ]
        self.current = None
        self.mutated = { }
        self.rollback_limit = 0
        self.rollback_is_fixed = False
        self.checkpointing_suspended = False
        self.fixed_rollback_boundary = None
        self.forward = [ ]
        self.old_store = { }

        # Did we just do a roll forward?
        self.rolled_forward = False

        # True if we should retain data from here to the next checkpoint
        # on load.
        self.retain_after_load_flag = False

        # Has there been an interaction since the last time this log was
        # reset?
        self.did_interaction = True

        # Should we force a checkpoint before completing the current
        # statement.
        self.force_checkpoint = False

# This was used to proxy accesses to the store. Now it's kept around to deal
# with cases where it might have leaked into a pickle.
class StoreProxy(object):

    pass
