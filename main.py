import decompressor
import logging
import os
import sys
import re

from parser import parse
from parser.block import Container, Element

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FILE_COMMENT = '''
# This file was created using renpy-cracker
# https://github.com/dododo25/renpy-kracker
'''

class LevelUp:

    pass

class LevelDown:

    pass

def collect_files(filepath) -> list[str]:
    if os.path.isfile(filepath):
        if re.fullmatch(r'^.*\.rpyc$', filepath):
            return filepath, 

        return ()
    
    res = []

    for path in os.listdir(filepath):
        res += collect_files(os.path.join(filepath, path))

    return res

def collect_blocks(obj_stack, blocks: list[any]):
    while len(obj_stack):
        obj = obj_stack.pop(0)
        obj_type = type(obj)

        if obj_type in [LevelDown, LevelUp]:
            blocks.append(obj)
            continue

        parsed = parse(obj)

        if not parsed:
            logger.warning('Unknown block type %s.%s' % (obj.__module__, obj.__class__.__name__))
            continue

        if type(parsed) == Container:
            obj_stack = [LevelUp(), *parsed.children, LevelDown(), *obj_stack]

        if parsed.type != 'INVALID':
            blocks.append(parsed)

def prepare_levels(blocks: list[any]):
    level = 0
    i = 0

    while i < len(blocks):
        obj = blocks[i]
        obj_type = type(obj)

        if obj_type in [LevelDown, LevelUp]:
            del blocks[i]

            if obj_type == LevelDown:
                level -= 1
            else:
                level += 1
        else:
            obj.level = level
            i += 1

def filter_redundant_return_blocks(blocks: list[any]):
    last_block = blocks[-1]

    if last_block.level == 0 and last_block.type == 'return':
        del blocks[-1]

def filter_single_python_blocks(blocks: list[any]):
    i = 0

    while i < len(blocks) - 1:
        current_block = blocks[i]

        if current_block.type == 'python':
            n1_block = blocks[i + 1]
            n2_block = blocks[i + 2] if i < len(blocks) - 2 else None

            if n1_block.level > current_block.level and (n2_block is None or n2_block.level <= current_block.level):
                del blocks[i]
                blocks[i] = Element(type='code-single', value='$ ' + n1_block.value, level=n1_block.level - 1)
        
        i += 1

def filter_single_init_python_blocks(blocks: list[any]):
    i = 0

    while i < len(blocks) - 1:
        current_block = blocks[i]

        if current_block.type == 'init':
            m = re.match(r'python(\s+early)?:', blocks[i + 1].value)

            if m:
                if m.group(1):
                    current_block.value = 'init python%s:' % m.group(1)
                else:
                    current_block.value = 'init python:'

                del blocks[i + 1]

                i += 1

                while i < len(blocks):
                    next_block = blocks[i]

                    if next_block.level <= current_block.level:
                        break

                    next_block.level -= 1
                    i += 1

                i -= 1

        i += 1

def prepare_restored_file(file, blocks):
    restored_file = '.'.join(file.split('.')[:-1])

    if file.split('.')[-1] == 'rpyc':
        restored_file += '.rpy'

    with open(restored_file, 'w', encoding='utf-8') as wfile:
        for block in blocks:
            wfile.write(' ' * (block.level * 4) + block.value + '\n')

        wfile.write(FILE_COMMENT)

def main(*argv):
    files = collect_files(os.path.abspath(argv[0]))

    if not len(files):
        logger.warning('no files were found')
        return
    
    for file in files:
        try:
            logger.info('trying to deserialize %s' % file)

            decompressed = decompressor.decompress(file)

            if not decompressed:
                logger.error('Unable to parse %s' % file)
                continue

            blocks = []

            collect_blocks(decompressed, blocks)
            prepare_levels(blocks)
            filter_redundant_return_blocks(blocks)
            filter_single_python_blocks(blocks)
            filter_single_init_python_blocks(blocks)
            prepare_restored_file(file, blocks)
        except (ModuleNotFoundError, AttributeError) as e:
            logger.critical(e)

    logger.info('done')

if __name__ == '__main__':
    main(*sys.argv[1:])