"""Задача 3. Balanced Binary Tree: сбалансировано ли дерево по высоте."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class Node:
    value: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def is_balanced(root: Optional[Node]) -> bool:
    """True, если у каждого узла высоты левого и правого поддеревьев
    отличаются не больше чем на 1. Высота пустого дерева – 0, листа – 1.

    Обход снизу вверх (postorder): высота узла считается из уже известных
    высот детей, поэтому каждый узел обрабатывается один раз. На первом
    разбалансированном узле обход останавливается.

    Время O(n), память O(h): стек обхода – один путь от корня, а в словаре
    лежат высоты только тех поддеревьев, чей родитель ещё не обработан.
    """
    heights: Dict[int, int] = {}
    stack: List[Node] = []
    node = root
    last_visited: Optional[Node] = None
    while stack or node:
        if node:
            stack.append(node)
            node = node.left
            continue
        top = stack[-1]
        if top.right and top.right is not last_visited:
            node = top.right
            continue
        left_height = heights.pop(id(top.left), 0)
        right_height = heights.pop(id(top.right), 0)
        if abs(left_height - right_height) > 1:
            return False
        heights[id(top)] = 1 + max(left_height, right_height)
        last_visited = stack.pop()
    return True


def height(root: Optional[Node]) -> int:
    """Высота в узлах, обход в ширину."""
    level = [root] if root else []
    result = 0
    while level:
        result += 1
        level = [child for node in level for child in (node.left, node.right) if child]
    return result


def build_tree(values: Iterable[Any]) -> Optional[Node]:
    """Дерево из списка по уровням, None – пустое место: [1, 2, 3, None, 4]."""
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
        "сбалансированное": [1, 2, 3, 4, 5, None, 6, None, None, 7],
        "цепочка слева": [1, 2, 3, 4, None, None, None, 5],
        "перекос ниже корня": [1, 2, 3, 4, None, None, 5, 6, None, None, 7],
    }
    for name, values in examples.items():
        print(f"{name:20} {values} -> {is_balanced(build_tree(values))}")
