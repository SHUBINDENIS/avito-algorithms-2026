import unittest
from random import Random

from solution import mergesort, quicksort


class IterativeSortTest(unittest.TestCase):
    def test_empty_and_singleton(self):
        for sort in (mergesort, quicksort):
            for values in ([], [7]):
                with self.subTest(sort=sort.__name__, values=values):
                    result = sort(values)
                    self.assertEqual(result, values)
                    self.assertIsNot(result, values)

    def test_odd_length_and_duplicates(self):
        examples = (
            ([4, 1, 5, 1, 3], [1, 1, 3, 4, 5]),
            ([5, 3, 0, 2, -1, 2, -3], [-3, -1, 0, 2, 2, 3, 5]),
        )
        for sort in (mergesort, quicksort):
            for values, expected in examples:
                with self.subTest(sort=sort.__name__, values=values):
                    original = values.copy()
                    self.assertEqual(sort(values), expected)
                    self.assertEqual(values, original)

    def test_sorted_reverse_and_equal(self):
        ordered = list(range(1500))
        for sort in (mergesort, quicksort):
            for values in (ordered, ordered[::-1], [4] * 1500):
                with self.subTest(sort=sort.__name__, first=values[0]):
                    self.assertEqual(sort(values), sorted(values))

    def test_seeded_random(self):
        rng = Random(42)
        for n in (2, 8, 17, 64, 127, 257):
            values = [rng.randint(-20, 20) for _ in range(n)]
            for sort in (mergesort, quicksort):
                with self.subTest(sort=sort.__name__, n=n):
                    self.assertEqual(sort(values), sorted(values))


if __name__ == "__main__":
    unittest.main()
