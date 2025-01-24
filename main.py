import argparse
import loader
import logging
import os
import pickle
import re
import sys

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

def collect_files(filepath: str, filter = None) -> list[str]:
    if not os.path.exists(filepath):
        return []

    if os.path.isfile(filepath):
        if not filter or filter(filepath):
            return [filepath]

        return []

    res = []

    for path in os.listdir(filepath):
        res += collect_files(os.path.join(filepath, path))

    return res

def process_file(filepath: str, b: bytes):
    try:
        logger.info('trying to deserialize %s' % filepath)

        data = pickle.loads(b)[1]

        if data is None:
            logger.error('unable to parse %s' % filepath)
            return

        blocks = []

        collect_blocks(data, blocks)
        prepare_levels(blocks)
        filter_redundant_return_blocks(blocks)
        filter_single_python_blocks(blocks)
        #filter_single_init_python_blocks(blocks)
        prepare_restored_file(filepath, blocks)
    except (ModuleNotFoundError, AttributeError) as e:
        logger.critical(e)
        raise e

def process_archive_file(filepath: str, b: bytes):
    logger.info('trying to extract %s' % filepath)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'wb') as file:
        file.write(b)

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
            parsed    = Element(type=parsed.type, value=parsed.value)

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

def main(file, recursive, clear):
    archive_files = collect_files(os.path.abspath(file), loader.is_archive)
    regular_files = []

    archive_files_found = len(archive_files) > 0

    while archive_files:
        filepath = archive_files.pop()
        parts, _ = loader.load_archive(filepath)

        for key, value in parts.items():
            full_path = os.path.join(*os.path.split(filepath)[:-1], *key.split('/'))

            process_archive_file(full_path, value)

            if not recursive:
                continue

            if loader.is_archive(full_path):
                archive_files.append(full_path)
            elif loader.is_file(full_path):
                regular_files.append(full_path)

        if clear:
            os.remove(filepath)

    regular_files += collect_files(os.path.abspath(filepath), loader.is_file)

    if len(regular_files) or archive_files_found:
        for file in regular_files:
            process_file(file, loader.load_file(file))

        logger.info('done')
    else:
        logger.warning('no files were found')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='cracker.py', 
                                     description='Decompile RenPy files and extract additional files from a RenPy archive')
    
    parser.add_argument('-r', '--recursive', help='Process files that were extracted from archives', action='store_true')
    parser.add_argument('-c', '--clear', help='Delete archive files after they were processed', action='store_true')
    parser.add_argument('file', help='Path to file \\ folder that this program should process')

    args = parser.parse_args()
    
    main(args.file, args.recursive, args.clear)
