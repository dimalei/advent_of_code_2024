import re

def getInputData(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read()

def calculate_mul(input: str) -> int:
    if not re.fullmatch("mul\(\d+,\d+\)", match):
        return 0
    a,b = input.split(",")
    a = int(a[4:])
    b = int(b[:-1])
    return a * b

if __name__ == "__main__":
    # data = getInputData("test_input.txt")
    data = getInputData()
    mul_matches = re.findall("(mul\(\d+,\d+\))", data)
    sum = 0
    for match in mul_matches:
        sum += calculate_mul(match)
    print(sum)

    mul_do_dont_matches = re.findall("mul\(\d+,\d+\)|do\\(\)|don't\(\)", data)
    do = True
    sum2 = 0
    for match in mul_do_dont_matches:
        if match == 'do()':
            do = True
        elif match == "don't()":
            do = False
        elif re.fullmatch("mul\(\d+,\d+\)", match) and do:
            sum2 += calculate_mul(match)
    print(sum2)



