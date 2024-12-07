import re


def getInputData(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read()


def calculate_mul(matches: str) -> int:
    if not re.fullmatch("mul\(\d+,\d+\)", matches):
        return 0
    a, b = re.findall("\d+", matches)
    return int(a) * int(b)


def calculate_matches(matches: str) -> int:
    do = True
    sum = 0
    for match in matches:
        if match == 'do()':
            do = True
        elif match == "don't()":
            do = False
        elif re.fullmatch("mul\(\d+,\d+\)", match) and do:
            sum += calculate_mul(match)
    return sum


if __name__ == "__main__":
    # data = getInputData("test_input.txt")
    data = getInputData()

    mul_matches = re.findall("(mul\(\d+,\d+\))", data)
    sum = calculate_matches(mul_matches)
    print(f'part1: {sum}')

    mul_do_dont_matches = re.findall("mul\(\d+,\d+\)|do\\(\)|don't\(\)", data)
    sum2 = calculate_matches(mul_do_dont_matches)
    print(f'part2: {sum2}')
