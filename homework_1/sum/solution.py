def max_even_sum(numbers: list[int]) -> int:
    """Возвращает максимальную чётную сумму элементов массива."""
    total = 0
    smallest_odd: int | None = None

    for number in numbers:
        total += number
        if number % 2 == 1 and (smallest_odd is None or number < smallest_odd):
            smallest_odd = number

    if total % 2 == 0:
        return total

    assert smallest_odd is not None
    return total - smallest_odd


def main() -> None:
    numbers = list(map(int, input().split()))
    print(max_even_sum(numbers))


if __name__ == "__main__":
    main()
