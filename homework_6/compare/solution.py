from functools import wraps
from random import Random
from statistics import median
from time import perf_counter


def mergesort(values):
    if len(values) <= 1:
        return list(values)

    middle = len(values) // 2
    left = mergesort(values[:middle])
    right = mergesort(values[middle:])
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


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

    def sort_range(low, high):
        while low < high:
            pivot = partition(result, low, high)
            if pivot - low < high - pivot:
                sort_range(low, pivot - 1)
                low = pivot + 1
            else:
                sort_range(pivot + 1, high)
                high = pivot - 1

    sort_range(0, len(result) - 1)
    return result


def timed(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = function(*args, **kwargs)
        return result, perf_counter() - start

    return wrapper


def benchmark(size=4000, repeats=7):
    ordered = list(range(size))
    shuffled = ordered.copy()
    Random(42).shuffle(shuffled)
    sorters = (timed(mergesort), timed(quicksort))
    rows = []

    for label, values in (("shuffled", shuffled), ("sorted", ordered)):
        samples = ([], [])
        for repeat in range(repeats):
            for offset in range(len(sorters)):
                index = (repeat + offset) % len(sorters)
                result, elapsed = sorters[index](values)
                if result != ordered:
                    raise AssertionError("incorrect sort result")
                samples[index].append(elapsed)
        rows.append((label, median(samples[0]), median(samples[1])))

    return rows


if __name__ == "__main__":
    print(f"{'input':<12} {'merge, ms':>10} {'quick, ms':>10} {'quick/merge':>12}")
    for label, merge_time, quick_time in benchmark():
        print(f"{label:<12} {merge_time * 1000:10.3f} {quick_time * 1000:10.3f}"
              f" {quick_time / merge_time:12.2f}")
