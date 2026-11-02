class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


def _height(node):
    return node.height if node else 0


def _update(node):
    node.height = 1 + max(_height(node.left), _height(node.right))


def _rotate_right(node):
    new_root = node.left
    node.left = new_root.right
    new_root.right = node
    _update(node)
    _update(new_root)
    return new_root


def _rotate_left(node):
    new_root = node.right
    node.right = new_root.left
    new_root.left = node
    _update(node)
    _update(new_root)
    return new_root


def _balance(node):
    _update(node)
    factor = _height(node.left) - _height(node.right)
    if factor > 1:
        if _height(node.left.left) < _height(node.left.right):
            node.left = _rotate_left(node.left)
        return _rotate_right(node)
    if factor < -1:
        if _height(node.right.right) < _height(node.right.left):
            node.right = _rotate_right(node.right)
        return _rotate_left(node)
    return node


class AVL:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def __contains__(self, key):
        return self.search(key)

    def insert(self, key):
        def visit(node):
            if node is None:
                return Node(key), True
            if key == node.key:
                return node, False
            if key < node.key:
                node.left, added = visit(node.left)
            else:
                node.right, added = visit(node.right)
            return _balance(node), added

        self.root, added = visit(self.root)
        self._size += added
        return added

    def delete(self, key):
        def visit(node, value):
            if node is None:
                return None, False
            if value < node.key:
                node.left, removed = visit(node.left, value)
            elif value > node.key:
                node.right, removed = visit(node.right, value)
            else:
                if node.left is None:
                    return node.right, True
                if node.right is None:
                    return node.left, True
                successor = node.right
                while successor.left:
                    successor = successor.left
                node.key = successor.key
                node.right, _ = visit(node.right, successor.key)
                removed = True
            return _balance(node), removed

        self.root, removed = visit(self.root, key)
        self._size -= removed
        return removed

    def inorder(self):
        def visit(node):
            if node:
                yield from visit(node.left)
                yield node.key
                yield from visit(node.right)

        return list(visit(self.root))

    def visualize(self):
        lines = []

        def visit(node, prefix, label):
            if node is None:
                lines.append(f"{prefix}{label}.")
                return
            lines.append(f"{prefix}{label}{node.key} (h={node.height})")
            if node.left or node.right:
                visit(node.left, prefix + "  ", "L: ")
                visit(node.right, prefix + "  ", "R: ")

        visit(self.root, "", "")
        return "\n".join(lines)


if __name__ == "__main__":
    tree = AVL()
    for value in (30, 10, 20, 40, 50):
        tree.insert(value)
        print(f"insert {value}\n{tree.visualize()}\n")
    tree.delete(10)
    print(f"delete 10\n{tree.visualize()}")
