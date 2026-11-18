from random import randrange


def kth_largest(nums, k):
    if not 1 <= k <= len(nums):
        raise ValueError("k must be between 1 and len(nums)")

    values = list(nums)
    target = len(values) - k
    low = 0
    high = len(values) - 1

    while low < high:
        pivot = values[randrange(low, high + 1)]
        less = low
        index = low
        greater = high

        while index <= greater:
            if values[index] < pivot:
                values[less], values[index] = values[index], values[less]
                less += 1
                index += 1
            elif values[index] > pivot:
                values[index], values[greater] = values[greater], values[index]
                greater -= 1
            else:
                index += 1

        if target < less:
            high = less - 1
        elif target > greater:
            low = greater + 1
        else:
            return pivot

    return values[low]
