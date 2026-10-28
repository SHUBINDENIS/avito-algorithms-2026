"""Задача 2. Validate BST: является ли произвольное бинарное дерево деревом поиска."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional


@dataclass
class Node:
    value: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def is_valid_bst(root: Optional[Node]) -> bool:
    """True, если для каждого узла всё левое поддерево строго меньше узла,
    а всё правое – строго больше. Повторы значений делают дерево некорректным.

    Каждый узел проверяется против интервала (low, high), который задают
    его предки: уходя влево, сужаем верхнюю границу, вправо – нижнюю.
    Граница None – «нет ограничения», поэтому подходят любые сравнимые
    значения, без бесконечностей-заглушек.

    Время O(n), память O(h): стек хранит не больше одного пути от корня
    плюс правых соседей вдоль него.
    """
    stack = [(root, None, None)]
    while stack:
        node, low, high = stack.pop()
        if node is None:
            continue
        if low is not None and not node.value > low:
            return False
        if high is not None and not node.value < high:
            return False
        stack.append((node.right, node.value, high))
        stack.append((node.left, low, node.value))
    return True


def build_tree(values: Iterable[Any]) -> Optional[Node]:
    """Дерево из списка по уровням, None – пустое место: [5, 3, 7, None, 6]."""
    values = list(values)
    if not values or values[0] is None:
        return None
    root = Node(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        parent = queue[head]
        head += 1
        for side in ("left", "right"):
            if i < len(values) and values[i] is not None:
                child = Node(values[i])
                setattr(parent, side, child)
                queue.append(child)
            i += 1
    return root


if __name__ == "__main__":
    examples = {
        "корректное": [8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13],
        "6 в левом поддереве 5": [5, 3, 8, 1, 6],
        "повтор": [2, 2],
    }
    for name, values in examples.items():
        print(f"{name:24} {values} -> {is_valid_bst(build_tree(values))}")
