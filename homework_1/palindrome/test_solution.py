import unittest

from solution import is_palindrome


class IsPalindromeTest(unittest.TestCase):
    def test_palindrome_with_odd_number_of_digits(self) -> None:
        self.assertTrue(is_palindrome(121))

    def test_palindrome_with_even_number_of_digits(self) -> None:
        self.assertTrue(is_palindrome(1221))

    def test_non_palindrome(self) -> None:
        self.assertFalse(is_palindrome(31))

    def test_number_ending_with_zero(self) -> None:
        self.assertFalse(is_palindrome(10))

    def test_one_digit_number(self) -> None:
        self.assertTrue(is_palindrome(7))


if __name__ == "__main__":
    unittest.main()
