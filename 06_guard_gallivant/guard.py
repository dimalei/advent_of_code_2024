from enum import Enum
import os


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
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

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


class Map:
    def __init__(self, map_data: list):
        self.data = map_data.copy()

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
                return Position(line.index("^"), y)

    def count_objects(self, object: str):
        counter = 0
        for line in self.data:
            for row in line:
                if object == row:
                    counter += 1
        return counter

    def __str__(self):
        out = ""
        for l in self.data:
            for r in l:
                out += r
            out += "\n"
        return out


class Guard:
    def __init__(self, position: Position, heading: Direction):
        self.pos = position
        self.heading = heading

    def move(self, map_data: Map):
        map_data.put_at('X', self.pos)
        self.pos = self.pos.step(self.heading)

    def see_ahead(self, map_data: Map):
        return map_data.get_at(self.pos.step(self.heading))

    def rotate_cw(self):
        self.heading = self.heading.rotate_cw()


if __name__ == "__main__":
    # my_map = Map(get_input_data("test_input.txt"))
    my_map = Map(get_input_data())
    my_guard = Guard(my_map.get_starting_position(), Direction.NORTH)

    i = 100

    # print(Direction.rotate_cw(Direction.SOUTH))
    # print(my_map.get_at(Position(0,4)))
    # print(my_map.data[0][4])

    while i > 0:
        # i -= 1
        # os.system('cls' if os.name == 'nt' else 'clear')
        # print(my_map)

        object_ahead = my_guard.see_ahead(my_map)
        print(object_ahead)
        if object_ahead != '#':
            my_guard.move(my_map)
        else:
            my_guard.rotate_cw()

        if object_ahead == 'E':
            break

    print(my_map)
    print("found an exit")

    print(f"Locations visited: {my_map.count_objects('X')}")
