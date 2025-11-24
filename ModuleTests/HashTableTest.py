from hash_table import HashTable

def test_insert_and_lookup():
    ht = HashTable(size=10)

    ht.insert("1", "Package1")
    ht.insert("2", "Package2")

    assert ht.lookup("1") == "Package1"
    assert ht.lookup("2") == "Package2"
    assert ht.lookup("999") is None

    print("Hash table insert/lookup: OK")

if __name__ == "__main__":
    test_insert_and_lookup()
    print("Hash table insert/lookup: OK")