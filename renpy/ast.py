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

import re

from . import EmptyLine, SwitchNode, TreeList, TreeNode, ValuedNode
from collections import OrderedDict

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

class Node(TreeNode):
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

    # True if the node is relevant to translation, and has to be processed by
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

    def __str__(self):
        res = ''

        if self.who:
            res += '%s ' % self.who

        if self.attributes:
            res += '%s ' % ', '.join(self.attributes)

        res += '"%s"' % self.what

        if self.arguments:
            args = self.arguments

            prepared = []

            if args.arguments:
                prepared += list(map(lambda pair: ((pair[0] + '=') if pair[0] else '') + pair[1], args.arguments))

            if args.extrapos:
                prepared.append('*' + args.extrapos)

            if args.extrakw:
                prepared.append('**' + args.extrakw)

            res += ' (%s)' % ', '.join(prepared)

        if self.with_:
            res += ' with %s' % self.with_

        return res

class Init(Node):

    block    = None
    priority = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.block:
            self.nchildren = TreeList(self.block + [EmptyLine()], self)

    def __str__(self):
        res = 'init'

        if self.priority:
            res += ' %s' % self.priority

        return res + ':'

class Label(Node):

    name       = None
    block      = None
    parameters = None
    hide       = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.block:
            self.nchildren = TreeList(self.block + [EmptyLine()], self)

    def __str__(self):
        res = 'label %s' % self.name

        if self.parameters:
            args = self.parameters

            prepared = []

            if args.parameters:
                prepared += list(map(lambda pair: pair[0] + (('=' + pair[1]) if pair[1] else ''), args.parameters))

            if args.extrapos:
                prepared.append('*' + args.extrapos)

            if args.extrakw:
                prepared.append('**' + args.extrakw)

            res += '(%s)' % ', '.join(prepared)

        if self.hide:
            res += ' hide'

        return res + ':'

class Python(Node):
    """
    @param code: A PyCode object.

    @param hide: If True, the code will be executed with its
    own local dictionary.
    """

    hide  = False
    code  = None
    store = 'store'

    def __setstate__(self, state):
        super().__setstate__(state)
        self.nchildren = TreeList([self.code.source], self)

    def __str__(self):
        res = 'python'

        if self.hide:
            res += ' hide'

        m = re.match(r'store(\.(.+))?', self.store)

        if m and m.group(1):
            res += ' in %s' % m.group(2)

        return res + ':'

class EarlyPython(Node):
    """
    @param code: A PyCode object.

    @param hide: If True, the code will be executed with its
    own local dictionary.
    """

    hide  = False
    code  = None
    store = 'store'

    def __setstate__(self, state):
        super().__setstate__(state)
        self.nchildren = TreeList([self.code.source], self)

    def __str__(self):
        res = 'python early'

        if self.hide:
            res += ' hide'

        m = re.match(r'store(\.(.+))?', self.store)

        if m and m.group(1):
            res += ' in %s' % m.group(2)

        return res + ':'

class Image(Node):
    """
    @param name: The name of the image being defined.

    @param expr: An expression yielding a Displayable that is
    assigned to the image.
    """

    imgname = None
    code    = None
    atl     = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.atl:
            self.nchildren = TreeList(self.atl.statements + [EmptyLine()], self)
        else:
            self.value = ''
            self.nchildren = TreeList([ValuedNode(self.code.source)], self)

    def __str__(self):
        if self.atl:
            return 'image %s:' % ' '.join(self.imgname)

        return 'image %s = %s' % (' '.join(self.imgname), self.value)

class Transform(Node):

    varname    = None
    atl        = None
    parameters = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if not hasattr(self, 'parameters'):
            self.parameters = ParameterInfo([], [], None, None)

        if self.atl:
            self.nchildren = TreeList(self.atl.statements + [EmptyLine()], self)

    def __str__(self):
        res = 'transform %s' % self.varname

        if self.parameters:
            if type(self.parameters.parameters) in (dict, OrderedDict):
                res += '(%s)' % ', '.join(Transform._prepare_parameters(
                    self.parameters.parameters.values(), 
                    lambda p: p.name,
                    lambda p: p.default,
                    lambda p: p.default is not None))
            elif type(self.parameters.parameters) in (list, set):
                res += '(%s)' % ', '.join(Transform._prepare_parameters(
                    self.parameters.parameters, 
                    lambda p: p[0],
                    lambda p: p[1],
                    lambda p: p[1] is not None))
            else:
                raise TypeError()

        return res + ':'
    
    @staticmethod
    def _prepare_parameters(params, first_param_func, second_param_func, second_param_filter):
        res = []

        for p in params:
            v = first_param_func(p)

            if second_param_filter(p):
                v += '=' + second_param_func(p)

            res.append(v)

        return res

