def get_input(file_name="test_input.txt"):
    with open(file_name, "r") as f:
        out = []
        for line in f:
            out.append(line)
        return out


def get_disk(map: str):
    out = []
    for index, digit in enumerate(map):
        if index % 2 == 0:
            file = index//2
        else:
            file = "."
        for c in range(int(digit)):
            out.append(file)
    return out


def fragment(disk: list):
    empy_space = disk.count(".")
    counter = 1
    for i in range(empy_space):
        last_digit = disk.pop(-1)
        if last_digit == ".":
            continue
        index = disk.index(".")
        disk[index] = last_digit

        print(f"{counter:05d} of {empy_space:05d}, index: {index}")
        counter += 1
    return disk


def checksum(disk: list):
    out = 0
    for i, f in enumerate(disk):
        out += i * f
    return out


if __name__ == "__main__":
    # input = get_input()
    input = get_input("input.txt")

    for line in input:
        disk = get_disk(line)
        disk = fragment(disk)
        print(checksum(disk))
