import random
import sys
import unittest

from pathlib import Path
from runpy import run_path

_solution = run_path(str(Path(__file__).with_name("solution.py")))
Node = _solution["Node"]
is_valid_bst = _solution["is_valid_bst"]
build_tree = _solution["build_tree"]


def inorder(node):
    out, stack = [], []
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.value)
        node = node.right
    return out


def reference(root):
    """Независимый способ: inorder корректного BST строго возрастает."""
    values = inorder(root)
    return all(a < b for a, b in zip(values, values[1:]))


def insert(root, value):
    if root is None:
        return Node(value)
    node = root
    while True:
        side = "left" if value < node.value else "right"
        child = getattr(node, side)
        if child is None:
            setattr(node, side, Node(value))
            return root
        node = child


def random_shape(rng, values):
    """Дерево случайной формы со значениями в случайном порядке."""
    if not values:
        return None
    nodes = [Node(v) for v in values]
    for i in range(1, len(nodes)):
        while True:
            parent = nodes[rng.randrange(i)]
            side = rng.choice(("left", "right"))
            if getattr(parent, side) is None:
                setattr(parent, side, nodes[i])
                break
    return nodes[0]


class ExamplesTest(unittest.TestCase):
    def test_valid_example(self):
        #        8
        #      /   \
        #     3     10
        #    / \      \
        #   1   6      14
        #      / \     /
        #     4   7   13
        root = build_tree([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13])
        self.assertTrue(is_valid_bst(root))

    def test_child_is_fine_locally_but_breaks_ancestor(self):
        # 6 > 3 – для родителя всё верно, но 6 в левом поддереве 5.
        self.assertFalse(is_valid_bst(build_tree([5, 3, 8, 1, 6])))
        # Зеркально: 4 < 8, но 4 в правом поддереве 5.
        self.assertFalse(is_valid_bst(build_tree([5, 3, 8, None, None, 4, 9])))

    def test_deep_violation(self):
        # 9 нарушает границу корня 8 через три уровня.
        root = build_tree([8, 3, 10, 1, 6, None, 14, None, None, 4, 9, 13])
        self.assertFalse(is_valid_bst(root))

    def test_children_swapped(self):
        self.assertFalse(is_valid_bst(build_tree([2, 3, 1])))


class EdgeCasesTest(unittest.TestCase):
    def test_empty_tree(self):
        self.assertTrue(is_valid_bst(None))
        self.assertIsNone(build_tree([]))
        self.assertIsNone(build_tree([None]))

    def test_single_node(self):
        self.assertTrue(is_valid_bst(Node(0)))

    def test_two_nodes(self):
        self.assertTrue(is_valid_bst(build_tree([2, 1])))
        self.assertTrue(is_valid_bst(build_tree([2, None, 3])))
        self.assertFalse(is_valid_bst(build_tree([2, 3])))
        self.assertFalse(is_valid_bst(build_tree([2, None, 1])))

    def test_duplicates_are_invalid(self):
        self.assertFalse(is_valid_bst(build_tree([2, 2])))
        self.assertFalse(is_valid_bst(build_tree([2, None, 2])))
        # Повтор далёкого предка тоже ловится: 5 справа от 3, но равно корню.
        self.assertFalse(is_valid_bst(build_tree([5, 3, 8, None, 5])))

    def test_extreme_values_without_sentinels(self):
        big, small = sys.maxsize, -sys.maxsize - 1
        self.assertTrue(is_valid_bst(build_tree([0, small, big])))
        self.assertTrue(is_valid_bst(build_tree([0.0, float("-inf"), float("inf")])))

    def test_other_comparable_types(self):
        self.assertTrue(is_valid_bst(build_tree(["m", "c", "x", "a", "e"])))
        self.assertFalse(is_valid_bst(build_tree(["m", "c", "x", "a", "z"])))

    def test_deep_chain_has_no_recursion_limit(self):
        root = None
        for value in range(3000):
            root = insert(root, value)
        self.assertTrue(is_valid_bst(root))

        node = root
        while node.right:
            node = node.right
        node.right = Node(-1)  # самый глубокий узел нарушает границу корня
        self.assertFalse(is_valid_bst(root))


class RandomTreesTest(unittest.TestCase):
    def test_trees_built_by_insertion_are_valid(self):
        for seed in range(50):
            rng = random.Random(seed)
            root = None
            for value in rng.sample(range(-100, 100), rng.randint(1, 60)):
                root = insert(root, value)
            with self.subTest(seed=seed):
                self.assertTrue(is_valid_bst(root))

    def test_swapping_two_values_breaks_bst(self):
        for seed in range(50):
            rng = random.Random(seed)
            root = None
            for value in rng.sample(range(-100, 100), rng.randint(2, 60)):
                root = insert(root, value)
            nodes, stack = [], [root]
            while stack:
                node = stack.pop()
                if node:
                    nodes.append(node)
                    stack += [node.left, node.right]
            a, b = rng.sample(nodes, 2)
            a.value, b.value = b.value, a.value
            with self.subTest(seed=seed):
                self.assertFalse(is_valid_bst(root))

    def test_random_shapes_match_reference(self):
        for seed in range(200):
            rng = random.Random(seed)
            values = [rng.randint(0, 15) for _ in range(rng.randint(0, 8))]
            root = random_shape(rng, values)
            with self.subTest(seed=seed, values=values):
                self.assertEqual(is_valid_bst(root), reference(root))


if __name__ == "__main__":
    unittest.main()
