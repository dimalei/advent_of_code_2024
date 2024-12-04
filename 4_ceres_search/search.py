def getInputData(filename="input.txt"):
    with open(filename, "r") as f:
        out = []
        for line in f:
            out.append(line.strip())
    return out

# part 1
def find_string(data: list, search_string: str):
    matches = 0
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == search_string[0]:
                matches += star_search(data, x, y, search_string)
    return matches


def star_search(data: list, x: int, y: int, search_string: str):
    matches = 0
    east = True
    west = True
    south = True
    north = True
    southeast = True
    northwest = True
    northeast = True
    southwest = True

    for offset in range(1, len(search_string)):

        # east
        if (x + (len(search_string) - 1) < len(data[y])) and east:
            if data[y][x + offset] != search_string[offset]:
                east = False
        else:
            east = False

        # west
        if (x - (len(search_string) - 1) >= 0) and west:
            if data[y][x - offset] != search_string[offset]:
                west = False
        else:
            west = False

        # south
        if (y + (len(search_string) - 1) < len(data)) and south:
            if data[y + offset][x] != search_string[offset]:
                south = False
        else:
            south = False

        # north
        if (y - (len(search_string) - 1) >= 0) and north:
            if data[y - offset][x] != search_string[offset]:
                north = False
        else:
            north = False

        # southeast
        if (y + (len(search_string) - 1) < len(data)) and (x + (len(search_string) - 1) < len(data[y])) and southeast:
            if data[y + offset][x + offset] != search_string[offset]:
                southeast = False
        else:
            southeast = False

        # northwest
        if (y - (len(search_string) - 1) >= 0) and (x - (len(search_string) - 1) >= 0) and northwest:
            if data[y - offset][x - offset] != search_string[offset]:
                northwest = False
        else:
            northwest = False

        # soutwest
        if (y + (len(search_string) - 1) < len(data)) and (x - (len(search_string) - 1) >= 0) and southwest:
            if data[y + offset][x - offset] != search_string[offset]:
                southwest = False
        else:
            southwest = False

        # northeast
        if (y - (len(search_string) - 1) >= 0) and (x + (len(search_string) - 1) < len(data[y])) and northeast:
            if data[y - offset][x + offset] != search_string[offset]:
                northeast = False
        else:
            northeast = False

    if (east):
        matches += 1

    if (west):
        matches += 1

    if (south):
        matches += 1

    if (north):
        matches += 1

    if (southeast):
        matches += 1

    if (northwest):
        matches += 1

    if (southwest):
        matches += 1

    if (northeast):
        matches += 1

    return matches

#part 2
def a_search(data: list):
    matches = 0
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == 'A':
                matches += ms_search(data, x, y)
    return matches


def ms_search(data, x, y):
    if (x - 1 >= 0) and (x + 1 < len(data[y])) and (y - 1 >= 0) and (y + 1 < len(data)):
        se_string = data[y-1][x-1] + data[y+1][x+1]
        ne_string = data[y+1][x-1] + data[y-1][x+1]
        se = se_string == 'MS' or se_string == 'SM'
        ne = ne_string == 'MS' or ne_string == 'SM'
        if se and ne:
            return 1
    return 0


if __name__ == "__main__":
    # data = getInputData("test_input.txt")
    data = getInputData()

    print(find_string(data, "XMAS"))
    print(a_search(data))
