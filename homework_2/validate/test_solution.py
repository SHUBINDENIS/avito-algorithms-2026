import unittest

from solution import validate_stack_sequences


class ValidateStackSequencesTest(unittest.TestCase):
    def test_valid_example(self) -> None:
        self.assertTrue(validate_stack_sequences([1, 2, 3, 4, 5], [1, 3, 5, 4, 2]))

    def test_invalid_example(self) -> None:
        self.assertFalse(validate_stack_sequences([1, 2, 3], [3, 1, 2]))

    def test_single_element(self) -> None:
        self.assertTrue(validate_stack_sequences([7], [7]))

    def test_same_order(self) -> None:
        self.assertTrue(validate_stack_sequences([1, 2, 3, 4], [1, 2, 3, 4]))

    def test_reverse_order(self) -> None:
        self.assertTrue(validate_stack_sequences([1, 2, 3, 4], [4, 3, 2, 1]))

    def test_several_pops_in_a_row(self) -> None:
        self.assertTrue(validate_stack_sequences([1, 2, 3, 4, 5], [3, 2, 4, 5, 1]))

    def test_invalid_order_near_end(self) -> None:
        self.assertFalse(validate_stack_sequences([1, 2, 3, 4, 5], [2, 4, 1, 5, 3]))

    def test_negative_numbers_and_zero(self) -> None:
        self.assertTrue(validate_stack_sequences([-5, 0, 8, -2], [0, -2, 8, -5]))

    def test_input_is_not_changed(self) -> None:
        pushed = [1, 2, 3]
        popped = [2, 3, 1]
        self.assertTrue(validate_stack_sequences(pushed, popped))
        self.assertEqual(pushed, [1, 2, 3])
        self.assertEqual(popped, [2, 3, 1])

    def test_maximum_length(self) -> None:
        pushed = list(range(100_000))
        self.assertTrue(validate_stack_sequences(pushed, pushed[::-1]))


if __name__ == "__main__":
    unittest.main()
