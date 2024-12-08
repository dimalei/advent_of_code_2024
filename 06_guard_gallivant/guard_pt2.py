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

        self.pos = self.pos.step(self.heading)

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

    def run(self, map_data: Map):
        while True:
            object_ahead = my_guard.see_ahead(map_data)

            if object_ahead == '#' or object_ahead == 'O':
                my_guard.rotate_cw(my_map)
            else:
                my_guard.move(my_map)

            if my_guard.running_in_circles(my_map):
                print("running in circles")
                return 'circle'

            if object_ahead == 'E':
                return 'exit'


if __name__ == "__main__":
    # map_data = get_input_data("test_input.txt")

    obstacles = 0
    skip_steps = 0

    while True:
        my_map = Map(get_input_data("test_input.txt"))
        # my_map = Map(get_input_data())

        starting_position = my_map.get_starting_position()
        my_guard = Guard(starting_position, Direction.NORTH)

        # my_map.put_at('O', Position(3, 6))  # force a circle
        # print(my_map)

        # moving forward without placing an obstacle
        for i in range(skip_steps):

            object_ahead = my_map.get_at(my_guard.pos.step(my_guard.heading))
            if object_ahead == '#' or object_ahead == 'O':
                my_guard.rotate_cw(my_map)
            my_guard.move(my_map)

        # end if guard made it to an exit
        if my_map.get_at(my_guard.pos.step(my_guard.heading)) == 'E':
            print('exit found')
            break
        # palce an obstacle at the next position
        my_map.put_at('O', my_guard.pos.step(my_guard.heading))

        if my_guard.run(my_map) == 'circle':
            obstacles += 1
            print("================")
            print(f"option {obstacles}")
            print(my_map)
            print("================")

        skip_steps += 1

    print(f"steps skipped {skip_steps}")
    print(f"obstacles: {obstacles}")
