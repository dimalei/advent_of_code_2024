import re

def getInputData(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read()

def calculate_mul(input: str) -> int:  
    a,b = input.split(",")
    a = int(a[4:])
    b = int(b[:-1])
    return a * b

if __name__ == "__main__":
    # data = getInputData("test_input.txt")
    data = getInputData()
    matches = re.findall("(mul\(\d+,\d+\))", data)
    sum = 0
    for match in matches:
        sum += calculate_mul(match)
    print(sum)



