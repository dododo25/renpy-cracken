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

    def __new__(cls, s, filename, linenumber):
        self = str.__new__(cls, s)
        self.filename = filename
        self.linenumber = linenumber

        return self

class PyCode(object):

    def __getstate__(self):
        return (1, self.source, self.location, self.mode)

    def __setstate__(self, state):
        (_, self.source, self.location, self.mode) = state
        self.bytecode = None

    def __init__(self, source, mode='exec'):
        # The source code.
        self.source = source
        self.mode = mode

class Scry(object):
    """
    This is used to store information about the future, if we know it. Unlike
    predict, this tries to only get things we _know_ will happen.
    """

    # By default, all attributes are None.
    def __getattr__(self, name):
        return None

    def next(self): # @ReservedAssignment
        if self._next is None:
            return None
        else:
            try:
                return self._next.scry()
            except:
                return None

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

    default_parameters = ParameterInfo([ ], [ ], None, None)

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

    warp = True

    __slots__ = [
        'layer',
        'at_list',
        'atl',
        ]

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

    def diff_info(self):

        if self.imspec:
            data = tuple(self.imspec[0])
        else:
            data = None

        return (Scene, data)

    def execute(self):

        next_node(self.next)
        statement_name("scene")

        renpy.config.scene(self.layer)

        if self.imspec:
            show_imspec(self.imspec, atl=getattr(self, "atl", None))

    def predict(self):

        if self.imspec:
            predict_imspec(self.imspec, atl=getattr(self, "atl", None), scene=True)

        return [ self.next ]

    def analyze(self):
        if getattr(self, 'atl', None) is not None:
            self.atl.mark_constant()


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

    def diff_info(self):
        return (Hide, tuple(self.imspec[0]))

    def predict(self):

        if len(self.imspec) == 3:
            name, _at_list, layer = self.imspec
            tag = None
            _expression = None
            _zorder = None
            _behind = None
        elif len(self.imspec) == 6:
            name, _expression, tag, _at_list, layer, _zorder = self.imspec
            _behind = None
        elif len(self.imspec) == 7:
            name, _expression, tag, _at_list, layer, _zorder, _behind = self.imspec

        if tag is None:
            tag = name[0]

        layer = renpy.exports.default_layer(layer, tag)

        renpy.game.context().images.predict_hide(layer, (tag,))

        return [ self.next ]

    def execute(self):

        next_node(self.next)
        statement_name("hide")

        if len(self.imspec) == 3:
            name, _at_list, layer = self.imspec
            _expression = None
            tag = None
            _zorder = 0
        elif len(self.imspec) == 6:
            name, _expression, tag, _at_list, layer, _zorder = self.imspec
        elif len(self.imspec) == 7:
            name, _expression, tag, _at_list, layer, _zorder, _behind = self.imspec

        layer = renpy.exports.default_layer(layer, tag or name)

        renpy.config.hide(tag or name, layer)


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

    def diff_info(self):
        return (Call, self.label, self.expression)

    def execute(self):

        statement_name("call")

        label = self.label
        if self.expression:
            label = renpy.python.py_eval(label)

        rv = renpy.game.context().call(label, return_site=self.next.name)
        next_node(rv)
        renpy.game.context().abnormal = True

        if self.arguments:
            args, kwargs = self.arguments.evaluate()
            renpy.store._args = args
            renpy.store._kwargs = kwargs
        else:
            renpy.store._args = None
            renpy.store._kwargs = None

    def predict(self):

        label = self.label

        if self.expression:

            if not probably_side_effect_free(label):
                return [ ]

            try:
                label = renpy.python.py_eval(label)
            except:
                return [ ]

            if not renpy.game.script.has_label(label):
                return [ ]

        return [ renpy.game.context().predict_call(label, self.next.name) ]

    def scry(self):
        rv = Node.scry(self)
        rv._next = None
        return rv

class Return(Node):

    def __init__(self, loc, expression):
        super(Return, self).__init__(loc)
        self.expression = expression

