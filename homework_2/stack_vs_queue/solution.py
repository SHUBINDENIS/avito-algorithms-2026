class Node:
    def __init__(self, value: int, next_node=None) -> None:
        self.value = value
        self.next = next_node


class Stack:
    def __init__(self) -> None:
        self.head = None

    def is_empty(self) -> bool:
        return self.head is None

    def push(self, value: int) -> None:
        self.head = Node(value, self.head)

    def pop(self) -> int:
        if self.is_empty():
            raise IndexError("Стек пуст")
        value = self.head.value
        self.head = self.head.next
        return value

    def peek(self) -> int:
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self.head.value


class Queue:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def is_empty(self) -> bool:
        return self.head is None

    def enqueue(self, value: int) -> None:
        node = Node(value)
        if self.is_empty():
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def dequeue(self) -> int:
        if self.is_empty():
            raise IndexError("Очередь пуста")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return value

    def peek(self) -> int:
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self.head.value
