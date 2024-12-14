def get_input(file="test_input.txt"):
    with open(file, "r") as f:
        data_str = f.read().strip().split(" ")
        return [int(d) for d in data_str]


def digits(number: int) -> int:
    return len(str(number))


def blink(row: list) -> list:
    out = []
    for number in row:
        if number == 0:
            out.append(1)
        elif digits(number) % 2 == 0:
            out.append(int((str(number))[:digits(number)//2]))
            out.append(int((str(number))[digits(number)//2:]))
        else:
            out.append(number * 2024)
    return out


if __name__ == "__main__":
    # input = get_input()
    input = get_input("input.txt")

    print(input)

    for i in range(25):
        input = blink(input)

    print(len(input))