class Menu(Node):

    translation_relevant = True

    __slots__ = [
        'items',
        'set',
        'with_',
        'has_caption',
        'arguments',
        'item_arguments',
        'rollback',
        ]

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
        self.rollback = renpy.statements.get("rollback", self.parsed) or "normal"

    def __repr__(self):
        return "<UserStatement {!r}>".format(self.line)

    def get_children(self, f):
        f(self)

        if self.code_block is not None:
            for i in self.code_block:
                i.get_children(f)

        for i in self.subparses:
            for j in i.block:
                j.get_children(f)

    def chain(self, next): # @ReservedAssignment
        self.next = next

        if self.code_block is not None:
            chain_block(self.code_block, next)

        for i in self.subparses:
            chain_block(i.block, next)

    def replace_next(self, old, new):
        Node.replace_next(self, old, new)

        if (self.code_block) and (self.code_block[0] is old):
            self.code_block.insert(0, new)

        for i in self.subparses:
            if i.block[0] is old:
                self.code_block.insert(0, new)

    def restructure(self, callback):
        if self.code_block:
            callback(self.code_block)

        for i in self.subparses:
            callback(i.block)

    def diff_info(self):
        return (UserStatement, self.line)

    def call(self, method, *args, **kwargs):

        parsed = self.parsed

        if parsed is None:
            parsed = renpy.statements.parse(self, self.line, self.block)
            self.parsed = parsed

        return renpy.statements.call(method, parsed, *args, **kwargs)

    def execute_init(self):
        self.call("execute_init")

    def get_init(self):
        return 0, self.execute_init

    def execute(self):
        next_node(self.get_next())
        statement_name(self.get_name())

        self.call("execute")

    def predict(self):
        predictions = self.call("predict")

        if predictions is not None:
            for i in predictions:
                renpy.easy.predict(i)

        if self.parsed and renpy.statements.get("predict_all", self.parsed):
            return [ i.block[0] for i in self.subparses ] + [ self.next ]

        if self.next:
            next_label = self.next.name
        else:
            next_label = None

        next_list = self.call("predict_next", next_label)

        if next_list is not None:
            nexts = [ renpy.game.script.lookup_or_none(i) for i in next_list if i is not None ]
            return [ i for i in nexts if i is not None ]

        return [ self.next ]

    def get_name(self):
        parsed = self.parsed

        if parsed is None:
            parsed = renpy.statements.parse(self, self.line, self.block)
            self.parsed = parsed

        return renpy.statements.get_name(parsed)

    def get_next(self):

        if self.code_block and len(self.code_block):
            rv = self.call("next", self.code_block[0].name)
        else:
            rv = self.call("next")

        if rv is not None:
            return renpy.game.script.lookup(rv)
        else:
            return self.next

    def scry(self):
        rv = Node.scry(self)
        rv._next = self.get_next()
        self.call("scry", rv)
        return rv

    def get_code(self, dialogue_filter=None):
        return self.line

    def can_warp(self):

        if self.call("warp"):
            return True

        return False


class PostUserStatement(Node):

    __slots__ = [
        'parent',
        ]

    def __init__(self, loc, parent):

        super(PostUserStatement, self).__init__(loc)
        self.parent = parent

        self.name = self.parent.call("post_label")

    def __repr__(self):
        return "<PostUserStatement {!r}>".format(self.parent.line)

    def diff_info(self):
        return (PostUserStatement, self.parent.line)

    def execute(self):
        next_node(self.next)
        statement_name("post " + self.parent.get_name())

        self.parent.call("post_execute")


def create_store(name):
    if name not in renpy.config.special_namespaces:
        renpy.python.create_store(name)


class StoreNamespace(object):
    pure = True

    def __init__(self, store):
        self.store = store

    def set(self, name, value):
        renpy.python.store_dicts[self.store][name] = value

    def get(self, name):
        return renpy.python.store_dicts[self.store][name]


