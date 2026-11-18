def mergesort(values):
    source = list(values)
    size = len(source)
    target = [None] * size
    width = 1

    while width < size:
        for start in range(0, size, 2 * width):
            middle = min(start + width, size)
            end = min(start + 2 * width, size)
            left = start
            right = middle

            for index in range(start, end):
                if left < middle and (right == end or source[left] <= source[right]):
                    target[index] = source[left]
                    left += 1
                else:
                    target[index] = source[right]
                    right += 1

        source, target = target, source
        width *= 2

    return source


def partition(values, low, high):
    pivot = values[high]
    boundary = low
    for index in range(low, high):
        if values[index] < pivot:
            values[boundary], values[index] = values[index], values[boundary]
            boundary += 1
    values[boundary], values[high] = values[high], values[boundary]
    return boundary


def quicksort(values):
    result = list(values)
    pending = [(0, len(result) - 1)]

    while pending:
        low, high = pending.pop()
        while low < high:
            pivot = partition(result, low, high)
            if pivot - low < high - pivot:
                if pivot + 1 < high:
                    pending.append((pivot + 1, high))
                high = pivot - 1
            else:
                if low < pivot - 1:
                    pending.append((low, pivot - 1))
                low = pivot + 1

    return result
