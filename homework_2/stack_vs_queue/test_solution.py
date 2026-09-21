import unittest

from solution import Queue, Stack


class StackTest(unittest.TestCase):
    def test_empty_stack(self) -> None:
        stack = Stack()
        self.assertTrue(stack.is_empty())
        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.peek()

    def test_last_in_first_out(self) -> None:
        stack = Stack()
        for value in [4, 7, 2]:
            stack.push(value)
        self.assertFalse(stack.is_empty())
        self.assertEqual([stack.pop(), stack.pop(), stack.pop()], [2, 7, 4])
        self.assertTrue(stack.is_empty())

    def test_peek_does_not_remove_element(self) -> None:
        stack = Stack()
        stack.push(5)
        self.assertEqual(stack.peek(), 5)
        self.assertEqual(stack.peek(), 5)
        self.assertEqual(stack.pop(), 5)
        self.assertTrue(stack.is_empty())

    def test_mixed_operations(self) -> None:
        stack = Stack()
        stack.push(4)
        stack.push(7)
        self.assertEqual(stack.pop(), 7)
        stack.push(2)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 4)
        stack.push(9)
        self.assertEqual(stack.pop(), 9)
        self.assertTrue(stack.is_empty())

    def test_repeated_and_negative_values(self) -> None:
        stack = Stack()
        for value in [-3, 0, -3]:
            stack.push(value)
        self.assertEqual([stack.pop() for _ in range(3)], [-3, 0, -3])


class QueueTest(unittest.TestCase):
    def test_empty_queue(self) -> None:
        queue = Queue()
        self.assertTrue(queue.is_empty())
        with self.assertRaises(IndexError):
            queue.dequeue()
        with self.assertRaises(IndexError):
            queue.peek()

    def test_first_in_first_out(self) -> None:
        queue = Queue()
        for value in [4, 7, 2]:
            queue.enqueue(value)
        self.assertFalse(queue.is_empty())
        self.assertEqual([queue.dequeue() for _ in range(3)], [4, 7, 2])
        self.assertTrue(queue.is_empty())

    def test_peek_does_not_remove_element(self) -> None:
        queue = Queue()
        queue.enqueue(5)
        self.assertEqual(queue.peek(), 5)
        self.assertEqual(queue.peek(), 5)
        self.assertEqual(queue.dequeue(), 5)
        self.assertTrue(queue.is_empty())

    def test_mixed_operations(self) -> None:
        queue = Queue()
        queue.enqueue(4)
        queue.enqueue(7)
        self.assertEqual(queue.dequeue(), 4)
        queue.enqueue(2)
        self.assertEqual(queue.dequeue(), 7)
        self.assertEqual(queue.dequeue(), 2)

    def test_reuse_after_removing_last_element(self) -> None:
        queue = Queue()
        queue.enqueue(1)
        self.assertEqual(queue.dequeue(), 1)
        self.assertIsNone(queue.head)
        self.assertIsNone(queue.tail)
        queue.enqueue(2)
        queue.enqueue(3)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.dequeue(), 3)
        self.assertTrue(queue.is_empty())

    def test_repeated_and_negative_values(self) -> None:
        queue = Queue()
        for value in [-3, 0, -3]:
            queue.enqueue(value)
        self.assertEqual([queue.dequeue() for _ in range(3)], [-3, 0, -3])


if __name__ == "__main__":
    unittest.main()
