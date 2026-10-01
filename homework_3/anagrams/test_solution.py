import unittest

from pathlib import Path
from runpy import run_path

group_anagrams = run_path(str(Path(__file__).with_name("solution.py")))["group_anagrams"]


def normalize(groups):
    return sorted(sorted(group) for group in groups)


class GroupAnagramsTest(unittest.TestCase):
    def test_groups(self):
        cases = [
            (
                ["eat", "tea", "tan", "ate", "nat", "bat"],
                [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
            ),
            ([], []),
            (["hello"], [["hello"]]),
            ([""], [[""]]),
            (["a", "a"], [["a", "a"]]),
            (["a", "b", "c"], [["a"], ["b"], ["c"]]),
            (["abc", "cab", "bca"], [["abc", "cab", "bca"]]),
            (["ab", "aab", "baa"], [["ab"], ["aab", "baa"]]),
        ]
        for words, expected in cases:
            with self.subTest(words=words):
                result = group_anagrams(words)
                self.assertEqual(normalize(result), normalize(expected))


if __name__ == "__main__":
    unittest.main()