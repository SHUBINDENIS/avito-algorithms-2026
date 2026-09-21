class ListNode:
    def __init__(self, value: int, next_node=None) -> None:
        self.value = value
        self.next = next_node


def merge_with_dummy(list1, list2):
    """Объединяет списки, используя фиктивный узел перед головой результата."""
    dummy = ListNode(0)
    tail = dummy

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    tail.next = list1 if list1 is not None else list2
    return dummy.next


def merge_without_dummy(list1, list2):
    """Объединяет списки, отдельно выбирая первый узел результата."""
    if list1 is None:
        return list2
    if list2 is None:
        return list1

    if list1.value <= list2.value:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next
    tail = head

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    tail.next = list1 if list1 is not None else list2
    return head
