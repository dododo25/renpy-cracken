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

    __slots__ = [
        'arguments',
        'extrapos',
        'extrakw'
    ]

class PyExpr(str):
    """
    Represents a string containing python code.
    """

    def __new__(cls, s, filename, linenumber):
        self = str.__new__(cls, s)

        self.filename = filename
        self.linenumber = linenumber

        return self

class PyCode(object):

    __slots__ = [
        'source',
        'mode',
        'location',
        'bytecode'
    ]

    def __getstate__(self):
        return (1, self.source, self.location, self.mode)

    def __setstate__(self, state):
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
    rollback = "normal"

    def __init__(self, loc):
        """
        Initializes this Node object.

        @param loc: A (filename, physical line number) tuple giving the
        logical line on which this Node node starts.
        """
        self.filename, self.linenumber = loc
        self.name = None
        self.next = None

class Say(Node):

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.attributes = None
        self.interact = True
        self.arguments = None
        self.temporary_attributes = None
        self.rollback = "normal"
        return self

    def __init__(self, loc, who, what, with_, interact=True, attributes=None, arguments=None, temporary_attributes=None, identifier=None):
        super(Say, self).__init__(loc)

        if who is not None:
            self.who = who.strip()
        else:
            self.who = None

        self.what = what
        self.with_ = with_
        self.interact = interact
        self.arguments = arguments

        # A tuple of attributes that are applied to the character that's
        # speaking, or None to disable this behavior.
        self.attributes = attributes

        # Ditto for temporary attributes.
        self.temporary_attributes = temporary_attributes

        # If given, write in the identifier.
        if identifier is not None:
            self.identifier = identifier

class Init(Node):

    def __init__(self, loc, block, priority):
        super(Init, self).__init__(loc)

        self.block = block
        self.priority = priority

class Label(Node):

    def __init__(self, loc, name, block, parameters, hide=False):
        super(Label, self).__init__(loc)

        self.name = name
        self.block = block
        self.parameters = parameters
        self.hide = hide

class Python(Node):

    def __init__(self, loc, python_code, hide=False, store="store"):
        """
        @param code: A PyCode object.

        @param hide: If True, the code will be executed with its
        own local dictionary.
        """
        super(Python, self).__init__(loc)

        self.hide = hide

        if hide:
            self.code = PyCode(python_code, mode='hide')
        else:
            self.code = PyCode(python_code, mode='exec')

        self.store = store

class EarlyPython(Node):

    def __init__(self, loc, python_code, hide=False, store="store"):
        """
        @param code: A PyCode object.

        @param hide: If True, the code will be executed with its
        own local dictionary.
        """
        super(EarlyPython, self).__init__(loc)

        self.hide = hide

        if hide:
            self.code = PyCode(python_code, mode='hide')
        else:
            self.code = PyCode(python_code, mode='exec')

        self.store = store

class Image(Node):

    def __init__(self, loc, name, expr=None, atl=None):
        """
        @param name: The name of the image being defined.

        @param expr: An expression yielding a Displayable that is
        assigned to the image.
        """
        super(Image, self).__init__(loc)

        self.imgname = name

        if expr:
            self.code = PyCode(expr, mode='eval')
            self.atl = None
        else:
            self.code = None
            self.atl = atl

class Transform(Node):

    default_parameters = ParameterInfo([], [], None, None)

    def __init__(self, loc, name, atl=None, parameters=default_parameters):
        super(Transform, self).__init__(loc)

        self.varname = name
        self.atl = atl
        self.parameters = parameters

class Show(Node):

    def __init__(self, loc, imspec, atl=None):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a layer.
        """
        super(Show, self).__init__(loc)

        self.imspec = imspec
        self.atl = atl

class ShowLayer(Node):

    __slots__ = [
        'layer',
        'at_list',
        'atl',
    ]

    warp = True

    def __init__(self, loc, layer, at_list, atl):
        super(ShowLayer, self).__init__(loc)

        self.layer = layer
        self.at_list = at_list
        self.atl = atl

class Camera(Node):

    def __init__(self, loc, layer, at_list, atl):
        super(Camera, self).__init__(loc)

        self.layer = layer
        self.at_list = at_list
        self.atl = atl

class Scene(Node):

    __slots__ = [
        'imspec',
        'layer',
        'atl',
    ]

    warp = True

    def __init__(self, loc, imgspec, layer, atl=None):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a layer, or
        None to not have this scene statement also display an image.
        """
        super(Scene, self).__init__(loc)

        self.imspec = imgspec
        self.layer = layer
        self.atl = atl

class Hide(Node):

    __slots__ = [
        'imspec',
    ]

    warp = True

    def __init__(self, loc, imgspec):
        """
        @param imspec: A triple consisting of an image name (itself a
        tuple of strings), a list of at expressions, and a list of
        with expressions.
        """
        super(Hide, self).__init__(loc)
        self.imspec = imgspec

class With(Node):

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.paired = None
        return self

    def __init__(self, loc, expr, paired=None):
        """
        @param expr: An expression giving a transition or None.
        """
        super(With, self).__init__(loc)

        self.expr = expr
        self.paired = paired

