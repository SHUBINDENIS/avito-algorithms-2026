import unittest

from pathlib import Path
from runpy import run_path

two_sum = run_path(str(Path(__file__).with_name("solution.py")))["two_sum"]


class TwoSumTest(unittest.TestCase):
    def test_pairs(self):
        cases = [
            ([1, 3, 4, 10], 7, (1, 2)),
            ([5, 5, 1, 4], 10, (0, 1)),
            ([-5, -2, 4, 9], -7, (0, 1)),
            ([0, 4, 0], 0, (0, 2)),
            ([1, 2, 8, 9], 17, (2, 3)),
            ([2, 8], 10, (0, 1)),
        ]
        for arr, k, expected in cases:
            with self.subTest(arr=arr, k=k):
                self.assertEqual(two_sum(arr, k), expected)

    def test_no_pair(self):
        for arr, k in [([], 0), ([5], 10), ([1, 2], 10)]:
            with self.subTest(arr=arr, k=k):
                with self.assertRaises(ValueError):
                    two_sum(arr, k)


if __name__ == "__main__":
    unittest.main()