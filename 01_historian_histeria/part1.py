def getInputLists(filename="input.txt"):
    l1, l2 = [], []
    with open(filename, "r") as f:
        for line in f:
            a, b = line.strip().split("   ")
            l1.append(int(a))
            l2.append(int(b))
    return (l1, l2)


def get_distance(a: list, b: list) -> int:
    a.sort()
    b.sort()
    total_distance = 0
    for i, a_n in enumerate(a):
        distance = abs(a_n - b[i])
        total_distance += distance
    return total_distance


def similarity_score(a: list, b: list) -> int:
    score = 0
    for id_a in a:
        appearances = 0
        for id_b in b:
            if (id_a == id_b):
                appearances += 1
        score += id_a * appearances
    return score


if (__name__) == "__main__":
    # test list
    # a, b = getInputLists("test_input.txt")
    # real list
    a, b = getInputLists()

    print(get_distance(a, b))
    print(similarity_score(a, b))
