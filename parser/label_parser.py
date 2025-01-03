from block import EmptyLine, Label, LevelDown, LevelUp

TYPE = Label

def parse(obj, level):
    return {'type': 'label', 'level': level, 'value': obj.value + ':'}, level, [LevelUp(), *obj.block, LevelDown(), EmptyLine()]
