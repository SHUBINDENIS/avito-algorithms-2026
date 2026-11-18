import unittest
from random import Random
from unittest.mock import patch

import solution
from solution import kth_largest


class KthLargestTest(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(kth_largest([3, 2, 1, 5, 6, 4], 2), 5)
        self.assertEqual(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4)

    def test_singleton_and_extreme_ranks(self):
        self.assertEqual(kth_largest([9], 1), 9)
        self.assertEqual(kth_largest([-8, -3, -6, -9], 1), -3)
        self.assertEqual(kth_largest([-8, -3, -6, -9], 4), -9)

    def test_duplicate_ranks_and_all_equal(self):
        self.assertEqual(kth_largest([5, 2, 5, 5, 1], 3), 5)
        self.assertEqual(kth_largest([5, 2, 5, 5, 1], 4), 2)
        self.assertEqual(kth_largest([4] * 2000, 1400), 4)

    def test_documented_trace_preserves_input(self):
        nums = [3, 2, 3, 1, 2, 4, 5, 5, 6]
        original = nums.copy()
        with patch.object(solution, "randrange", side_effect=(0, 6)) as choose:
            self.assertEqual(kth_largest(nums, 4), 4)
        self.assertEqual([call.args for call in choose.call_args_list],
                         [(0, 9), (5, 9)])
        self.assertEqual(nums, original)

    def test_invalid_rank(self):
        for values, k in (([], 1), ([1, 2], -1), ([1, 2], 0), ([1, 2], 3)):
            with self.subTest(values=values, k=k):
                with self.assertRaises(ValueError):
                    kth_largest(values, k)

    def test_seeded_random_all_ranks(self):
        rng = Random(42)
        with patch.object(solution, "randrange", rng.randrange):
            for n in (2, 3, 9, 20, 57, 100):
                values = [rng.randint(-20, 20) for _ in range(n)]
                for k, expected in enumerate(sorted(values, reverse=True), 1):
                    with self.subTest(n=n, k=k):
                        self.assertEqual(kth_largest(values, k), expected)


if __name__ == "__main__":
    unittest.main()
