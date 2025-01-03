from block import CodePart

TYPE = CodePart

def parse(obj, level):
    return {'type': 'code', 'level': level, 'value': obj.value}, level, []
