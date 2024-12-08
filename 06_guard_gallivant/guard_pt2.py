from enum import Enum
import copy


def get_input_data(filename="input.txt"):
    with open(filename, "r") as f:
        '''create a 2 dimensional char array from the input file'''
        data = []
        for y, line in enumerate(f):
            line.strip()
            data.append([])
            for x in line:
                data[y].append(x)

    return data


class Direction(Enum):
    NORTH = (0, -1, '|')
    EAST = (1, 0, '-')
    SOUTH = (0, 1, '|')
    WEST = (-1, 0, '-')

    def rotate_cw(current_direction):
        current_direction_index = list(Direction).index(current_direction)
        next_direction_index = (current_direction_index + 1) % len(Direction)
        next_direction = list(Direction)[next_direction_index]
        return next_direction


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def step(self, heading: Direction):
        return Position(self.x + heading.value[0], self.y + heading.value[1])

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"

    def copy(self):
        return Position(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Position):
            if self.x == other.x and self.y == other.y:
                return True
        return False


class Map:
    def __init__(self, map_data: list):
        self.data = copy.deepcopy(map_data)
        self.starting_position = self.get_starting_position()

    def get_at(self, pos: Position):
        if pos.y >= 0 and pos.y < len(self.data):
            if pos.x >= 0 and pos.x < len(self.data[pos.y]):
                return self.data[pos.y][pos.x]
        # return E for exit
        return 'E'

    def put_at(self, object: str, pos: Position):
        if pos.y > 0 and pos.y < len(self.data):
            if pos.x > 0 and pos.x < len(self.data[pos.y]):
                self.data[pos.y][pos.x] = object

    def get_starting_position(self) -> Position:
        for y, line in enumerate(self.data):
            if "^" in line:
                starting_position = Position(line.index("^"), y)
                self.put_at('.', starting_position)
                return starting_position

    def count_objects(self, object: str):
        counter = 0
        for line in self.data:
            for row in line:
                if object == row:
                    counter += 1
        return counter

    def get_trail_locations(self) -> list:
        locations = []
        for y, l in enumerate(self.data):
            for x, object in enumerate(l):
                if object == Direction.NORTH.value[2] or object == Direction.EAST.value[2] or object == '+':
                    locations.append(Position(x, y))
        return locations

    def __str__(self):
        out = ""
        for y, l in enumerate(self.data):
            out += f"{y:03} "
            for r in l:
                if r == '.':
                    r = ' '
                out += r
        return out


class Guard:
    def __init__(self, position: Position, heading: Direction):
        self.pos = position
        self.heading = heading

    def step(self, map_data: Map):
        self.draw_trail(map_data)
        self.pos = self.pos.step(self.heading)

    def draw_trail(self, map_data: Map):
        object_current_location = map_data.get_at(self.pos)

        if self.heading == Direction.NORTH or self.heading == Direction.SOUTH:
            if object_current_location == '.':
                map_data.put_at(Direction.NORTH.value[2], self.pos)
            elif object_current_location == Direction.EAST.value[2]:
                map_data.put_at("+", self.pos)

        if self.heading == Direction.WEST or self.heading == Direction.EAST:
            if object_current_location == '.':
                map_data.put_at(Direction.WEST.value[2], self.pos)
            elif object_current_location == Direction.NORTH.value[2]:
                map_data.put_at('+', self.pos)

    def see_ahead(self, map_data: Map):
        return map_data.get_at(self.pos.step(self.heading))

    def rotate_cw(self, map_data: Map):
        map_data.put_at('+', self.pos)
        self.heading = self.heading.rotate_cw()

    def running_in_circles(self, map_data: Map) -> bool:
        if map_data.get_at(self.pos) == '+':
            object_ahead = self.see_ahead(map_data)
            if object_ahead == '#' or object_ahead == 'O':
                return True
        return False

    def move(self, map_data: Map):
        # check if an obstacle is ahead
        object_ahead = self.see_ahead(map_data)

        if object_ahead == '#' or object_ahead == 'O':
            self.rotate_cw(map_data)

            # and check if another one is in the way
            object_ahead = self.see_ahead(map_data)
            if object_ahead == '#' or object_ahead == 'O':
                self.rotate_cw(map_data)

        self.step(map_data)

    def run(self, map_data: Map):
        while True:

            if self.running_in_circles(map_data):
                return 'circle'

            self.move(map_data)
            object_ahead = self.see_ahead(map_data)

            if object_ahead == 'E':
                self.draw_trail(map_data)
                return 'exit'


if __name__ == "__main__":
    obstacles = 0
    potential_locations = []

    # setup initial run
    # input_data = get_input_data("test_input.txt")
    input_data = get_input_data()

    my_map = Map(input_data)
    my_guard = Guard(my_map.starting_position, Direction.NORTH)

    # initial run
    my_guard.run(my_map)

    # show trailed map
    print(my_map)

    # get trail locations
    potential_locations = my_map.get_trail_locations()
    # remove starting position
    potential_locations = list(
        filter(lambda x: x != my_map.starting_position, potential_locations))

    # place an obstacle at each potential location
    for p in potential_locations:
        # reset map & guard
        my_map = Map(input_data)
        my_guard = Guard(my_map.starting_position, Direction.NORTH)

        # place obstacle
        my_map.put_at('O', p)

        # check if obstruction resultet in circle
        if my_guard.run(my_map) == 'circle':
            obstacles += 1
            print(f"loops found: {obstacles}")

    print(f"Total possible obstacles: {obstacles}")
