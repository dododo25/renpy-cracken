import os
import pickle
import struct
import sys
import re
import zlib

from parser import parsers

DEFAULT_BLOCK_SIZE = 12

def collect_files(filepath) -> list[str]:
    if os.path.isfile(filepath):
        if re.fullmatch(r'^.*\.rpyc$', filepath):
            return filepath, 

        return ()
    
    res = []

    for path in os.listdir(filepath):
        res += collect_files(os.path.join(filepath, path))

    return res

def decompress_file(filepath: str) -> bytes | None:
    with open(filepath, 'rb') as file:
        header = file.read(10)

        if header != b'RENPY RPC2':
            return
        
        slot, start, length = None, None, None
        
        while not slot or slot > 1:
            slot, start, length = struct.unpack("III", file.read(DEFAULT_BLOCK_SIZE))

        if slot == 1:
            buf = bytearray(length)

            file.seek(start)
            file.readinto(buf)

            return zlib.decompress(buf)

        return None

def collect_blocks(decompressed: bytes, blocks: list[any]):
    obj_stack = pickle.loads(decompressed)[1]
    level = 0

    while len(obj_stack):
        obj = obj_stack.pop(0)
        obj_type = type(obj)

        if not obj_type in parsers:
            print('Unknown block %s' % (obj))
            continue

        block, new_level, parts = parsers[obj_type](obj, level)

        if not block is None:
            blocks.append(block)

        level = new_level
        obj_stack = parts + obj_stack

def filter_redundant_return_blocks(blocks: list[any]):
    last_block = blocks[-1]

    if last_block['level'] == 0 and last_block['type'] == 'return':
        del blocks[-1]

def filter_single_python_blocks(blocks: list[any]):
    i = 0

    while i < len(blocks) - 1:
        current_block = blocks[i]

        if current_block['type'] == 'python':
            n1_block = blocks[i + 1]
            n2_block = blocks[i + 2] if i < len(blocks) - 2 else None

            if n1_block['level'] > current_block['level'] and (n2_block is None or n2_block['level'] <= current_block['level']):
                del blocks[i]
                blocks[i] = {'type': 'code-single', 'value': '$ ' + n1_block['value'], 'level': n1_block['level'] - 1}
        
        i += 1

def filter_single_init_python_blocks(blocks: list[any]):
    i = 0

    while i < len(blocks) - 1:
        current_block = blocks[i]

        if current_block['type'] == 'init':
            m = re.match(r'python(\s+early)?:', blocks[i + 1]['value'])

            if m:
                if m.group(1):
                    current_block['value'] = 'init python%s:' % m.group(1)
                else:
                    current_block['value'] = 'init python:'

                del blocks[i + 1]

                i += 1

                while i < len(blocks):
                    next_block = blocks[i]

                    if next_block['level'] <= current_block['level']:
                        break

                    next_block['level'] -= 1
                    i += 1

                i -= 1

        i += 1

def filter_double_empty_blocks(blocks: list[any]):
    i = 0

    while i < len(blocks) - 1:
        if blocks[i]['value'] == '':
            while i < len(blocks) - 1:
                if blocks[i + 1]['value'] != '':
                    break

                del blocks[i + 1]
        
        i += 1

def filter_redundant_empty_blocks(blocks: list[any]):
    i = 1

    while i < len(blocks) - 1:
        if blocks[i]['value'] != '':
            i += 1
            continue

        blocks[i]['level'] = 0

        if blocks[i - 1]['type'] in ('init', 'python', 'code-single') \
            and blocks[i + 1]['type'] in ('elif', 'else', 'code', 'code-single'):
            del blocks[i]
            continue

        i += 1

    if blocks[0]['value'] == '':
        del blocks[0]

    if blocks[-1]['value'] == '':
        del blocks[-1]

def prepare_restored_file(file, blocks):
    restored_file = '.'.join(file.split('.')[:-1])

    if file.split('.')[-1] == 'rpyc':
        restored_file += '.rpy'

    with open(restored_file, 'w', encoding='utf-8') as wfile:
        for block in blocks:
            wfile.write(' ' * (block['level'] * 4) + block['value'] + '\n')

def main(*argv):
    files = collect_files(os.path.abspath(argv[0]))

    if not len(files):
        print('No files was found.')
        return

    for file in files:
        decompressed = decompress_file(file)

        if not decompressed:
            print('Unable to parse %s.' % file)

        blocks = []

        collect_blocks(decompressed, blocks)
        filter_redundant_return_blocks(blocks)
        filter_single_python_blocks(blocks)
        filter_single_init_python_blocks(blocks)
        filter_double_empty_blocks(blocks)
        filter_redundant_empty_blocks(blocks)
        prepare_restored_file(file, blocks)

if __name__ == '__main__':
    main(*sys.argv[1:])