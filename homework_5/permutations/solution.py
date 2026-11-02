from pathlib import Path
from runpy import run_path


tracer = run_path(str(Path(__file__).resolve().parents[1] / "tracer" / "solution.py"))["tracer"]


def permutations(nums, trace=False):
    nums = list(nums)
    result = []
    path = []
    used = [False] * len(nums)

    def visit(path):
        if len(path) == len(nums):
            result.append(path.copy())
            return path.copy()

        seen = set()
        for index, value in enumerate(nums):
            if used[index] or value in seen:
                continue
            seen.add(value)
            used[index] = True
            path.append(value)
            visit(path)
            path.pop()
            used[index] = False
        return None

    if trace:
        visit = tracer(visit)
    visit(path)
    return result


if __name__ == "__main__":
    print(permutations([1, 2, 3], trace=True))
