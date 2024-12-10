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

    calibration_result = calibration[0]
    operands = calibration[1]

    comb = product(elements, repeat=len(operands)-1)

    for combination in comb:
        result = operands[0]

        for index, operator in enumerate(combination):
            if (operator == '+'):
                result += operands[index + 1]
            elif (operator == '*'):
                result *= operands[index + 1]
            elif (operator == 'c'):
                result *= (10 ** len(str(operands[index + 1])))
                result += operands[index + 1]

        if (calibration_result == result):
            return True

    return False


def sum_of_calibrations(input_data: list, operators: list) -> int:
    sum = 0
    for i, calibration in enumerate(input_data):
        if check_calibration_truth(calibration, operators):
            sum += calibration[0]

        print(f"checked {i:03} out of {
              len(input_data)} calibrations. Total Sum {sum}")
        
    return sum


if __name__ == "__main__":
    # input_data = get_input_data("test_input.txt")
    input_data = get_input_data()

    # print(f"Part 1: sum of all true calibrations: {sum_of_calibrations(input_data, ['+', '*'])}")
    print(f"Part 2: sum of all true calibrations with concat: {sum_of_calibrations(input_data, ['+', '*', 'c'])}")
