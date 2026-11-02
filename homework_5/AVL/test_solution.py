import random
import unittest
from pathlib import Path
from runpy import run_path

AVL = run_path(str(Path(__file__).with_name("solution.py")))["AVL"]


class AVLTest(unittest.TestCase):
    def assert_invariants(self, tree, expected):
        def check(node, low=None, high=None):
            if node is None:
                return 0
            if low is not None:
                self.assertGreater(node.key, low)
            if high is not None:
                self.assertLess(node.key, high)
            left = check(node.left, low, node.key)
            right = check(node.right, node.key, high)
            self.assertLessEqual(abs(left - right), 1)
            self.assertEqual(node.height, 1 + max(left, right))
            return node.height

        check(tree.root)
        self.assertEqual(tree.inorder(), sorted(expected))
        self.assertEqual(len(tree), len(expected))

    def test_empty_and_missing(self):
        tree = AVL()
        self.assertFalse(tree.search(1))
        self.assertFalse(tree.delete(1))
        self.assertEqual(tree.visualize(), ".")
        self.assert_invariants(tree, set())

    def test_four_insert_rotation_cases(self):
        for values in ((30, 20, 10), (10, 20, 30), (30, 10, 20), (10, 30, 20)):
            with self.subTest(values=values):
                tree = AVL()
                for value in values:
                    self.assertTrue(tree.insert(value))
                self.assertEqual(tree.root.key, 20)
                self.assert_invariants(tree, set(values))

    def test_duplicates_and_search(self):
        tree = AVL()
        self.assertTrue(tree.insert(5))
        self.assertFalse(tree.insert(5))
        self.assertTrue(tree.search(5))
        self.assertIn(5, tree)
        self.assertNotIn(7, tree)
        self.assert_invariants(tree, {5})

    def test_delete_leaf_one_child_and_two_children(self):
        tree = AVL()
        expected = {20, 10, 30, 5, 15, 25, 40, 35}
        for value in sorted(expected):
            tree.insert(value)
        for value in (5, 40, 20, 10, 15, 25, 30, 35):
            self.assertTrue(tree.delete(value))
            expected.remove(value)
            self.assert_invariants(tree, expected)
        self.assertIsNone(tree.root)

    def test_rebalancing_after_deletion(self):
        tree = AVL()
        values = {9, 5, 10, 0, 6, 11, -1, 1, 2}
        for value in (9, 5, 10, 0, 6, 11, -1, 1, 2):
            tree.insert(value)
        tree.delete(10)
        self.assert_invariants(tree, values - {10})

    def test_sorted_insertions_and_reverse_deletions(self):
        tree = AVL()
        expected = set()
        for value in range(300):
            tree.insert(value)
            expected.add(value)
            self.assert_invariants(tree, expected)
        for value in reversed(range(300)):
            tree.delete(value)
            expected.remove(value)
            self.assert_invariants(tree, expected)

    def test_random_operations_match_set(self):
        rng = random.Random(42)
        tree = AVL()
        expected = set()
        for _ in range(1500):
            value = rng.randrange(-100, 101)
            operation = rng.choice(("insert", "delete", "search"))
            if operation == "insert":
                self.assertEqual(tree.insert(value), value not in expected)
                expected.add(value)
            elif operation == "delete":
                self.assertEqual(tree.delete(value), value in expected)
                expected.discard(value)
            else:
                self.assertEqual(tree.search(value), value in expected)
            self.assert_invariants(tree, expected)

    def test_visualization_distinguishes_left_and_right(self):
        tree = AVL()
        for value in (2, 1, 3):
            tree.insert(value)
        self.assertEqual(tree.visualize(), "2 (h=2)\n  L: 1 (h=1)\n  R: 3 (h=1)")


if __name__ == "__main__":
    unittest.main()
