class HashTable:
    def __init__(self, size=40):
        self.size = size
        self.hash_table = [[] for _ in range(self.size)]

    # Create hash function to choose bucket for packageID
    def hash(self, key):
        return int(key) % self.size

    def insert(self, key: int, value):  # Custom insert function
        hash_bucket = self.hash(key)
        curr_bucket = self.hash_table[hash_bucket]

        for i, (k, v) in enumerate(curr_bucket):
            if k == key:
                return

        curr_bucket.append((key, value))

    # Lookup function to return package object
    def lookup(self, key: int):
        hash_bucket = self.hash(key)
        curr_bucket = self.hash_table[hash_bucket]

        for k, v in curr_bucket:
            if k == key:
                return v
        return None
