def two_sum(arr: list[int], k: int) -> tuple[int, int]:
    seen = {}

    for i, x in enumerate(arr):
        complement = k - x

        if complement in seen:
            return seen[complement], i

        seen[x] = i

    raise ValueError("Пара с нужной суммой не найдена")


def main() -> None:
    arr = list(map(int, input().split()))
    k = int(input())
    i, j = two_sum(arr, k)
    print(i, j)


if __name__ == "__main__":
    main()