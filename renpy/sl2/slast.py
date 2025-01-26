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

#########################################################################
# WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING
#
# When adding fields to a class in an __init__ method, we need to ensure that
# field is copied in the copy() method.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

# This file contains the abstract syntax tree for a screen language
# screen.

class SLNode(object):
    """
    The base class for screen language nodes.
    """

    # The type of constant this node is.
    constant = None

    # True if this node has at least one keyword that applies to its
    # parent. False otherwise.
    has_keyword = False

    # True if this node should be the last keyword parsed.
    last_keyword = False

    serial   = None
    location = None

class SLBlock(SLNode):
    """
    Represents a screen language block that can contain keyword arguments
    and child displayables.
    """

    # RawBlock from parse or None if not present.
    atl_transform = None

    # A list of keyword argument, expr tuples.
    keyword  = []

    # A list of child SLNodes.
    children = []

class SLCache(object):
    """
    The type of cache associated with an SLDisplayable.
    """

    # The displayable object created.
    displayable = None

    # The positional arguments that were used to create the displayable.
    positional = None

    # The keyword arguments that were used to created the displayable.
    keywords = None

    # A list of the children that were added to self.displayable.
    children = None

    # The outermost old transform.
    router_transform = None

    # The innermost old transform.
    inner_transform = None

    # The transform (or list of transforms) that was used to create self.transform.
    raw_transform = None

    # The imagemap stack entry we reuse.
    imagemap = None

    # If this can be represented as a single constant displayable,
    # do so.
    constant = None

    # For a constant statement, a list of our children that use
    # the scope.
    constant_uses_scope = []

    # For a constant statement, a map from children to widgets.
    constant_widgets = {}

    # True if the displayable should be re-created if its arguments
    # or children are changed.
    copy_on_change = False

    # The ShowIf this statement was wrapped in the last time it was wrapped.
    old_showif = None

    # The SLUse that was transcluded by this SLCache statement.
    transclude = None

    # The style prefix used when this statement was first created.
    style_prefix = None

class SLDisplayable(SLBlock):
    """
    A screen language AST node that corresponds to a displayable being
    added to the tree.

    `displayable`
        A function that, when called with the positional and keyword
        arguments, causes the displayable to be displayed.

    `scope`
        If true, the scope is supplied as an argument to the displayable.

    `child_or_fixed`
        If true and the number of children of this displayable is not one,
        the children are added to a Fixed, and the Fixed is added to the
        displayable.

    `style`
        The base name of the main style.

    `pass_context`
        If given, the context is passed in as the first positional argument
        of the displayable.

    `imagemap`
        True if this is an imagemap, and should be handled as one.

    `hotspot`
        True if this is a hotspot that depends on the imagemap it was
        first displayed with.

    `replaces`
        True if the object this displayable replaces should be
        passed to it.

    `default_keywords`
        The default keyword arguments to supply to the displayable.

    `variable`
        A variable that the main displayable is assigned to.
    """

    # A list of variables that are locally constant.
    local_constant = []

    displayable = None
    scope = None
    child_or_fixed = None
    style = None
    pass_context = None
    imagemap = None
    hotspot = None
    replaces = None
    default_keywords = None
    variable = None

    # Positional argument expressions.
    positional = []

class SLIf(SLNode):
    """
    A screen language AST node that corresponds to an If/Elif/Else statement.
    """

    # A list of entries, with each consisting of an expression (or
    # None, for the else block) and a SLBlock.
    entries = []

class SLShowIf(SLNode):
    """
    The AST node that corresponds to the showif statement.
    """

    # A list of entries, with each consisting of an expression (or
    # None, for the else block) and a SLBlock.
    entries = []

class SLFor(SLBlock):
    """
    The AST node that corresponds to a for statement. This only supports
    simple for loops that assign a single variable.
    """

    variable         = None
    expression       = None
    index_expression = None

class SLPython(SLNode):

    code = None

class SLPass(SLNode):

    pass

class SLDefault(SLNode):

    variable   = None
    expression = None

class SLUse(SLNode):

    # The name of the screen we're accessing.
    target = None

    # If the target is an SL2 screen, the SLScreen node at the root of
    # the ast for that screen.
    ast = None

    # If arguments are given, those arguments.
    args = None

    # An expression, if the id property is given.
    id = None

    # A block for transclusion, or None if the statement does not have a
    # block.
    block = None

class SLTransclude(SLNode):

    pass

class SLCustomUse(SLNode):
    """
    This represents special use screen statement defined
    by renpy.register_sl_statement.
    """

    # The name of the screen we're accessing.
    target = None

    # The SL2 SLScreen node at the root of the ast for that screen.
    ast = None

    # Positional argument expressions.
    positional = None

    # A block for transclusion, from which we also take kwargs.
    block = None

class SLScreen(SLBlock):
    """
    This represents a screen defined in the screen language 2.
    """

    version = 0

    # This screen's AST when the transcluded block is entirely
    # constant (or there is no transcluded block at all). This may be
    # the actual AST, or a copy.
    const_ast = None

    # A copy of this screen's AST when the transcluded block is not
    # constant.
    not_const_ast = None

    # The analysis
    analysis = None

    layer = "'screens'"
    sensitive = "True"

    # The name of the screen.
    name = None

    # Should this screen be declared as modal?
    modal = "False"

    # The screen's zorder.
    zorder = "0"

    # The screen's tag.
    tag = None

    # The variant of screen we're defining.
    variant = "None"

    # Should we predict this screen?
    predict = "None"

    # Should this screen be sensitive.
    sensitive = "True"

    # The parameters this screen takes.
    parameters = None

    # The analysis object used for this screen, if the screen has already been analyzed.
    analysis = None

    # True if this screen has been prepared.
    prepared = False

class ScreenCache(object):

    version            = 1
    const_analyzed     = {}
    not_const_analyzed = {}
    updated            = False
