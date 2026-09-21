import unittest

from solution import ListNode, merge_with_dummy, merge_without_dummy


def make_list(values):
    head = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def collect_nodes(head):
    nodes = []
    seen = set()
    while head is not None:
        if id(head) in seen:
            raise AssertionError("В списке появился цикл")
        seen.add(id(head))
        nodes.append(head)
        head = head.next
    return nodes


class MergeListsTest(unittest.TestCase):
    def check_merge(self, values1, values2, expected) -> None:
        for merge in (merge_with_dummy, merge_without_dummy):
            with self.subTest(method=merge.__name__):
                # Каждый способ меняет ссылки, поэтому создаём списки заново.
                list1 = make_list(values1)
                list2 = make_list(values2)
                original_nodes = collect_nodes(list1) + collect_nodes(list2)
                result_nodes = collect_nodes(merge(list1, list2))
                self.assertEqual([node.value for node in result_nodes], expected)
                self.assertEqual(len(result_nodes), len(original_nodes))
                self.assertEqual(
                    {id(node) for node in result_nodes},
                    {id(node) for node in original_nodes},
                )

    def test_example(self) -> None:
        self.check_merge([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4])

    def test_both_empty(self) -> None:
        self.check_merge([], [], [])

    def test_first_empty(self) -> None:
        self.check_merge([], [1, 3, 5], [1, 3, 5])

    def test_second_empty(self) -> None:
        self.check_merge([1, 3, 5], [], [1, 3, 5])

    def test_single_nodes(self) -> None:
        self.check_merge([2], [1], [1, 2])

    def test_all_values_equal(self) -> None:
        self.check_merge([2, 2], [2, 2, 2], [2, 2, 2, 2, 2])

    def test_negative_numbers_and_zero(self) -> None:
        self.check_merge([-5, -1, 0], [-3, 0, 4], [-5, -3, -1, 0, 0, 4])

    def test_non_overlapping_ranges(self) -> None:
        self.check_merge([1, 2], [5, 6, 7], [1, 2, 5, 6, 7])
        self.check_merge([5, 6, 7], [1, 2], [1, 2, 5, 6, 7])

    def test_different_lengths(self) -> None:
        self.check_merge([3], [1, 2, 4, 5, 6], [1, 2, 3, 4, 5, 6])

    def test_alternating_values(self) -> None:
        self.check_merge([1, 3, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6])

    def test_long_lists(self) -> None:
        self.check_merge(list(range(0, 4000, 2)), list(range(1, 4000, 2)), list(range(4000)))


if __name__ == "__main__":
    unittest.main()
