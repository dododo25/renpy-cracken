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

# This file contains the AST for the Ren'Py script language. Each class
# here corresponds to a statement in the script language.

# NOTE:
# When updating this file, consider if lint.py or warp.py also need
# updating.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

class ParameterInfo(object):
    """
    This class is used to store information about parameters to a
    label.
    """

    def __init__(self, parameters, positional, extrapos, extrakw):
        # A list of parameter name, default value pairs.
        self.parameters = parameters

        # A list, giving the positional parameters to this function,
        # in order.
        self.positional = positional

        # A variable that takes the extra positional arguments, if
        # any. None if no such variable exists.
        self.extrapos = extrapos

        # A variable that takes the extra keyword arguments, if
        # any. None if no such variable exists.
        self.extrakw = extrakw

class ArgumentInfo(object):

    def __init__(self, arguments, extrapos, extrakw):
        # A list of (keyword, expression) pairs. If an argument doesn't
        # have a keyword, it's thought of as positional.
        self.arguments = arguments

        # An expression giving extra positional arguments being
        # supplied to this function.
        self.extrapos = extrapos

        # An expression giving extra keyword arguments that need
        # to be supplied to this function.
        self.extrakw = extrakw

class PyExpr(str):
    """
    Represents a string containing python code.
    """

    def __new__(cls, s, filename, linenumber, py=3):
        self = str.__new__(cls, s)

        self.filename = filename
        self.linenumber = linenumber
        self.py = py

        return self

class PyCode(object):

    __slots__ = [
        'source',
        'mode',
        'location',
        'bytecode',
        'py'
    ]

    def __setstate__(self, state):
        if len(state) == 5:
            (_, self.source, self.location, self.mode, self.py) = state
        else:
            (_, self.source, self.location, self.mode) = state

        self.bytecode = None

class Node(object):
    """
    A node in the abstract syntax tree of the program.

    @ivar name: The name of this node.
    @ivar filename: The filename where this node comes from.
    @ivar linenumber: The line number of the line on which this node is defined.
    @ivar next: The statement that will execute after this one.
    @ivar statement_start: If present, the first node that makes up the statement that includes this node.
    """

    # True if this node is translatable, false otherwise. (This can be set on
    # the class or the instance.)
    translatable = False

    # True if the node is releveant to translation, and has to be processed by
    # take_translations.
    translation_relevant = False

    # How does the node participate in rollback?
    #
    # * "normal" in normal mode.
    # * "never" generally never.
    # * "force" force it to start.
    rollback = 'normal'

    def __setstate__(self, state):
        self.__dict__.update(state[1])

class Say(Node):

    who                  = None
    what                 = None
    with_                = None
    interact             = None
    arguments            = None
    attributes           = None
    temporary_attributes = None
    identifier           = None
    rollback             = 'normal'

    def __setstate__(self, state):
        super().__setstate__(state)

        if hasattr(self, 'who') and self.who:
            self.who = self.who.strip()

class Init(Node):

    block    = None
    priority = None

class Label(Node):

    name       = None
    block      = None
    parameters = None
    hide       = None

class Python(Node):
    """
    @param code: A PyCode object.

    @param hide: If True, the code will be executed with its
    own local dictionary.
    """

    hide  = False
    code  = None
    store = 'store'

class EarlyPython(Node):
    """
    @param code: A PyCode object.

    @param hide: If True, the code will be executed with its
    own local dictionary.
    """

    hide  = False
    code  = None
    store = 'store'

class Image(Node):
    """
    @param name: The name of the image being defined.

    @param expr: An expression yielding a Displayable that is
    assigned to the image.
    """

    imgname = None
    code    = None
    atl     = None

class Transform(Node):

    varname    = None
    atl        = None
    parameters = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if not hasattr(self, 'parameters'):
            self.parameters = ParameterInfo([], [], None, None)

class Show(Node):

    imspec = None
    atl    = None

class ShowLayer(Node):

    warp    = True
    layer   = None
    at_list = None
    atl     = None

class Camera(Node):

    layer   = None
    at_list = None
    atl     = None

class Scene(Node):

    warp   = True
    imspec = None
    layer  = None
    atl    = None

class Hide(Node):

    warp   = True
    imspec = None

class With(Node):

    expr   = None
    paired = None

class Call(Node):

    label      = None
    expression = None
    arguments  = None

class Return(Node):

    expression = None

class Menu(Node):

    items                = None
    set                  = None
    with_                = None
    has_caption          = False
    arguments            = None
    item_arguments       = None
    translation_relevant = True
    rollback             = 'force'

class Jump(Node):

    target     = None
    expression = None

class Pass(Node):

    pass

class While(Node):

    condition = None
    block     = None

class If(Node):

    """
    @param entries: A list of (condition, block) tuples.
    """
    entries = None

class UserStatement(Node):

    name                 = None
    block                = []
    code_block           = None
    parsed               = None
    line                 = None
    translatable         = False
    translation_relevant = False
    rollback             = 'normal'
    subparses            = [ ]

class PostUserStatement(Node):

    name   = None
    parent = None

class StoreNamespace(object):

    pure  = True
    store = None

class Define(Node):

    varname  = None
    code     = None
    store    = 'store'
    operator = '='
    index    = None

class Default(Node):

    varname  = None
    code     = None
    store    = 'store'

class Screen(Node):

    screen = None

################################################################################
# Translations
################################################################################

class Translate(Node):
    """
    A translation block, produced either by explicit translation statements
    or implicit translation blocks.

    If language is None, when executed this transfers control to the translate
    statement in the current language, if any, and otherwise runs the block.
    If language is not None, causes an error to occur if control reaches this
    statement.

    When control normally leaves a translate statement, in any language, it
    goes to the end of the translate statement in the None language.
    """

    identifier           = None
    alternate            = None
    language             = None
    block                = None
    after                = None
    rollback             = 'never'
    translation_relevant = True

class EndTranslate(Node):
    """
    A node added implicitly after each translate block. It's responsible for
    resetting the translation identifier.
    """

    rollback = 'never'

class TranslateString(Node):
    """
    A node used for translated strings.
    """

    language             = None
    old                  = None
    new                  = None
    newloc               = None
    translation_relevant = True

class TranslatePython(Node):
    """
    Runs python code when changing the language.

    This is no longer generated, but is still run when encountered.
    """

    language             = None
    code                 = None
    translation_relevant = True

class TranslateBlock(Node):
    """
    Runs a block of code when changing the language.
    """

    language             = None
    block                = None
    translation_relevant = True

class TranslateEarlyBlock(TranslateBlock):
    """
    This is similar to the TranslateBlock, except it runs before deferred
    styles do.
    """

class Style(Node):

    style_name = None
    parent     = None
    properties = None
    clear      = None
    take       = None
    delattr    = None
    variant    = None
