def getInputData(filename="input.txt"):
    data = []
    with open(filename, "r") as f:
        for line in f:
            str_values = line.strip().split(" ")
            int_values = []
            for str_value in str_values:
                int_values.append(int(str_value))
            data.append(int_values)
    return data


def asessSafety(data: list) -> bool:
    isIncreasing = data[0] < data[1]
    for i in range(0, len(data) - 1):
        difference = abs(data[i] - data[i+1])

        # print(f'isIncreasing: {isIncreasing}')
        # print(f'is actually increasing: {(data[i] < data[i+1])}')

        if(isIncreasing != (data[i] < data[i+1])):
            # print('direction changed')
            return False
        
        if(difference < 1 or difference > 3):
            # print('difference exeeded')
            return False
        
    return True


if __name__ == "__main__":
    # test data
    # reports = getInputData("test_input.txt")
    # real data
    reports = getInputData()


    # print(reports[28])
    # print(asessSafety(reports[28]))

    # print(reports[448])
    # print(asessSafety(reports[448]))

    total_safe = 0
    for r in reports:
        isSafe = asessSafety(r)
        # print(isSafe)
        if (isSafe):
            total_safe += 1
    
    print(f'Total reports: {len(reports)}')
    print(f'Total un-safe reports: {len(reports) - total_safe}')
    print(f'Total safe reports: {total_safe}')