class Show(Node):

    imspec = None
    atl    = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.atl:
            self.nchildren = TreeList(self.atl.statements, self)

    def __str__(self, *_):
        value = 'show'

        if self.imspec:
            if self.imspec[1]:
                value += ' expression %s' % self.imspec[1]
            elif self.imspec[0]:
                value += ' %s' % ' '.join(self.imspec[0])

            if self.imspec[2]:
                value += ' as %s' % self.imspec[2]

            if self.imspec[3]:
                value += ' at %s' % ' '.join(self.imspec[3])

        if self.atl:
            value += ':'

        return value

class ShowLayer(Node):

    warp    = True
    layer   = None
    at_list = None
    atl     = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.atl:
            self.nchildren = TreeList(self.atl.statements, self)

    def __str__(self):
        value = 'show layer %s' % self.layer

        if self.at_list:
            value += ' at %s' % ', '.join(self.at_list)

        if self.atl:
            value += ':'

        return value

class Camera(Node):

    layer   = None
    at_list = None
    atl     = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.atl:
            self.nchildren = TreeList(self.atl.statements, self)

    def __str__(self):
        value = 'camera'

        if self.layer:
            value += ' %s' % self.layer

        if self.at_list:
            value += ' at %s' % ', '.join(self.at_list)

        if self.atl:
            value += ':'

        return value

class Scene(Node):

    warp   = True
    imspec = None
    layer  = None
    atl    = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.atl:
            self.nchildren = TreeList(self.atl.statements, self)

    def __str__(self):
        value = 'scene'

        if self.imspec:
            if self.imspec[1]:
                value += ' expression %s' % self.imspec[1]
            elif self.imspec[0]:
                value += ' %s' % ' '.join(self.imspec[0])

            if self.imspec[2]:
                value += ' as %s' % self.imspec[2]

            if self.imspec[3]:
                value += ' at %s' % ' '.join(self.imspec[3])

        if self.atl:
            value += ':'

        return value

class Hide(Node):

    warp   = True
    imspec = None

    def __str__(self):
        return 'hide %s' % ' '.join(self.imspec[0])

class With(Node):

    expr   = None
    paired = None

    def __str__(self):
        return 'with %s' % self.expr

class Call(Node):

    label      = None
    expression = None
    arguments  = None

    def __str__(self):
        res = 'call %s' % self.label

        if self.arguments:
            args = self.arguments

            prepared = []

            if args.arguments:
                prepared += list(map(lambda pair: ((pair[0] + '=') if pair[0] else '') + pair[1], args.arguments))

            if args.extrapos:
                prepared.append('*' + args.extrapos)

            if args.extrakw:
                prepared.append('**' + args.extrakw)

            res += '(%s)' % ', '.join(prepared)

        return res

class Return(Node):

    expression = None
    
    def __str__(self):
        res = 'return'

        if self.expression:
            res += ' %s' % self.expression

        return  res

class Menu(Node):

    items                = None
    set                  = None
    with_                = None
    has_caption          = False
    arguments            = None
    item_arguments       = None
    translation_relevant = True
    rollback             = 'force'

    def __setstate__(self, state):
        super().__setstate__(state)

        self.nchildren = TreeList([], self)

        if self.set:
            self.nchildren.append(ValuedNode('set %s' % self.set))

        for item in self.items:
            value = '"%s"' % item[0]

            if item[1] and item[1] != 'True':
                value += ' if %s' % item[1]

            new_node = ValuedNode(value + ':')
            new_node.nchildren = TreeList(item[2], new_node)

            self.nchildren.append(new_node)

        self.nchildren.append(EmptyLine())

    def __str__(self):
        res = 'menu'

        if self.arguments:
            args = self.arguments

            prepared = []

            if args.arguments:
                prepared += list(map(lambda pair: ((pair[0] + '=') if pair[0] else '') + pair[1], args.arguments))

            if args.extrapos:
                prepared.append('*' + args.extrapos)

            if args.extrakw:
                prepared.append('**' + args.extrakw)

            res += '(%s)' % ', '.join(prepared)

        return res + ':'

