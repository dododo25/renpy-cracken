from block import LevelDown, LevelUp, IfPart

TYPE = IfPart

def parse(obj, level):
    if obj.type == 'else':
        b = {'type': 'else', 'level': level, 'value': 'else:'}
    else:
        b = {'type': obj.type, 'level': level, 'value': '%s %s:' % (obj.type, obj.condition)}

    return b, level, [LevelUp(), *obj.block, LevelDown()]
