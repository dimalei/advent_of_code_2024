def get_input(file="test_input.txt"):
    with open(file, "r") as f:
        data_str = f.read().strip().split(" ")
        return [int(d) for d in data_str]


def get_dictionary(input: list):
    out = {}
    for number in input:
        if number in out.keys():
            out[number] += 1
        else:
            out[number] = 1
    return out


def digits(number: int) -> int:
    return len(str(number))


def blink(input: dict) -> list:
    out = {}

    for number in input.keys():
        if number == 0:

            if 1 in out.keys():
                out[1] += input[number]
            else:
                out[1] = input[number]

        elif digits(number) % 2 == 0:
            fist_half = int((str(number))[:digits(number)//2])
            second_half = int((str(number))[digits(number)//2:])

            if fist_half in out.keys():
                out[fist_half] += input[number]
            else:
                out[fist_half] = input[number]
            if second_half in out.keys():
                out[second_half] += input[number]
            else:
                out[second_half] = input[number]

        else:
            value = number * 2024

            if value in out.keys():
                out[value] += input[number]
            else:
                out[value] = input[number]

    return out


if __name__ == "__main__":
    # input = get_input()
    input = get_input("input.txt")

    input_dict = get_dictionary(input)

    print(input_dict)

    for i in range(75):
        input_dict = blink(input_dict)

    print(input_dict)
    print(sum(input_dict.values()))
