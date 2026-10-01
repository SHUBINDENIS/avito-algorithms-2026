class HashTable:
    def __init__(self, capacity: int = 8) -> None:
        if capacity <= 0:
            raise ValueError("Размер таблицы должен быть положительным")

        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value) -> None:
        bucket = self._bucket(key)

        for pair in bucket:
            if pair[0] is key or pair[0] == key:
                pair[1] = value
                return

        bucket.append([key, value])
        self._size += 1

        if self._size / len(self._buckets) > 0.75:
            self._resize()

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._buckets = [[] for _ in range(len(old_buckets) * 2)]

        for bucket in old_buckets:
            for key, value in bucket:
                self._bucket(key).append([key, value])

    def get(self, key):
        for stored_key, value in self._bucket(key):
            if stored_key is key or stored_key == key:
                return value

        raise KeyError(key)

    def delete(self, key) -> None:
        bucket = self._bucket(key)

        for i, pair in enumerate(bucket):
            if pair[0] is key or pair[0] == key:
                bucket.pop(i)
                self._size -= 1
                return

        raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key) -> bool:
        for stored_key, _ in self._bucket(key):
            if stored_key is key or stored_key == key:
                return True

        return False

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value) -> None:
        self.put(key, value)

    def __delitem__(self, key) -> None:
        self.delete(key)