def get_namespace(store):
    """
    Returns the namespace object for `store`, and a flag that is true if the
    namespace is special, and false if it is a normal store.
    """

    if store in renpy.config.special_namespaces:
        return renpy.config.special_namespaces[store], True

    return StoreNamespace(store), False

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
        else:
            self.index = None

        self.operator = operator
        self.code = PyCode(expr, mode='eval')

    def diff_info(self):
        return (Define, self.store, self.varname)

    def early_execute(self):
        create_store(self.store)

        if self.operator != "=":
            return

        if self.index is not None:
            return

        if self.store == "store.config" and self.varname in EARLY_CONFIG:

            value = renpy.python.py_eval_bytecode(self.code.bytecode)
            setattr(renpy.config, self.varname, value)

    def execute(self):

        next_node(self.next)
        statement_name("define")

        define_statements.append(self)

        if self.store == 'store':
            renpy.dump.definitions.append((self.varname, self.filename, self.linenumber))
        else:
            renpy.dump.definitions.append((self.store[6:] + "." + self.varname, self.filename, self.linenumber))

        if self.operator == "=" and self.index is None:
            ns, _special = get_namespace(self.store)
            if getattr(ns, "pure", True):
                renpy.exports.pure(self.store + "." + self.varname)

        self.set()

    def redefine(self, stores):

        if self.store not in stores:
            return

        self.set()

    def set(self):

        value = renpy.python.py_eval_bytecode(self.code.bytecode)
        ns, _special = get_namespace(self.store)

        if (self.index is None) and (self.operator == "="):
            ns.set(self.varname, value)
            return

        base = ns.get(self.varname)
        old = base

        if self.index:
            key = renpy.python.py_eval_bytecode(self.index.bytecode)

            if self.operator != "=":
                old = base[key]

        if self.operator == "=":
            new = value
        elif self.operator == "+=":
            new = old + value
        elif self.operator == "|=":
            new = old | value

        if self.index:
            base[key] = new
        else:
            ns.set(self.varname, new)


def redefine(stores):
    """
    Re-runs the given define statements.
    """

    for i in define_statements:
        i.redefine(stores)


# All the default statements, in the order they were registered.
default_statements = [ ]


class Default(Node):

    __slots__ = [
        'varname',
        'code',
        'store',
        ]

    def __new__(cls, *args, **kwargs):
        self = Node.__new__(cls)
        self.store = 'store'
        return self

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

    def diff_info(self):
        return (Screen, self.screen.name)

    def execute(self):
        next_node(self.next)
        statement_name("screen")

        self.screen.define((self.filename, self.linenumber))
        renpy.dump.screens.append((self.screen.name, self.filename, self.linenumber))

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

    rollback = "never"

    translation_relevant = True

    __slots__ = [
        "identifier",
        "alternate",
        "language",
        "block",
        "after",
        ]

    def __init__(self, loc, identifier, language, block, alternate=None):
        super(Translate, self).__init__(loc)

        self.identifier = identifier
        self.alternate = alternate
        self.language = language
        self.block = block

    def diff_info(self):
        return (Translate, self.identifier, self.language)

    def chain(self, next): # @ReservedAssignment
        if self.block:
            self.next = self.block[0]
            chain_block(self.block, next)
        else:
            self.next = next

        self.after = next

    def replace_next(self, old, new):
        Node.replace_next(self, old, new)

        if self.block and (self.block[0] is old):
            self.block.insert(0, new)

        if self.after is old:
            self.after = new

    def lookup(self):
        return renpy.game.script.translator.lookup_translate(self.identifier, getattr(self, "alternate", None))

    def execute(self):

        statement_name("translate")

        if self.language is not None:
            next_node(self.next)
            raise Exception("Translation nodes cannot be run directly.")

        if self.identifier not in renpy.game.persistent._seen_translates: # @UndefinedVariable
            renpy.game.persistent._seen_translates.add(self.identifier) # @UndefinedVariable
            renpy.game.seen_translates_count += 1
            renpy.game.new_translates_count += 1

        next_node(self.lookup())

        renpy.game.context().translate_identifier = self.identifier
        renpy.game.context().alternate_translate_identifier = getattr(self, "alternate", None)

    def predict(self):
        node = self.lookup()
        return [ node ]

    def scry(self):
        rv = Scry()
        rv._next = self.lookup()
        return rv

    def get_children(self, f):
        f(self)

        for i in self.block:
            i.get_children(f)

    def restructure(self, callback):
        return callback(self.block)


