import argparse
import re

import loader
import logging
import os
import pickle

import mommy
from renpy.ast import EarlyPython, Init, Node, Python, Return, RootNode, TreeIterBlockEnd, ValuedNode, Image, \
    TreeList, If

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FILE_COMMENT = '''
# This file was created using renpy-cracker
# https://github.com/dododo25/renpy-kracker
'''

def collect_files(filepath: str, filter = None) -> list[str]:
    if not os.path.exists(filepath):
        return []

    if os.path.isfile(filepath):
        if not filter or filter(filepath):
            return [filepath]

        return []

    res = []

    for path in os.listdir(filepath):
        res += collect_files(os.path.join(filepath, path), filter)

    return res

def process_file(filepath: str, b: bytes, prettify: bool):
    try:
        logger.info('trying to deserialize %s' % filepath)

        tree = RootNode(pickle.loads(b)[1])

        filter_tree(tree)
        prepare_python_code_snippets(tree, prettify)
        filter_simple_python_blocks(tree)
        filter_single_init_python_blocks(tree)
        separate_nodes(tree)
        prepare_image_nodes(tree, prettify)
        prepare_restored_file(filepath, tree)
    except (ModuleNotFoundError, AttributeError) as e:
        logger.critical(e)
        raise e

def process_archive_file(filepath: str, b: bytes):
    logger.info('trying to extract %s' % filepath)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'wb') as file:
        file.write(b)

def filter_tree(tree: Node):
    nodes_to_remove = []

    for node in tree:
        if hasattr(node, 'nexclude') and node.nexclude:
            nodes_to_remove.append(node)

    if isinstance(tree.nchildren[-1], Return):
        nodes_to_remove.append(tree.nchildren[-1])

    for node in nodes_to_remove:
        index = node.nparent.nchildren.index(node)
        node.nparent.nchildren.remove(node)

        if not node.nchildren:
            continue

        for shift, child in enumerate(node.nchildren):
            node.nparent.nchildren.insert(index + shift, child)

def prepare_python_code_snippets(tree: Node, prettify: bool):
    last_node = None

    for node in tree:
        if isinstance(last_node, Node) and isinstance(node, str):
            index = last_node.nchildren.index(node)
            last_node.nchildren.remove(node)

            code = mommy.clean(node) if prettify else node

            for shift, part in enumerate(code.split('\n')):
                last_node.nchildren.insert(index + shift, ValuedNode(part))

        last_node = node

def filter_simple_python_blocks(tree: Node):
    for node in tree:
        if not isinstance(node, (Python, EarlyPython)):
            continue

        if len(node.nchildren) == 1 and re.match(r'python(\s+early)?:', str(node)):
            parent_node = node.nparent
            index = parent_node.nchildren.index(node)

            del parent_node.nchildren[index]

            for shift, child in enumerate(node.nchildren):
                new_value = ''

                if child.value != '':
                    new_value = '$ ' + child.value

                parent_node.nchildren.insert(index + shift, ValuedNode(new_value))

def filter_single_init_python_blocks(tree: Node):
    for node in tree:
        node_parent = node.nparent

        if isinstance(node_parent, Init) and len(node_parent.nchildren) == 1 \
                and isinstance(node, (Python, EarlyPython)):
            node_parent_parent = node_parent.nparent
            index = node_parent_parent.nchildren.index(node_parent)

            node_parent_parent.nchildren.remove(node_parent)
            node_parent_parent.nchildren.insert(index, ValuedNode(
                '%s %s:' % (str(node_parent)[:-1], str(node)[:-1]), children=node.nchildren))

def separate_nodes(tree: Node):
    checked_nodes = set()

    for node in tree:
        if isinstance(node, If.Part) and not (node in checked_nodes):
            children_len = len(node.nparent.nchildren)
            index = node.nparent.nchildren.index(node)

            if re.match(r'^if.*:', node.value) and index > 0:
                node.nparent.nchildren.insert(index, ValuedNode(''))
            elif node.value == 'else:' and index < children_len - 1:
                node.nparent.nchildren.insert(index + 1, ValuedNode(''))

            checked_nodes.add(node)

    for index in range(1, len(tree.nchildren) * 2 - 1, 2):
        tree.nchildren.insert(index, ValuedNode(''))

def prepare_image_nodes(tree: Node, prettify: bool):
    def map_code(value):
        if re.match(r'\s{4}.*', value):
            value = value[4:]

        return ValuedNode(value)

    for node in tree:
        if not isinstance(node, Image) or node.atl:
            continue

        parts = (mommy.clean(node.nchildren[0].value) if prettify else node.nchildren[0].value).split('\n')

        node.value = parts[0]
        node.nchildren = TreeList(list(map(map_code, parts[1:])), node)

def prepare_restored_file(file, tree):
    restored_file = '.'.join(file.split('.')[:-1])

    if file.split('.')[-1] == 'rpyc':
        restored_file += '.rpy'
    elif file.split('.')[-1] == 'rpymc':
        restored_file += '.rpym'

    with open(restored_file, 'w', encoding='utf-8') as wfile:
        level = 0

        for node in tree:
            if isinstance(node, TreeIterBlockEnd):
                level -= 1
            elif not isinstance(node, RootNode):
                value = str(node)

                if value != '':
                    wfile.write(' ' * (level * 4) + str(node))

                wfile.write('\n')
                level += 1

        if level == -1:
            wfile.write(FILE_COMMENT)
        else:
            wfile.write(FILE_COMMENT[1:])

def main(file, recursive, clear, prettify):
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

    regular_files += collect_files(os.path.abspath(file), loader.is_file)

    if len(regular_files) or archive_files_found:
        for file in regular_files:
            process_file(file, loader.load_file(file), prettify)

        logger.info('done')
    else:
        logger.warning('no files were found')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='cracker.py', 
                                     description='Decompile RenPy files and extract additional files from a RenPy archive')

    parser.add_argument('-r', '--recursive', help='Process files that were extracted from archives', action='store_true')
    parser.add_argument('-c', '--clear', help='Delete archive files after they were processed', action='store_true')
    parser.add_argument('-p', '--prettify', help='Try to make Python code snippets more pretty', action='store_true')
    parser.add_argument('file', help='Path to file \\ folder that this program should process')

    args = parser.parse_args()

    main(args.file, args.recursive, args.clear, args.prettify)
