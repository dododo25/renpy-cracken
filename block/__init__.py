class LevelUp:

    pass

class LevelDown:

    pass

class EmptyLine:

    pass

class CodePart:

    def __init__(self, level, value):
        self.level = level
        self.value = value

class Label:

    def __init__(self, value, block):
        self.value = value
        self.block = block

class IfPart:

    def __init__(self, type, condition, block):
        self.type = type
        self.condition = condition
        self.block = block