import renpy

TYPE = renpy.ast.Return

def parse(obj, level):
    value = 'return'

    if obj.expression:
        value += ' %s' % obj.expression

    return {'type': 'return', 'level': level, 'value': value}, level, []
