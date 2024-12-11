def get_input_data(filename="input.txt"):
    with open(filename, "r") as f:
        data = []
        for line in f:
            data.append(line.strip())
        return data


def get_antennas(input_data: list):
    """data format:
    {
    'frequency': {
        (location_1_y,location_1_x),
        (location_2_y,location_2_x)
        }
    }
    """
    data = {}
    for y, line in enumerate(input_data):
        for x, char in enumerate(line):
            if char != '.':
                if char not in data.keys():
                    data[char] = set()
                data[char].add((x, y))
    return data


def get_resonace_loactions(max_x: int, max_y: int, antenna1: tuple, antenna2: tuple):
    dx, dy = (antenna1[0] - antenna2[0], antenna1[1] - antenna2[1])
    resonances = set()

    # 1st direction
    n = 1
    while True:
        r_x = antenna1[0] + dx * n
        r_y = antenna1[1] + dy * n
        if (r_x < 0 or r_x > max_x or r_y < 0 or r_y > max_y):
            break
        resonances.add((r_x, r_y))
        n += 1

    # 2nd direction
    n = 1
    while True:
        r_x = antenna2[0] - dx * n
        r_y = antenna2[1] - dy * n
        if (r_x < 0 or r_x > max_x or r_y < 0 or r_y > max_y):
            break
        resonances.add((r_x, r_y))
        n += 1
    
    #adding the antennas themselves
    resonances.add(antenna1)
    resonances.add(antenna2)

    return resonances


def print_map(map_data: list, resonance_locations=set()):
    map_out = ""
    for y, line in enumerate(map_data):
        # resonance map
        for x, char in enumerate(line):
            if (x, y) in resonance_locations:
                map_out += '#'
            else:
                map_out += char
        # vanilla map
        map_out += "  |  "
        for char in map_data[y]:
            map_out += char
        map_out += '\n'
    print(map_out)


if __name__ == "__main__":
    # input_data = get_input_data("test_input2.txt")
    input_data = get_input_data()

    antenna_locations = get_antennas(input_data)
    all_resonance_locations = set()

    for frequency in antenna_locations.keys():
        antenna_list = list(antenna_locations[frequency])
        for i, antenna in enumerate(antenna_list):

            for j in range(i + 1, len(antenna_list)):

                antenna1 = antenna_list[i]
                antenna2 = antenna_list[j]
                resonances = get_resonace_loactions(
                    len(input_data[0])-1, len(input_data)-1, antenna1, antenna2)

                all_resonance_locations = all_resonance_locations.union(
                    resonances)

    print_map(input_data, all_resonance_locations)

    print(f"total resonances within map: {len(all_resonance_locations)}")