class Call(Node):

    __slots__ = [
        'label',
        'arguments',
        'expression',
    ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.arguments = None
        return self

    def __init__(self, loc, label, expression, arguments):
        super(Call, self).__init__(loc)

        self.label = label
        self.expression = expression
        self.arguments = arguments

class Return(Node):

    def __init__(self, loc, expression):
        super(Return, self).__init__(loc)

        self.expression = expression

class Menu(Node):

    __slots__ = [
        'items',
        'set',
        'with_',
        'has_caption',
        'arguments',
        'item_arguments',
        'rollback',
    ]

    translation_relevant = True

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.has_caption = False
        self.arguments = None
        self.item_arguments = None
        self.rollback = "force"
        return self

    def __init__(self, loc, items, set, with_, has_caption, arguments, item_arguments): # @ReservedAssignment
        super(Menu, self).__init__(loc)

        self.items = items
        self.set = set
        self.with_ = with_
        self.has_caption = has_caption
        self.arguments = arguments
        self.item_arguments = item_arguments

class Jump(Node):

    def __init__(self, loc, target, expression):
        super(Jump, self).__init__(loc)

        self.target = target
        self.expression = expression

class Pass(Node):

    pass

class While(Node):

    def __init__(self, loc, condition, block):
        super(While, self).__init__(loc)

        self.condition = condition
        self.block = block

class If(Node):

    def __init__(self, loc, entries):
        """
        @param entries: A list of (condition, block) tuples.
        """
        super(If, self).__init__(loc)

        self.entries = entries

class UserStatement(Node):

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.block = [ ]
        self.code_block = None
        self.translatable = False
        self.translation_relevant = False
        self.rollback = "normal"
        self.subparses = [ ]
        return self

    def __init__(self, loc, line, block, parsed):
        super(UserStatement, self).__init__(loc)

        self.code_block = None
        self.parsed = parsed
        self.line = line
        self.block = block
        self.subparses = [ ]

        self.name = self.call("label")

class PostUserStatement(Node):

    __slots__ = [
        'parent',
    ]

    def __init__(self, loc, parent):
        super(PostUserStatement, self).__init__(loc)

        self.parent = parent
        self.name = self.parent.call('post_label')

class StoreNamespace(object):

    pure = True

    def __init__(self, store):
        self.store = store

class Define(Node):

    __slots__ = [
        'varname',
        'code',
        'store',
        'operator',
        'index',
    ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.store = 'store'
        self.operator = '='
        self.index = None
        return self

    def __init__(self, loc, store, name, index, operator, expr):
        super(Define, self).__init__(loc)

        self.store = store
        self.varname = name

        if index is not None:
            self.index = PyCode(index, mode='eval')

        self.operator = operator
        self.code = PyCode(expr, mode='eval')

class Default(Node):

    __slots__ = [
        'varname',
        'code',
        'store',
    ]

    def __init__(self, loc, store, name, expr):
        super(Default, self).__init__(loc)

        self.store = store
        self.varname = name
        self.code = PyCode(expr, mode='eval')

class Screen(Node):

    __slots__ = [
        'screen',
    ]

    def __init__(self, loc, screen):
        """
        @param screen: The screen object being defined.
        In SL1, an instance of screenlang.ScreenLangScreen.
        In SL2, an instance of sl2.slast.SLScreen.
        """
        super(Screen, self).__init__(loc)
        self.screen = screen

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

    __slots__ = [
        'identifier',
        'alternate',
        'language',
        'block',
        'after'
    ]

    rollback = "never"

    translation_relevant = True

    def __init__(self, loc, identifier, language, block, alternate=None):
        super(Translate, self).__init__(loc)

        self.identifier = identifier
        self.alternate = alternate
        self.language = language
        self.block = block

class EndTranslate(Node):
    """
    A node added implicitly after each translate block. It's responsible for
    resetting the translation identifier.
    """

    rollback = "never"

    def __init__(self, loc):
        super(EndTranslate, self).__init__(loc)

class TranslateString(Node):
    """
    A node used for translated strings.
    """

    __slots__ = [
        'language',
        'old',
        'new',
        'newloc'
    ]

    translation_relevant = True

    def __init__(self, loc, language, old, new, newloc):
        super(TranslateString, self).__init__(loc)

        self.language = language
        self.old = old
        self.new = new
        self.newloc = newloc

class TranslatePython(Node):
    """
    Runs python code when changing the language.

    This is no longer generated, but is still run when encountered.
    """

    translation_relevant = True

    __slots__ = [
        'language',
        'code',
    ]

    def __init__(self, loc, language, python_code):
        """
        @param code: A PyCode object.

        @param hide: If True, the code will be executed with its
        own local dictionary.
        """
        super(TranslatePython, self).__init__(loc)

        self.language = language
        self.code     = PyCode(python_code, mode='exec')

class TranslateBlock(Node):
    """
    Runs a block of code when changing the language.
    """

    translation_relevant = True

    __slots__ = [
        'block',
        'language',
    ]

    def __init__(self, loc, language, block):
        super(TranslateBlock, self).__init__(loc)

        self.language = language
        self.block = block

class TranslateEarlyBlock(TranslateBlock):
    """
    This is similar to the TranslateBlock, except it runs before deferred
    styles do.
    """

class Style(Node):

    __slots__ = [
        'style_name',
        'parent',
        'properties',
        'clear',
        'take',
        'delattr',
        'variant',
    ]

    def __init__(self, loc, name):
        """
        `name`
            The name of the style to define.
        """
        super(Style, self).__init__(loc)

        self.style_name = name

        # The parent of this style.
        self.parent = None

        # Properties.
        self.properties = {}

        # Should we clear the style?
        self.clear = False

        # Should we take properties from another style?
        self.take = None

        # A list of attributes we should delete from this style.
        self.delattr = []

        # If not none, an expression for the variant.
        self.variant = None

class Testcase(Node):

    __slots__ = [
        'label',
        'test',
    ]

    def __init__(self, loc, label, test):
        super(Testcase, self).__init__(loc)

        self.label = label
        self.test = test

class RPY(Node):

    __slots__ = [
        'rest'
    ]

    def __init__(self, loc, rest):
        super(RPY, self).__init__(loc)
        self.rest = rest
