import unittest

from solution import count_primes


class CountPrimesTest(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(count_primes(10), 4)

    def test_number_less_than_two(self) -> None:
        self.assertEqual(count_primes(1), 0)

    def test_two_is_not_included(self) -> None:
        self.assertEqual(count_primes(2), 0)

    def test_small_boundary(self) -> None:
        self.assertEqual(count_primes(3), 1)

    def test_larger_number(self) -> None:
        self.assertEqual(count_primes(100), 25)


if __name__ == "__main__":
    unittest.main()
