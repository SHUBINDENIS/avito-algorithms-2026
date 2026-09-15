def is_palindrome(number: int) -> bool:
    """Проверяет, совпадает ли число с записью его цифр в обратном порядке."""
    original_number = number
    reversed_number = 0

    while number > 0:
        digit = number % 10
        reversed_number = reversed_number * 10 + digit
        number //= 10

    return original_number == reversed_number


def main() -> None:
    number = int(input())
    print(is_palindrome(number))


if __name__ == "__main__":
    main()
