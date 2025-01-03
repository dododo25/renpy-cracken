import renpy

from block import EmptyLine, Label

TYPE = renpy.ast.Label

def parse(obj, level):
    value = 'label %s' % obj.name

    if obj.parameters:
        value += '(%s)' % ', '.join(obj.parameters)

    return None, level, [EmptyLine(), Label(value, obj.block)]
