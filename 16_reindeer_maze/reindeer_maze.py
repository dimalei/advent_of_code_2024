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

    def __str__(self):
        return f"({self._x},{self._y})"


class Heading(Enum):
    NORTH = Vector2(0, -1)
    EAST = Vector2(1, 0)
    SOUTH = Vector2(0, 1)
    WEST = Vector2(-1, 0)

    def turn_cw(self):
        directions = list(Heading)
        current_index = directions.index(self)
        next_index = (current_index + 1) % len(directions)
        return directions[next_index]

    def turn_ccw(self):
        directions = list(Heading)
        current_index = directions.index(self)
        next_index = (current_index - 1) % len(directions)
        return directions[next_index]

    def __str__(self):
        if self == Heading.NORTH:
            return "^"
        if self == Heading.EAST:
            return ">"
        if self == Heading.SOUTH:
            return "v"
        if self == Heading.WEST:
            return "<"


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    STRAIGHT = 2


class Maze:
    def __init__(self, file_name="test_input.txt"):
        self.paths = []
        self.start = Vector2(0, 0)
        self.exit = Vector2(0, 0)
        self.parse_input(file_name)
        self.player_pos = self.start
        self.player_heading = Heading.EAST
        self.trails = []
        self.lowest_cost = 0

    def parse_input(self, file_name):
        with open(file_name, "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == ".":
                        self.paths.append(Vector2(x, y))
                    elif char == "E":
                        self.exit = Vector2(x, y)
                    elif char == "S":
                        self.start = (Vector2(x, y))

    def see_ahead(self) -> list:
        directions = []

        if self.player_pos + self.player_heading.turn_ccw().value in self.paths:
            directions.append(Direction.LEFT)
        if self.player_pos + self.player_heading.value in self.paths:
            directions.append(Direction.STRAIGHT)
        if self.player_pos + self.player_heading.turn_cw().value in self.paths:
            directions.append(Direction.RIGHT)

        return directions

    def create_trail(self):
        trail = {}
        cost = 0
        self.player_pos = self.start
        self.player_heading = Heading.EAST
        directions = self.see_ahead()

        while len(directions) > 0 and not self.player_pos in trail.keys():
            trail[self.player_pos] = self.player_heading
            # go left
            if Direction.LEFT in directions:
                cost += 1001
                self.player_heading = self.player_heading.turn_ccw()
                self.player_pos += self.player_heading.value
            # go straight
            elif Direction.STRAIGHT in directions:
                cost += 1
                self.player_pos += self.player_heading.value
            # go right
            elif Direction.RIGHT in directions:
                cost += 1001
                self.player_heading = self.player_heading.turn_cw()
                self.player_pos += self.player_heading.value

            else:
                break

            directions = self.see_ahead()

        self.trails.append(trail)

    def __str__(self):
        out = ""
        max_x = max([path.x for path in self.paths])
        max_y = max([path.y for path in self.paths])

        for y in range(max_y + 2):
            for x in range(max_x + 2):

                location = Vector2(x, y)

                if len(self.trails) > 0 and location in self.trails[-1]:
                    out += self.trails[-1][location].__str__()

                elif location == self.player_pos:
                    out += self.player_heading.__str__()
                elif location in self.paths:
                    out += "."
                elif location == self.start:
                    out += "S"
                elif location == self.exit:
                    out += "E"

                else:
                    out += "#"
            out += "\n"
        return out


if __name__ == "__main__":

    maze = Maze()

    print(maze)
    print(maze.create_trail())
    print(maze)

    # path1 = Path(Vector2(12, 13))
    # path2 = Exit(Vector2(12, 13))

    # my_list = [path1]

    # print(path2 in my_list)
