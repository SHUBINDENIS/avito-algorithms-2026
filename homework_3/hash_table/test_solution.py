import random
import unittest

from pathlib import Path
from runpy import run_path

HashTable = run_path(str(Path(__file__).with_name("solution.py")))["HashTable"]


class CollisionKey:
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, CollisionKey) and self.value == other.value


class HashTableTest(unittest.TestCase):
    def test_put_and_get(self):
        table = HashTable()
        table.put("apple", 1)
        table.put("empty", None)

        self.assertEqual(table.get("apple"), 1)
        self.assertIsNone(table.get("empty"))
        self.assertIn("empty", table)
        self.assertEqual(len(table), 2)

    def test_update(self):
        table = HashTable()
        table.put("apple", 1)
        table.put("apple", 2)

        self.assertEqual(table.get("apple"), 2)
        self.assertEqual(len(table), 1)

    def test_delete(self):
        table = HashTable()
        table.put("apple", 1)
        table.delete("apple")

        self.assertNotIn("apple", table)
        self.assertEqual(len(table), 0)

    def test_missing_key(self):
        table = HashTable()

        self.assertNotIn("missing", table)
        with self.assertRaises(KeyError):
            table.get("missing")
        with self.assertRaises(KeyError):
            table.delete("missing")

        self.assertEqual(len(table), 0)

    def test_collisions(self):
        table = HashTable()
        for i in range(20):
            table.put(CollisionKey(i), i * 10)

        table.put(CollisionKey(7), 777)
        self.assertEqual(len(table), 20)
        self.assertEqual(table.get(CollisionKey(7)), 777)

        for i in range(0, 20, 2):
            table.delete(CollisionKey(i))

        self.assertEqual(len(table), 10)
        for i in range(20):
            with self.subTest(key=i):
                if i % 2 == 0:
                    self.assertNotIn(CollisionKey(i), table)
                else:
                    expected = 777 if i == 7 else i * 10
                    self.assertEqual(table.get(CollisionKey(i)), expected)

    def test_resize(self):
        table = HashTable(capacity=2)
        for i in range(1000):
            table.put(i, i * 2)

        self.assertEqual(len(table), 1000)
        for i in range(1000):
            self.assertEqual(table.get(i), i * 2)

        for i in range(1000):
            table.delete(i)

        self.assertEqual(len(table), 0)
        table.put("again", 42)
        self.assertEqual(table.get("again"), 42)

    def test_different_key_types(self):
        table = HashTable()
        pairs = [("name", 1), (10, 2), ((1, 2), 3), (None, 4)]

        for key, value in pairs:
            table.put(key, value)
        for key, value in pairs:
            self.assertEqual(table.get(key), value)

        self.assertEqual(len(table), 4)

    def test_dict_operators(self):
        table = HashTable()
        table["a"] = 10

        self.assertEqual(table["a"], 10)
        self.assertIn("a", table)

        del table["a"]
        self.assertNotIn("a", table)
        with self.assertRaises(KeyError):
            _ = table["a"]

    def test_invalid_capacity(self):
        for capacity in [0, -1]:
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValueError):
                    HashTable(capacity)

    def test_random_operations(self):
        rng = random.Random(42)
        table = HashTable(capacity=1)
        reference = {}

        for _ in range(3000):
            key = rng.randrange(50)
            operation = rng.choice(["put", "get", "delete"])

            if operation == "put":
                value = rng.randrange(-1000, 1001)
                table.put(key, value)
                reference[key] = value
            elif operation == "get":
                if key in reference:
                    self.assertEqual(table.get(key), reference[key])
                else:
                    with self.assertRaises(KeyError):
                        table.get(key)
            else:
                if key in reference:
                    table.delete(key)
                    del reference[key]
                else:
                    with self.assertRaises(KeyError):
                        table.delete(key)

            self.assertEqual(len(table), len(reference))

            for candidate in range(50):
                self.assertEqual(candidate in table, candidate in reference)

            for stored_key, value in reference.items():
                self.assertEqual(table.get(stored_key), value)


if __name__ == "__main__":
    unittest.main()