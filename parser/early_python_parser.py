import renpy
import re

from block import CodePart, EmptyLine, LevelUp, LevelDown

TYPE = renpy.ast.EarlyPython

def parse(obj, level):
    return {'type': 'python', 'level': level, 'value': prepare_value(obj)}, level, prepare_parts(obj, level)

def prepare_value(obj):
    res = 'python early'

    if obj.hide:
        res += ' hide'

    m = re.match(r'store(\.(.+))?', obj.store)

    if m and m.group(1):
        res += ' in %s' % m.group(2)

    return res + ':'

def prepare_parts(obj, level):
    res = [LevelUp()]

    for v in obj.code.source.split('\n'):
        if v.strip() == '':
            res.append(EmptyLine())
        else:
            res.append(CodePart(level, v))

    return res + [LevelDown(), EmptyLine()]