def get_input_list(filename="input.txt"):
    list_a, list_b = [], []
    with open(filename, "r") as f:
        for line in f:
            num_a, num_b = line.strip().split("   ")
            list_a.append(int(num_a))
            list_b.append(int(num_b))
    return (list_a, list_b)


def get_distance(list_a: list, list_b: list) -> int:
    list_a.sort()
    list_b.sort()
    total_distance = 0
    for i, num_a in enumerate(list_a):
        distance = abs(num_a - list_b[i])
        total_distance += distance
    return total_distance


def similarity_score(list_a: list, list_b: list) -> int:
    score = 0
    for num_a in list_a:
        appearances = 0
        for num_b in list_b:
            if (num_a == num_b):
                appearances += 1
        score += num_a * appearances
    return score


if (__name__) == "__main__":
    # test list
    # list_a, list_b = getInputLists("test_input.txt")
    # real list
    list_a, list_b = get_input_list()

    print(get_distance(list_a, list_b))
    print(similarity_score(list_a, list_b))
