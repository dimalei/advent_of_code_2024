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


def is_safe(report: list, damped=False) -> bool:
    isIncreasing = report[0] < report[1]
    for i in range(0, len(report) - 1):
        difference = abs(report[i] - report[i+1])

        if (isIncreasing != (report[i] < report[i+1]) or (difference < 1 or difference > 3)):
            if (damped):
                for i in range(len(report)):
                    tuned_report = report.copy()
                    tuned_report.pop(i)
                    if is_safe(tuned_report, False):
                        return True
            return False

    return True


def count_safe_reports(reports: list, damped: bool) -> int:
    total_safe = 0
    for r in reports:
        isSafe = is_safe(r, damped)
        if (isSafe):
            total_safe += 1
    return total_safe


if __name__ == "__main__":
    # test data
    # reports = getInputData("test_input.txt")
    # real data
    reports = getInputData()

    total_safe = count_safe_reports(reports, True)

    print(f'Total reports: {len(reports)}')
    print(f'Total un-safe reports: {len(reports) - total_safe}')
    print(f'Total safe reports: {total_safe}')
