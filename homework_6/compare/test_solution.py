import unittest
from random import Random
from unittest.mock import patch

import solution


class RecursiveSortTest(unittest.TestCase):
    def test_empty_and_singleton(self):
        for sort in (solution.mergesort, solution.quicksort):
            for values in ([], [7]):
                with self.subTest(sort=sort.__name__, values=values):
                    result = sort(values)
                    self.assertEqual(result, values)
                    self.assertIsNot(result, values)

    def test_mixed_values_keep_input(self):
        values = [4, -1, 4, 2, 0, -5, 3]
        original = values.copy()
        for sort in (solution.mergesort, solution.quicksort):
            with self.subTest(sort=sort.__name__):
                self.assertEqual(sort(values), [-5, -1, 0, 2, 3, 4, 4])
                self.assertEqual(values, original)

    def test_sorted_reverse_and_equal(self):
        ordered = list(range(1500))
        for sort in (solution.mergesort, solution.quicksort):
            for values in (ordered, ordered[::-1], [9] * 1500):
                with self.subTest(sort=sort.__name__, first=values[0]):
                    self.assertEqual(sort(values), sorted(values))

    def test_seeded_random(self):
        rng = Random(42)
        for n in (2, 3, 31, 128, 501):
            values = [rng.randint(-100, 100) for _ in range(n)]
            for sort in (solution.mergesort, solution.quicksort):
                with self.subTest(sort=sort.__name__, n=n):
                    self.assertEqual(sort(values), sorted(values))

    def test_timer_forwards_arguments_and_returns_elapsed(self):
        @solution.timed
        def add(a, *, b):
            return a + b

        with patch.object(solution, "perf_counter", side_effect=(10.0, 10.25)):
            self.assertEqual(add(2, b=3), (5, 0.25))
        self.assertEqual(add.__name__, "add")

    def test_benchmark_checks_both_inputs(self):
        rows = solution.benchmark(size=64, repeats=3)
        self.assertEqual([row[0] for row in rows], ["shuffled", "sorted"])
        for _, merge_time, quick_time in rows:
            self.assertGreaterEqual(merge_time, 0)
            self.assertGreaterEqual(quick_time, 0)


if __name__ == "__main__":
    unittest.main()
