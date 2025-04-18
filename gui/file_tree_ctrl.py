import os
import re
import wx

from tree import Node, TreeIterBlockEnd

class FileTreeCtrl(wx.TreeCtrl):

    def __init__(self,
                 parent=None,
                 id=wx.ID_ANY,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.TR_DEFAULT_STYLE,
                 validator=wx.DefaultValidator,
                 name=wx.TreeCtrlNameStr,
                 pattern=None):
        super().__init__(parent, id, pos, size, style | wx.TR_HIDE_ROOT, validator, name)

        self.root_item = self.AddRoot('root')
        self.root_node = Node('.', [])
        self.pattern = pattern

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown, self)

    # noinspection PyPep8Naming
    def OnKeyDown(self, event):
        if event.GetKeyCode() != wx.WXK_DELETE:
            return

        selection = self.GetSelection()

        if selection:
            self.RemoveFileItem(selection)

    # noinspection PyPep8Naming
    def FindFileItem(self, filepath):
        item = self.root_item
        parts = FileTreeCtrl._split_path(filepath)

        while parts:
            child, _ = self.GetFirstChild(item)

            while child.IsOk():
                item_parts = FileTreeCtrl._split_path(self.GetItemText(child))

                if parts[:len(item_parts)] == item_parts:
                    parts = parts[len(item_parts):]
                    item = child
                    break

                child = self.GetNextSibling(child)
            else:
                return None

        return item

    # noinspection PyPep8Naming
    def ExpandFileItem(self, filepath):
        items_to_expand = [self.root_item]
        parts = FileTreeCtrl._split_path(filepath)

        while parts:
            child, _ = self.GetFirstChild(items_to_expand[-1])

            while child.IsOk():
                item_parts = FileTreeCtrl._split_path(self.GetItemData(child)['ref'].value)

                if parts[:len(item_parts)] == item_parts:
                    parts = parts[len(item_parts):]
                    items_to_expand.append(child)
                    break

                child = self.GetNextSibling(child)
            else:
                return

        for item in items_to_expand[1:]:
            self.Expand(item)

    # noinspection PyPep8Naming
    def AppendFileItem(self, filepath):
        if not re.match(self.pattern, filepath):
            return

        self._append_to_tree(filepath)
        self._prepare_items()
        self.ExpandFileItem(filepath)

    # noinspection PyPep8Naming
    def AppendDirSubItems(self, dirpath):
        dirs_stack = [dirpath]

        while dirs_stack:
            current_dir = dirs_stack.pop(0)
            index = 0

            for file in os.listdir(current_dir):
                full_path = os.path.join(current_dir, file)

                if os.path.isfile(full_path):
                    if re.match(self.pattern, full_path):
                        self._append_to_tree(full_path)
                else:
                    dirs_stack.insert(index, full_path)
                    index += 1

        self._prepare_items()
        self.ExpandFileItem(dirpath)

    # noinspection PyPep8Naming
    def RemoveFileItem(self, obj):
        if not isinstance(obj, wx.TreeItemId):
            return

        data = self.GetItemData(obj)

        node   = data['ref']
        item_parent = data['parent']

        if not node:
            return

        node.parent.children.remove(node)
        self.Delete(obj)

        while item_parent:
            parent_data = self.GetItemData(item_parent)

            if not parent_data or len(parent_data['ref'].children):
                break

            parent_data['ref'].parent.children.remove(parent_data['ref'])
            self.Delete(item_parent)
            item_parent = parent_data['parent']

        if self.GetItemData(item_parent):
            self.Expand(item_parent)

    def _append_to_tree(self, path):
        parts = FileTreeCtrl._split_path(path)
        node = self.root_node

        while parts and node.children:
            part = parts[0]

            for index, child in enumerate(node.children):
                if child.value == part:
                    break
            else:
                break

            parts.pop(0)
            node = node.children[index]

        for part in parts:
            new_node = Node(part, None if re.match(self.pattern, part) else [])

            for index, child in enumerate(node.children):
                if self._compare(child.value, part) < 0:
                    node.children.insert(index, new_node)
                    break
            else:
                node.children.append(new_node)

            node = new_node

    def _prepare_items(self):
        self.DeleteChildren(self.root_item)

        items_stack = [self.root_item]

        for index, node in enumerate(self.root_node):
            if index == 0:
                continue

            if isinstance(node, TreeIterBlockEnd):
                items_stack.pop()
            elif node.children:
                new_item = self.AppendItem(items_stack[-1], '📂 ' + node.value)
                self.SetItemData(new_item, {'ref': node, 'parent': items_stack[-1]})
                items_stack.append(new_item)
            else:
                new_item = self.AppendItem(items_stack[-1], '📄 ' + node.value)
                self.SetItemData(new_item, {'ref': node, 'parent': items_stack[-1]})

    def _compare(self, n1, n2):
        m1 = re.match(self.pattern, n1)
        m2 = re.match(self.pattern, n2)

        if (m1 and m2) or not (m1 or m2):
            if n1 > n2:
                return -1
            elif n1 < n2:
                return 1
            else:
                return 0

        if m1:
            return -1

        return 1

    @staticmethod
    def _split_path(path):
        res = []
        head, tail = os.path.split(path)

        while tail:
            res.insert(0, tail)
            head, tail = os.path.split(head)

        if head:
            res.insert(0, head)

        return res
