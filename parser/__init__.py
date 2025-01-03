import sys
import os

def prepare_parsers():
    res = {}

    sys.path.append(os.path.abspath('./parser'))

    for f in os.listdir('./parser'):
        if f == '__pycache__' or f == '__init__.py':
            continue

        module_name = f.split('.')[0]
        module = __import__('parser.%s' % module_name).__dict__[module_name]

        res[module.TYPE] = module.parse

    return res

parsers = prepare_parsers()
