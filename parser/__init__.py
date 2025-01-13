import os

PARSERS = {}

for f in os.listdir('./parser'):
    if f in ('__pycache__', '__init__.py', 'block', 'test'):
        continue

    module_name = f.split('.')[0]
    module = __import__('parser.%s' % module_name).__dict__[module_name]

    PARSERS[module.TYPE] = module.parse

def parse(obj):
    if not type(obj) in PARSERS:
        return None
    
    return PARSERS[type(obj)](obj)
