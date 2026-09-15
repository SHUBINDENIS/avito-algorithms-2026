import unittest

from solution import max_even_sum


class MaxEvenSumTest(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(max_even_sum([5, 7, 13, 2, 14]), 36)

    def test_already_even_total(self) -> None:
        self.assertEqual(max_even_sum([2, 4, 8]), 14)

    def test_removes_smallest_odd_number(self) -> None:
        self.assertEqual(max_even_sum([9, 1, 3]), 12)

    def test_single_odd_number(self) -> None:
        self.assertEqual(max_even_sum([3]), 0)

    def test_empty_array(self) -> None:
        self.assertEqual(max_even_sum([]), 0)


if __name__ == "__main__":
    unittest.main()
