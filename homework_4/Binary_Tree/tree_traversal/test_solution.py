import random
import unittest

from pathlib import Path
from runpy import run_path

_solution = run_path(str(Path(__file__).with_name("solution.py")))
BST = _solution["BST"]
Node = _solution["Node"]
to_text = _solution["to_text"]

#          8
#        /   \
#       3     10
#      / \      \
#     1   6      14
#        / \     /
#       4   7   13
EXAMPLE = [8, 3, 10, 1, 6, 14, 4, 7, 13]

TRAVERSALS = [
    "preorder",
    "inorder",
    "postorder",
    "reverse_preorder",
    "reverse_inorder",
    "reverse_postorder",
]


def reference(node, order):
    """Рекурсивный эталон: короткий и очевидно верный."""
    if node is None:
        return []
    n = [node.value]
    l = reference(node.left, order)
    r = reference(node.right, order)
    return {
        "preorder": n + l + r,
        "inorder": l + n + r,
        "postorder": l + r + n,
        "reverse_preorder": n + r + l,
        "reverse_inorder": r + n + l,
        "reverse_postorder": r + l + n,
    }[order]


def is_bst(node, low=None, high=None):
    if node is None:
        return True
    if (low is not None and node.value <= low) or (high is not None and node.value >= high):
        return False
    return is_bst(node.left, low, node.value) and is_bst(node.right, node.value, high)


def traversals(tree):
    return {order: getattr(tree, order)() for order in TRAVERSALS}


class ExampleTreeTest(unittest.TestCase):
    def test_traversals_counted_by_hand(self):
        expected = {
            "preorder": [8, 3, 1, 6, 4, 7, 10, 14, 13],
            "inorder": [1, 3, 4, 6, 7, 8, 10, 13, 14],
            "postorder": [1, 4, 7, 6, 3, 13, 14, 10, 8],
            "reverse_preorder": [8, 10, 14, 13, 3, 6, 7, 4, 1],
            "reverse_inorder": [14, 13, 10, 8, 7, 6, 4, 3, 1],
            "reverse_postorder": [13, 14, 10, 7, 4, 6, 1, 3, 8],
        }
        self.assertEqual(traversals(BST(EXAMPLE)), expected)

    def test_structure_after_inserts(self):
        tree = BST(EXAMPLE)
        root = tree.root
        self.assertEqual(root.value, 8)
        self.assertEqual((root.left.value, root.right.value), (3, 10))
        self.assertEqual((root.left.left.value, root.left.right.value), (1, 6))
        self.assertIsNone(root.right.left)
        self.assertEqual(root.right.right.left.value, 13)
        self.assertEqual(tree.height(), 4)
        self.assertEqual(len(tree), 9)

    def test_contains(self):
        tree = BST(EXAMPLE)
        for value in EXAMPLE:
            self.assertIn(value, tree)
        self.assertNotIn(5, tree)
        self.assertNotIn(100, tree)


class EdgeCasesTest(unittest.TestCase):
    def test_empty_tree(self):
        tree = BST()
        self.assertEqual(traversals(tree), {order: [] for order in TRAVERSALS})
        self.assertEqual(len(tree), 0)
        self.assertEqual(tree.height(), 0)
        self.assertNotIn(1, tree)
        self.assertEqual(to_text(tree), "(пустое дерево)")

    def test_single_node(self):
        tree = BST([42])
        self.assertEqual(traversals(tree), {order: [42] for order in TRAVERSALS})
        self.assertEqual(tree.height(), 1)

    def test_insert_returns_whether_value_is_new(self):
        tree = BST()
        self.assertTrue(tree.insert(1))
        self.assertTrue(tree.insert(2))
        self.assertFalse(tree.insert(1))
        self.assertEqual(len(tree), 2)

    def test_duplicates_do_not_change_tree(self):
        tree = BST([5, 3, 7])
        before = traversals(tree)
        self.assertFalse(tree.insert(5))
        self.assertFalse(tree.insert(3))
        self.assertEqual(len(tree), 3)
        self.assertEqual(traversals(tree), before)

    def test_two_nodes(self):
        left = BST([2, 1])
        right = BST([1, 2])
        self.assertEqual((left.preorder(), left.postorder()), ([2, 1], [1, 2]))
        self.assertEqual((right.preorder(), right.postorder()), ([1, 2], [2, 1]))
        self.assertEqual(left.inorder(), [1, 2])
        self.assertEqual(right.inorder(), [1, 2])

    def test_degenerate_tree_has_no_recursion_limit(self):
        # Отсортированный ввод даёт цепочку высотой n больше лимита рекурсии (~1000).
        for values in (range(3000), range(3000, 0, -1)):
            with self.subTest(first=values[0]):
                tree = BST(values)
                self.assertEqual(tree.height(), 3000)
                self.assertEqual(tree.inorder(), sorted(values))
                for order in TRAVERSALS:
                    self.assertEqual(sorted(getattr(tree, order)()), sorted(values))

    def test_other_comparable_types(self):
        self.assertEqual(BST(["m", "c", "x", "a", "e"]).inorder(), ["a", "c", "e", "m", "x"])
        self.assertEqual(BST([0.5, -3, 2.25, -3.5]).inorder(), [-3.5, -3, 0.5, 2.25])

    def test_manually_built_tree(self):
        # Обходы работают по структуре узлов, даже без вставки.
        tree = BST()
        tree.root = Node(1, Node(2, Node(4)), Node(3))
        self.assertEqual(tree.preorder(), [1, 2, 4, 3])
        self.assertEqual(tree.postorder(), [4, 2, 3, 1])
        self.assertEqual(tree.reverse_inorder(), [3, 1, 2, 4])

    def test_to_text(self):
        self.assertEqual(to_text(BST([2, 1, 3])), "┌── 3\n2\n└── 1")


class RandomTreesTest(unittest.TestCase):
    def test_random_trees(self):
        for seed in range(50):
            rng = random.Random(seed)
            values = [rng.randint(-50, 50) for _ in range(rng.randint(0, 60))]
            tree = BST(values)
            with self.subTest(seed=seed):
                self.assertTrue(is_bst(tree.root))
                self.assertEqual(len(tree), len(set(values)))
                self.assertEqual(tree.inorder(), sorted(set(values)))
                for order in TRAVERSALS:
                    self.assertEqual(getattr(tree, order)(), reference(tree.root, order))

                # Разворотом списка совпадают только эти три пары.
                self.assertEqual(tree.reverse_inorder(), tree.inorder()[::-1])
                self.assertEqual(tree.reverse_postorder(), tree.preorder()[::-1])
                self.assertEqual(tree.reverse_preorder(), tree.postorder()[::-1])

                # Вставка в порядке preorder восстанавливает то же дерево.
                self.assertEqual(BST(tree.preorder()).preorder(), tree.preorder())


if __name__ == "__main__":
    unittest.main()
