import math
from collections import Counter

def calculate_entropy(data: bytes):
    if not data:
        return 0

    counter = Counter(data)
    length = len(data)

    entropy = 0
    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy
