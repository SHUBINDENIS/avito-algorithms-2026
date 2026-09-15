from math import isqrt


def count_primes(n: int) -> int:
    """Возвращает количество простых чисел, меньших n."""
    if n <= 2:
        return 0

    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    for divisor in range(2, isqrt(n - 1) + 1):
        if is_prime[divisor]:
            for multiple in range(divisor * divisor, n, divisor):
                is_prime[multiple] = False

    return sum(is_prime)


def main() -> None:
    n = int(input())
    print(count_primes(n))


if __name__ == "__main__":
    main()
