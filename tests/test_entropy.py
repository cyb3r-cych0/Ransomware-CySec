from app.entropy import calculate_entropy

def test_entropy_low():
    data = b"aaaaaa"
    entropy = calculate_entropy(data)
    assert entropy < 1

def test_entropy_high():
    import os
    data = os.urandom(1024)
    entropy = calculate_entropy(data)
    assert entropy > 7
