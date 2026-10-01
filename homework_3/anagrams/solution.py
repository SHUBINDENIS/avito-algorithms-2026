def group_anagrams(words: list[str]) -> list[list[str]]:
    groups = {}

    for word in words:
        key = "".join(sorted(word))

        if key not in groups:
            groups[key] = []

        groups[key].append(word)

    return list(groups.values())


def main() -> None:
    words = input().split()
    print(group_anagrams(words))


if __name__ == "__main__":
    main()