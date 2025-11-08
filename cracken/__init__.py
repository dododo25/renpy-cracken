import loader
import logging
import io
import os
import pickle
import re

from . import mommy
from renpy import EmptyLine, RootNode, TreeIterBlockEnd, TreeList, TreeNode, ValuedNode
from renpy.ast import Define, EarlyPython, Image, Init, Python, Return, Style, Transform
from renpy.sl2.slast import SLPython

FILE_COMMENT = '''
# This file was reconstructed by renpy-cracken
# https://github.com/dododo25/renpy-cracken
'''

is_file = loader.is_file
is_archive = loader.is_archive

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if module.split('.')[0] == 'renpy':
            return super().find_class(module, name)

        logger.warning('Loading from %s is not allowed.' % module)
        return None

def collect_files(filepath: str, callback):
    if not os.path.exists(filepath):
        return

    if callback and os.path.isfile(filepath):
        callback(filepath)
        return

    for path in os.listdir(filepath):
        collect_files(os.path.join(filepath, path), callback)

def process_archive_file(filepath: str, recursive: bool, callback):
    parts, _ = loader.load_archive(filepath)

    for key, value in parts.items():
        full_path = os.path.join(*os.path.split(filepath)[:-1], *key.split('/'))

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb') as file:
            file.write(value)

        if not recursive:
            continue

        if callback and os.path.isfile(full_path):
            callback(full_path)

def process_file(filepath: str, prettify: bool):
    bytes = io.BytesIO(loader.load_file(filepath))
    unpickler = RestrictedUnpickler(bytes)

    tree = RootNode(unpickler.load()[1])

    remove_excluded_nodes(tree)
    remove_excessive_empty_lines(tree)
    prepare_python_code_snippets(tree, prettify)
    filter_simple_python_blocks(tree)
    filter_simple_init_blocks(tree)
    filter_simple_init_python_blocks(tree)
    prepare_image_nodes(tree, prettify)
    prepare_restored_file(filepath, tree)

def remove_excluded_nodes(tree: TreeNode):
    nodes_to_remove = set()

    for node in tree:
        if hasattr(node, 'nexclude') and node.nexclude:
            nodes_to_remove.add(node)

    if len(tree.nchildren) >= 2 and isinstance(tree.nchildren[-2], Return):
        nodes_to_remove.add(tree.nchildren[-2])

    for node in nodes_to_remove:
        index = node.nparent.nchildren.index(node)
        node.nparent.nchildren.remove(node)

        if not node.nchildren:
            continue

        for shift, child in enumerate(node.nchildren):
            node.nparent.nchildren.insert(index + shift, child)

def remove_excessive_empty_lines(tree: TreeNode):
    nodes_to_remove = []

    for node in tree:
        current = node

        new_nodes_to_remove = []

        while isinstance(current, TreeNode) and current.nchildren:
            for child in current.nchildren[::-1]:
                if not isinstance(child, EmptyLine):
                    break

                new_nodes_to_remove.append(child)

            current = child

        if len(new_nodes_to_remove) > 1:
            nodes_to_remove += new_nodes_to_remove[1:]

    if isinstance(tree, TreeNode) \
        and tree.nchildren \
        and isinstance(tree.nchildren[-1], EmptyLine):
        nodes_to_remove.append(tree.nchildren[-1])

    for n in nodes_to_remove:
        if n in n.nparent.nchildren:
            n.nparent.nchildren.remove(n)

def prepare_python_code_snippets(tree: TreeNode, prettify: bool):
    nodes = []

    for node in tree:
        if isinstance(node, TreeIterBlockEnd):
            nodes.pop()
        elif isinstance(node, TreeNode):
            nodes.append(node)
        elif isinstance(node, str):
            last_node = nodes[-1]

            index = last_node.nchildren.index(node)
            last_node.nchildren.remove(node)

            code = mommy.clean(node) if prettify else node

            for shift, part in enumerate(code.split('\n')):
                last_node.nchildren.insert(index + shift, ValuedNode(part))

def filter_simple_python_blocks(tree: TreeNode):
    for node in tree:
        if not isinstance(node, (Python, EarlyPython, SLPython)):
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

def filter_simple_init_blocks(tree: TreeNode):
    for node in tree:
        node_parent = node.nparent

        if isinstance(node_parent, Init) \
                and str(node_parent) == 'init:' \
                and len(node_parent.nchildren) == 2 \
                and isinstance(node, (Define, Style, Transform)):
            if isinstance(node, Style) and node.nchildren:
                continue

            node_parent_parent = node_parent.nparent
            index = node_parent_parent.nchildren.index(node_parent)

            node_parent_parent.nchildren.remove(node_parent)
            node_parent_parent.nchildren.insert(index, ValuedNode(str(node), children=node.nchildren))

def filter_simple_init_python_blocks(tree: TreeNode):
    for node in tree:
        node_parent = node.nparent

        if isinstance(node_parent, Init) \
                and len(node_parent.nchildren) == 2 \
                and isinstance(node, (Python, EarlyPython)):
            node_parent_parent = node_parent.nparent
            index = node_parent_parent.nchildren.index(node_parent)

            node_parent_parent.nchildren.remove(node_parent)
            node_parent_parent.nchildren.insert(index, ValuedNode(
                '%s %s' % (str(node_parent)[:-1], str(node)), children=node.nchildren[1:]))

def prepare_image_nodes(tree: TreeNode, prettify: bool):
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

        if level == -1 and len(tree.nchildren):
            wfile.write(FILE_COMMENT)
        else:
            wfile.write(FILE_COMMENT[1:])
