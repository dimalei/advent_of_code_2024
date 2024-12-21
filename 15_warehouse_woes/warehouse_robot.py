from enum import Enum
import os


class Vector2:
    def __init__(self, x, y):
        self.__x = int(x)
        self.__y = int(y)

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def __add__(self, other: object):
        if isinstance(other, Vector2):
            return Vector2(self.__x + other.__x, self.__y + other.__y)

    def __eq__(self, other: object):
        if isinstance(other, Vector2):
            return self.__x == other.__x and self.__y == other.__y

    def to_tuple(self):
        return (self.__x, self.__y)


class Direction(Enum):
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)


class WarehouseObject:
    """A WO is a wall by default and cant be moved"""
    symbol = "#"

    def __init__(self, pos: Vector2):
        self.pos = pos

    def object_ahead(self, direction: Direction, objects: list) -> 'WarehouseObject':
        ahead_pos = self.pos + direction.value
        for o in objects:
            if isinstance(o, WarehouseObject) and o.pos == ahead_pos:
                return o
        return None

    def __str__(self):
        return f"pos_x: {self.pos.x()}, pos_y: {self.pos.y()}"


class Box(WarehouseObject):
    """A Box can be moved."""
    symbol = "O"

    def __init__(self, pos):
        super().__init__(pos)

    def move(self, direction: Direction, objects: list) -> bool:
        ahead = self.object_ahead(direction, objects)

        if ahead == None:
            self.pos += direction.value
            return True

        if isinstance(ahead, Box):
            if ahead.move(direction, objects):
                self.pos += direction.value
                return True

        return False


class Warehouse:

    def __init__(self, robot: Box, wh_objects: WarehouseObject, instructions: list):
        self.robot = robot
        self.wh_objects = wh_objects
        self.instructions = instructions
        self.width = self.find_width()
        self.height = self.find_height()

    def find_width(self):
        return max([o.pos.x() for o in self.wh_objects])

    def find_height(self):
        return max([o.pos.y() for o in self.wh_objects])

    def __str__(self):
        out = ""
        objects_dict = self.objects_to_dict()

        for y in range(self.width + 1):
            for x in range(self.height + 1):
                if (x, y) in objects_dict.keys():
                    out += objects_dict[(x, y)]
                else:
                    out += "."
            out += "\n"
        return out

    def objects_to_dict(self) -> dict:
        objects_dict = {}
        for o in self.wh_objects:
            objects_dict[o.pos.to_tuple()] = o.symbol
        objects_dict[self.robot.pos.to_tuple()] = "@"
        return objects_dict

    def run_instructions(self):
        for direction in instructions:
            self.robot.move(direction, self.wh_objects)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self)

    def move_robot(self, direction: Direction):
        self.robot.move(direction, self.wh_objects)

    def get_gps_sum(self):
        sum = 0
        for o in self.wh_objects:
            if isinstance(o, Box):
                sum += 100 * o.pos.y() + o.pos.x()
        return sum


def parse_input(robot: object, wh_objects: list, instructions: list, file_name="test_input.txt"):
    with open(file_name, "r") as file:
        for y, line in enumerate(file):
            for x, cell in enumerate(line.strip()):
                if cell == "#":
                    wh_objects.append(WarehouseObject(Vector2(x, y)))
                elif cell == "O":
                    wh_objects.append(Box(Vector2(x, y)))
                elif cell == "@":
                    robot.append(Box(Vector2(x, y)))
                elif cell == "^":
                    instructions.append(Direction.UP)
                elif cell == "v":
                    instructions.append(Direction.DOWN)
                elif cell == "<":
                    instructions.append(Direction.LEFT)
                elif cell == ">":
                    instructions.append(Direction.RIGHT)


if __name__ == "__main__":
    robot = []
    wh_objects = []
    instructions = []

    # parse_input(robot, wh_objects, instructions)
    parse_input(robot, wh_objects, instructions, "input.txt")

    wh = Warehouse(robot[0], wh_objects, instructions)
    print(wh)
    # wh.move_robot(Direction.LEFT)
    wh.run_instructions()
    print(wh.get_gps_sum())
