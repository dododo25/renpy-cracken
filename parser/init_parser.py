import renpy

from block import EmptyLine, LevelDown, LevelUp

TYPE = renpy.ast.Init

def parse(obj, level):
    value = 'init'

    if obj.priority:
        value += ' %s' % obj.priority

    return {'type': 'init', 'level': level, 'value': value + ':'}, level, [LevelUp(), *obj.block, EmptyLine(), LevelDown()]
