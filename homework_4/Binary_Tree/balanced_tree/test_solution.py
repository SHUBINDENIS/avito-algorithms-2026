import random
import unittest

from pathlib import Path
from runpy import run_path

_solution = run_path(str(Path(__file__).with_name("solution.py")))
Node = _solution["Node"]
is_balanced = _solution["is_balanced"]
height = _solution["height"]
build_tree = _solution["build_tree"]


def naive_height(node):
    if node is None:
        return 0
    return 1 + max(naive_height(node.left), naive_height(node.right))


def naive_is_balanced(node):
    """Определение «в лоб»: O(n²), зато очевидно верное – эталон для тестов."""
    if node is None:
        return True
    return (abs(naive_height(node.left) - naive_height(node.right)) <= 1
            and naive_is_balanced(node.left)
            and naive_is_balanced(node.right))


def perfect_tree(depth):
    """Полное дерево из 2**depth - 1 узлов, строится по уровням."""
    return build_tree(range(2 ** depth - 1))


def fibonacci_tree(h):
    """Минимальное AVL-дерево высоты h: левое поддерево на 1 выше правого
    в каждом узле – самое «кривое» из сбалансированных."""
    if h == 0:
        return None
    if h == 1:
        return Node(h)
    return Node(h, fibonacci_tree(h - 1), fibonacci_tree(h - 2))


def chain(n, side="left"):
    root = node = Node(0)
    for i in range(1, n):
        setattr(node, side, Node(i))
        node = getattr(node, side)
    return root


def random_shape(rng, n):
    if n == 0:
        return None
    nodes = [Node(i) for i in range(n)]
    for i in range(1, n):
        while True:
            parent = nodes[rng.randrange(i)]
            side = rng.choice(("left", "right"))
            if getattr(parent, side) is None:
                setattr(parent, side, nodes[i])
                break
    return nodes[0]


class ExamplesTest(unittest.TestCase):
    def test_balanced_example(self):
        #         1
        #       /   \
        #      2     3
        #     / \     \
        #    4   5     6
        #       /
        #      7
        self.assertTrue(is_balanced(build_tree([1, 2, 3, 4, 5, None, 6, None, None, 7])))

    def test_root_is_fine_but_subtree_is_not(self):
        # У корня обе стороны высоты 3, но узлы 2 и 3 – цепочки.
        root = build_tree([1, 2, 3, 4, None, None, 5, 6, None, None, 7])
        self.assertEqual(height(root.left), height(root.right))
        self.assertFalse(is_balanced(root))

    def test_subtrees_are_fine_but_root_is_not(self):
        # Каждое поддерево сбалансировано, но их высоты 3 и 1.
        root = build_tree([1, 2, 3, 4, 5, None, None, 6])
        self.assertTrue(is_balanced(root.left))
        self.assertTrue(is_balanced(root.right))
        self.assertFalse(is_balanced(root))

    def test_fibonacci_tree_is_balanced(self):
        for h in range(1, 15):
            with self.subTest(h=h):
                root = fibonacci_tree(h)
                self.assertEqual(height(root), h)
                self.assertTrue(is_balanced(root))

    def test_fibonacci_tree_breaks_after_extra_node(self):
        # Ещё один лист на самом длинном пути – и на всём этом пути, включая корень,
        # разница высот становится 2.
        root = fibonacci_tree(6)
        node = root
        while node.left:
            node = node.left
        node.left = Node("extra")
        self.assertFalse(is_balanced(root))


class EdgeCasesTest(unittest.TestCase):
    def test_empty_tree(self):
        self.assertTrue(is_balanced(None))
        self.assertEqual(height(None), 0)

    def test_single_node(self):
        self.assertTrue(is_balanced(Node(1)))
        self.assertEqual(height(Node(1)), 1)

    def test_one_child(self):
        self.assertTrue(is_balanced(build_tree([1, 2])))
        self.assertTrue(is_balanced(build_tree([1, None, 2])))

    def test_chain_of_three(self):
        self.assertFalse(is_balanced(chain(3, "left")))
        self.assertFalse(is_balanced(chain(3, "right")))

    def test_perfect_trees(self):
        for depth in range(1, 15):
            with self.subTest(depth=depth):
                self.assertTrue(is_balanced(perfect_tree(depth)))

    def test_long_chain_has_no_recursion_limit(self):
        self.assertFalse(is_balanced(chain(5000)))
        self.assertEqual(height(chain(5000, "right")), 5000)

    def test_equal_values_do_not_matter(self):
        # Балансировка зависит только от формы дерева, не от значений.
        self.assertTrue(is_balanced(build_tree([0, 0, 0, 0])))


class RandomTreesTest(unittest.TestCase):
    def test_random_shapes_match_naive_definition(self):
        balanced = 0
        for seed in range(300):
            rng = random.Random(seed)
            root = random_shape(rng, rng.randint(0, 12))
            expected = naive_is_balanced(root)
            balanced += expected
            with self.subTest(seed=seed):
                self.assertEqual(is_balanced(root), expected)
        # Тест проверяет обе ветки ответа.
        self.assertTrue(0 < balanced < 300)


if __name__ == "__main__":
    unittest.main()
