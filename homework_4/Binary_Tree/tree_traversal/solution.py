"""Задача 1. Tree Traversal: бинарное дерево поиска и шесть обходов.

Все операции написаны итеративно: в вырожденном дереве (вставка
отсортированной последовательности) высота равна n, и рекурсия
упёрлась бы в лимит интерпретатора (~1000 вызовов).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Optional


@dataclass
class Node:
    value: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None


class BST:
    """Бинарное дерево поиска без повторов.

    Свойство BST: для любого узла все значения в левом поддереве
    меньше значения узла, все значения в правом – больше.
    Повторная вставка существующего значения ничего не меняет.
    """

    def __init__(self, values: Iterable[Any] = ()) -> None:
        self.root: Optional[Node] = None
        self._size = 0
        for value in values:
            self.insert(value)

    def __len__(self) -> int:
        return self._size

    def insert(self, value: Any) -> bool:
        """Вставляет значение. Возвращает False, если оно уже было в дереве.

        Время O(h), память O(1), где h – высота дерева.
        """
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            self._size = 1
            return True

        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    break
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = new_node
                    break
                current = current.right
            else:
                return False
        self._size += 1
        return True

    def __contains__(self, value: Any) -> bool:
        current = self.root
        while current is not None:
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return True
        return False

    def height(self) -> int:
        """Высота в узлах: пустое дерево – 0, один узел – 1. Обход в ширину."""
        if self.root is None:
            return 0
        level = [self.root]
        height = 0
        while level:
            height += 1
            level = [child for node in level for child in (node.left, node.right) if child]
        return height

    # Прямые обходы.

    def preorder(self) -> List[Any]:
        """Узел → левое → правое (NLR)."""
        return _preorder(self.root, reverse=False)

    def inorder(self) -> List[Any]:
        """Левое → узел → правое (LNR). Для BST – значения по возрастанию."""
        return _inorder(self.root, reverse=False)

    def postorder(self) -> List[Any]:
        """Левое → правое → узел (LRN)."""
        return _postorder(self.root, reverse=False)

    # Обратные обходы: те же схемы, но правое поддерево раньше левого.

    def reverse_preorder(self) -> List[Any]:
        """Узел → правое → левое (NRL)."""
        return _preorder(self.root, reverse=True)

    def reverse_inorder(self) -> List[Any]:
        """Правое → узел → левое (RNL). Для BST – значения по убыванию."""
        return _inorder(self.root, reverse=True)

    def reverse_postorder(self) -> List[Any]:
        """Правое → левое → узел (RLN)."""
        return _postorder(self.root, reverse=True)


def _children(node: Node, reverse: bool):
    """Дети в порядке посещения: (первый, второй)."""
    return (node.right, node.left) if reverse else (node.left, node.right)


def _preorder(root: Optional[Node], reverse: bool) -> List[Any]:
    result: List[Any] = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        result.append(node.value)
        first, second = _children(node, reverse)
        # Стек – LIFO: кладём сначала того, кого посетим вторым.
        if second:
            stack.append(second)
        if first:
            stack.append(first)
    return result


def _inorder(root: Optional[Node], reverse: bool) -> List[Any]:
    result: List[Any] = []
    stack: List[Node] = []
    node = root
    while stack or node:
        # Спускаемся до упора в «первую» сторону, запоминая путь.
        while node:
            stack.append(node)
            node = _children(node, reverse)[0]
        node = stack.pop()
        result.append(node.value)
        node = _children(node, reverse)[1]
    return result


def _postorder(root: Optional[Node], reverse: bool) -> List[Any]:
    result: List[Any] = []
    stack: List[Node] = []
    node = root
    last_visited: Optional[Node] = None
    while stack or node:
        if node:
            stack.append(node)
            node = _children(node, reverse)[0]
            continue
        top = stack[-1]
        second = _children(top, reverse)[1]
        # Во второе поддерево идём один раз: если оттуда только что вернулись,
        # узел готов к выводу.
        if second and second is not last_visited:
            node = second
        else:
            result.append(top.value)
            last_visited = stack.pop()
    return result


def to_text(tree: BST) -> str:
    """Схема дерева «лёжа»: корень слева, правое поддерево сверху."""
    if tree.root is None:
        return "(пустое дерево)"
    lines: List[str] = []
    # (узел, отступ, ветка, отступ для правого ребёнка, отступ для левого)
    stack = [(tree.root, "", "", "", "")]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            lines.append(item)
            continue
        node, prefix, branch, right_prefix, left_prefix = item
        # Порядок вывода: правое поддерево, узел, левое (reverse inorder).
        if node.left:
            stack.append((node.left, left_prefix, "└── ", left_prefix + "│   ", left_prefix + "    "))
        stack.append(prefix + branch + str(node.value))
        if node.right:
            stack.append((node.right, right_prefix, "┌── ", right_prefix + "    ", right_prefix + "│   "))
    return "\n".join(lines)


if __name__ == "__main__":
    example = BST([8, 3, 10, 1, 6, 14, 4, 7, 13])
    print(to_text(example), end="\n\n")
    for name in ("preorder", "inorder", "postorder",
                 "reverse_preorder", "reverse_inorder", "reverse_postorder"):
        print(f"{name:18} {getattr(example, name)()}")