class EndTranslate(Node):
    """
    A node added implicitly after each translate block. It's responsible for
    resetting the translation identifier.
    """

    rollback = "never"

    def __init__(self, loc):
        super(EndTranslate, self).__init__(loc)

    def diff_info(self):
        return (EndTranslate,)

    def execute(self):
        next_node(self.next)
        statement_name("end translate")

        renpy.game.context().translate_identifier = None
        renpy.game.context().alternate_translate_identifier = None


class TranslateString(Node):
    """
    A node used for translated strings.
    """

    translation_relevant = True

    __slots__ = [
        "language",
        "old",
        "new",
        "newloc",
        ]

    def __init__(self, loc, language, old, new, newloc):
        super(TranslateString, self).__init__(loc)
        self.language = language

        self.old = old
        self.new = new
        self.newloc = newloc

    def diff_info(self):
        return (TranslateString,)

    def execute(self):
        next_node(self.next)
        statement_name("translate string")

        newloc = getattr(self, "newloc", (self.filename, self.linenumber + 1))
        renpy.translation.add_string_translation(self.language, self.old, self.new, newloc)


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
        self.code = PyCode(python_code, mode='exec')

    def diff_info(self):
        return (TranslatePython, self.code.source)

    def execute(self):
        next_node(self.next)
        statement_name("translate_python")

    # def early_execute(self):
    #    renpy.python.create_store(self.store)
    #    renpy.python.py_exec_bytecode(self.code.bytecode, self.hide, store=self.store)


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

    def get_children(self, f):
        f(self)

        for i in self.block:
            i.get_children(f)

    # We handle chaining specially. We want to chain together the nodes in
    # the block, but we want that chain to end in None, and we also want
    # this node to just continue on to the next node in normal execution.
    def chain(self, next): # @ReservedAssignment
        self.next = next
        chain_block(self.block, None)

    def execute(self):
        next_node(self.next)
        statement_name("translate_block")

    def restructure(self, callback):
        callback(self.block)


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
        self.properties = { }

        # Should we clear the style?
        self.clear = False

        # Should we take properties from another style?
        self.take = None

        # A list of attributes we should delete from this style.
        self.delattr = [ ]

        # If not none, an expression for the variant.
        self.variant = None

    def diff_info(self):
        return (Style, self.style_name)

    def apply(self):
        if self.variant is not None:
            variant = renpy.python.py_eval(self.variant)
            if not renpy.exports.variant(variant):
                return

        s = renpy.style.get_or_create_style(self.style_name) # @UndefinedVariable

        if self.clear:
            s.clear()

        if self.parent is not None:
            s.set_parent(self.parent)

        if self.take is not None:
            s.take(self.take)

        for i in self.delattr:
            s.delattr(i)

        if self.properties:
            properties = { }

            for name, expr in self.properties.items():

                value = renpy.python.py_eval(expr)

                if name == "properties":
                    properties.update(value)
                else:
                    properties[name] = value

            s.add_properties(properties)

    def execute(self):
        next_node(self.next)
        statement_name("style")

        if renpy.config.defer_styles and renpy.game.context().init_phase:
            renpy.translation.deferred_styles.append(self)
            return

        self.apply()


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
        "rest"
        ]

    def __init__(self, loc, rest):
        super(RPY, self).__init__(loc)

        self.rest = rest