class Jump(Node):

    target     = None
    expression = None

    def __str__(self):
        return 'jump %s' % self.target

class Pass(Node):

    def __str__(self):
        return 'pass'

class While(Node):

    condition = None
    block     = None

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.block:
            self.nchildren = TreeList(self.block + [EmptyLine()], self)

    def __str__(self):
        return 'while %s:' % self.condition

class If(SwitchNode, Node):

    """
    @param entries: A list of (condition, block) tuples.
    """
    entries = None

    def __setstate__(self, state):
        super().__setstate__(state)

        for i, p in enumerate(self.entries):
            self.nchildren.append(self.prepare_part(i, p[0], p[1]))

        self.nchildren.append(EmptyLine())

class UserStatement(Node):

    name                 = None
    block                = []
    code_block           = None
    parsed               = None
    line                 = None
    translatable         = False
    translation_relevant = False
    rollback             = 'normal'
    subparses            = []

    def __setstate__(self, state):
        super().__setstate__(state)

        if len(self.block):
            self.nchildren = TreeList(list(map(lambda item: ValuedNode(item[2]), self.block)) + [EmptyLine()], self)

    def __str__(self):
        return self.line

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

    def __str__(self):
        value = 'define '

        m = re.match(r'store\.(.+)', self.store)

        if m:
            value += m.group(1) + '.'

        return value + '%s %s %s' % (self.varname, self.operator, self.code.source)

class Default(Node):

    varname  = None
    code     = None
    store    = 'store'

    def __str__(self):
        value = 'default '

        m = re.match(r'store\.(.+)', self.store)

        if m:
            value += m.group(1) + '.'

        return value + '%s = %s' % (self.varname, self.code.source)

class Screen(Node):

    screen = None

    def __setstate__(self, state):
        super().__setstate__(state)

        self.nchildren = TreeList([self.screen], self)
        self.nexclude = True

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

    def __setstate__(self, state):
        super().__setstate__(state)

        self.nchildren = TreeList(self.block, self)

    def __str__(self):
        return 'translate %s %s:' % (self.language, self.identifier)

class EndTranslate(Node):
    """
    A node added implicitly after each translate block. It's responsible for
    resetting the translation identifier.
    """

    rollback = 'never'

    def __setstate__(self, state):
        super().__setstate__(state)
        self.nexclude = True

class TranslateString(Node):
    """
    A node used for translated strings.
    """

    language             = None
    old                  = None
    new                  = None
    newloc               = None
    translation_relevant = True

    def __setstate__(self, state):
        super().__setstate__(state)

        self.nchildren = TreeList([
            PyExpr('old "%s"' % self.old, filename=None, linenumber=None),
            PyExpr('new "%s"' % self.new, filename=None, linenumber=None)
        ], self)

    def __str__(self):
        return 'translate %s strings:' % self.language

class TranslateBlock(Node):
    """
    Runs a block of code when changing the language.
    """

    language             = None
    block                = None
    translation_relevant = True

    def __setstate__(self, state):
        super().__setstate__(state)

        if self.block:
            self.nchildren = TreeList(self.block, self)

    def __str__(self):
        if not len(self.block):
            return 'translate <invalid>'

        child = self.block[0]
        return 'translate %s style %s:' % (self.language, child.style_name)

class TranslateEarlyBlock(TranslateBlock):
    """
    This is similar to the TranslateBlock, except it runs before deferred
    styles do.
    """

    def __str__(self):
        return 'translate %s python:' % self.language

class Style(Node):

    style_name = None
    parent     = None
    properties = None
    clear      = None
    take       = None
    delattr    = None
    variant    = None

    def __setstate__(self, state):
        super().__setstate__(state)

        self.nchildren = TreeList([], self)

        if not self.properties:
            return
        
        for k, v in self.properties.items():
            value = k

            if v:
                value += ' %s' % v

            self.nchildren.append(ValuedNode(value))

        self.nchildren.append(EmptyLine())

    def __str__(self):
        res = 'style %s' % self.style_name

        if self.parent:
            res += ' is %s' % self.parent

        if self.clear:
            res += ' clear'

        if self.take:
            res += ' take %s' % self.take

        if self.variant:
            res += ' variant %s' % self.variant

        if len(self.nchildren):
            res += ':'

        return res
