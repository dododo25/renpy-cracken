import renpy

TYPE = renpy.ast.Say

def parse(obj, level):
    value = ''

    if obj.who:
        value += "%s " % obj.who

    value += '"%s"' % obj.what

    if obj.with_:
        value += " with %s" % obj.with_

    return {'type': 'say', 'level': level, 'value': value}, level, []
