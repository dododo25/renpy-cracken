from block import EmptyLine

TYPE = EmptyLine

def parse(obj, level):
    return {'type': 'empty', 'level': level, 'value': ''}, level, []
