from itertools import product


def get_input_data(filename="input.txt"):
    """(result, [operad1, operan2, ...])"""
    with open(filename, "r") as f:
        data = []
        for line in f:
            result, op_str = line.strip().split(":")
            op_str = op_str.strip().split(" ")
            operands = []
            for o in op_str:
                operands.append(int(o))
            data.append((int(result), operands))
        return data


def check_calibration_truth(calibration: tuple, elements: list) -> bool:

    print(f"checking calibration: {calibration}")

    calibration_result = calibration[0]
    operands = calibration[1]

    comb = product(elements, repeat=len(operands)-1)

    # print(list(comb))

    # return False

    for combination in comb:
        result = operands[0]

        for index, operator in enumerate(combination):
            if (operator == '+'):
                result += operands[index + 1]
            elif (operator == '*'):
                result *= operands[index + 1]

        if (calibration_result == result):
            print(f"solution for this calibration: {calibration}:")
            print(combination)
            return True

    print(f"solution cant be solved: {calibration}:")
    return False


if __name__ == "__main__":
    # input_data = get_input_data("test_input.txt")
    input_data = get_input_data()

    sum = 0
    for calibration in input_data:
        if check_calibration_truth(calibration, ['+', '*']):
            sum += calibration[0]

    print(f"sum of all true calibrations: {sum}")
