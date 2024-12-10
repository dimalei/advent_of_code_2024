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


def get_resonace_loactions(antenna1: tuple, antenna2: tuple):
    dx, dy = (antenna1[0] - antenna2[0], antenna1[1] - antenna2[1])
    resonance1 = (antenna1[0] + dx, antenna1[1] + dy)
    resonance2 = (antenna2[0] - dx, antenna2[1] - dy)
    return {resonance1, resonance2}


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


def out_of_bounds(size_x: int, size_y: int, location: tuple):
    return not (location[0] < 0 or location[0] >= size_x or location[1] < 0 or location[1] >= size_y)


if __name__ == "__main__":
    # input_data = get_input_data("test_input.txt")
    input_data = get_input_data()

    antenna_locations = get_antennas(input_data)
    all_resonance_locations = set()

    for frequency in antenna_locations.keys():
        antenna_list = list(antenna_locations[frequency])
        for i, antenna in enumerate(antenna_list):

            for j in range(i + 1, len(antenna_list)):

                antenna1 = antenna_list[i]
                antenna2 = antenna_list[j]
                resonances = get_resonace_loactions(antenna1, antenna2)

                all_resonance_locations = all_resonance_locations.union(
                    resonances)

    # filter out of bounds resonace locations
    filter_locations = set(filter(lambda x: out_of_bounds(
        len(input_data[0]), len(input_data), x), all_resonance_locations))

    print_map(input_data, all_resonance_locations)

    print(f"total resonances within map: {len(filter_locations)}")
