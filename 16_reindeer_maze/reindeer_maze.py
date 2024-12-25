from enum import Enum


class Vector2:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self._x + other._x, self._y + other._y)
        return self

    def __hash__(self):
        return hash((self._x, self._y))

    def __eq__(self, other):
        if not isinstance(other, Vector2):
            return False
        return self._x == other._x and self._y == other._y


class Direction(Enum):
    NORTH = Vector2(0, -1)
    EAST = Vector2(1, 0)
    SOUTH = Vector2(0, 1)
    WEST = Vector2(-1, 0)

    def turn_cw(self):
        directions = list(Direction)
        current_index = directions.index(self)
        next_index = (current_index + 1) % len(directions)
        return directions[next_index]

    def turn_ccw(self):
        directions = list(Direction)
        current_index = directions.index(self)
        next_index = (current_index - 1) % len(directions)
        return directions[next_index]

    def __str__(self):
        if self == Direction.NORTH:
            return "^"
        if self == Direction.EAST:
            return ">"
        if self == Direction.SOUTH:
            return "v"
        if self == Direction.WEST:
            return "<"


class Path:
    def __init__(self, pos: Vector2):
        self._pos = pos

    @property
    def pos(self) -> Vector2:
        return self._pos

    def __eq__(self, other):
        if isinstance(other, Path):
            return self._pos == other._pos
        return False

    def __hash__(self):
        return hash(self._pos)
    
    def __str__(self):
        return f"Path({self._pos.x},{self._pos.y})"


class Exit(Path):
    def __init__(self, pos: Vector2):
        super().__init__(pos)


class Start(Path):
    def __init__(self, pos: Vector2):
        super().__init__(pos)


class Trail(Path):
    def __init__(self, pos, direction: Direction):
        super().__init__(pos)
        self.direction = direction

    def __str__(self):
        return self.direction.__str__()


def parse_input(file_name="test_input.txt") -> list:
    out = []
    with open(file_name, "r") as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line):
                if char == ".":
                    out.append(Path(Vector2(x, y)))
                elif char == "E":
                    out.append(Exit(Vector2(x, y)))
                elif char == "S":
                    out.append(Start(Vector2(x, y)))
        return out


class Maze:
    def __init__(self, paths):
        self.paths = paths
        self.player_pos = self.get_start()
        self.player_heading = Direction.EAST
        self.player_trail = []

    def get_start(self):
        for path in paths:
            if isinstance(path, Start):
                return path.pos

    def see_ahead(self):
        left_location = Path(self.player_pos + self.player_heading.turn_ccw())
    
        return left

    def __str__(self):
        out = ""
        max_x = max([path.pos.x for path in self.paths])
        max_y = max([path.pos.y for path in self.paths])

        for y in range(max_y + 2):
            for x in range(max_x + 2):

                location = Path(Vector2(x, y))

                if location.pos == self.player_pos:
                    out += self.player_heading.__str__()

                elif location in self.player_trail:
                    index = self.player_trail.index(location)
                    out += self.player_trail[index]

                elif location in self.paths:
                    index = self.paths.index(location)
                    location = self.paths[index]
                    if isinstance(location, Exit):
                        out += "E"
                    elif isinstance(location, Start):
                        out += "S"
                    else:
                        out += "."

                else:
                    out += "#"
            out += "\n"
        return out


if __name__ == "__main__":
    paths = parse_input()
    print(paths)

    maze = Maze(paths)

    print(maze)
    print(maze.see_ahead())

    # path1 = Path(Vector2(12, 13))
    # path2 = Exit(Vector2(12, 13))

    # my_list = [path1]

    # print(path2 in my_list)
