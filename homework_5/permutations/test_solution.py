import io
import itertools
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from runpy import run_path

permutations = run_path(str(Path(__file__).with_name("solution.py")))["permutations"]


class PermutationsTest(unittest.TestCase):
    def test_examples(self):
        for values in ([1, 2, 3], [0, 1], [1]):
            with self.subTest(values=values):
                expected = [list(p) for p in itertools.permutations(values)]
                self.assertEqual(permutations(values), expected)

    def test_empty(self):
        self.assertEqual(permutations([]), [[]])

    def test_duplicates(self):
        self.assertEqual(permutations([1, 1, 2]), [[1, 1, 2], [1, 2, 1], [2, 1, 1]])

    def test_does_not_modify_input_or_share_results(self):
        values = [1, 2, 3]
        answer = permutations(values)
        answer[0][0] = 99
        self.assertEqual(values, [1, 2, 3])
        self.assertNotEqual(answer[1][0], 99)

    def test_stack_visualization_uses_tracer(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(permutations([0, 1], trace=True), [[0, 1], [1, 0]])
        self.assertIn("    <- visit = [0, 1]", output.getvalue())
        self.assertIn("    <- visit = [1, 0]", output.getvalue())
        self.assertEqual(output.getvalue().count("-> visit("), 5)

    def test_small_inputs_match_standard_library(self):
        for size in range(7):
            with self.subTest(size=size):
                values = list(range(size))
                self.assertEqual(permutations(values), [list(p) for p in itertools.permutations(values)])


if __name__ == "__main__":
    unittest.main()
