from enum import Enum
import os
import time
import keyboard


class Vector2:
    def __init__(self, x, y):
        self.__x = int(x)
        self.__y = int(y)

    @property
    def x(self):
        return self.__x

    @property
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

    def __init__(self, pos: list):
        self.pos = pos
        self.symbol = "#" * len(pos)

    def get_objects_ahead(self, direction: Direction, all_objects: list) -> list:
        """Returns all objects ahead in the defined direction"""

        objects_ahead = []
        for position in self.pos:
            ahead_pos = position + direction.value
            for object in all_objects:
                if object != self and isinstance(object, WarehouseObject) and ahead_pos in object.pos:
                    objects_ahead.append(object)
        # filter duplicates
        out = []
        for object in objects_ahead:
            if object not in out:
                out.append(object)

        return out

    def __str__(self):
        return f"pos_x: {self.pos.x()}, pos_y: {self.pos.y()}"


class Box2(WarehouseObject):
    """Is a box or a Robot"""

    def __init__(self, pos):
        super().__init__(pos)
        self.symbol = "[]" if len(pos) > 1 else "@"

    def move(self, direction: Direction, all_objects: list):
        if not self.is_moveable(direction, all_objects):
            return
        self.move_all(direction, all_objects)

    def move_all(self, direction: Direction, all_objects: list):
        objects_ahead = self.get_objects_ahead(direction, all_objects)

        self.pos = [pos + direction.value for pos in self.pos]

        
        for object_ahead in objects_ahead:
            if isinstance(object_ahead, Box2):
                object_ahead.move_all(direction, all_objects)
            

    def is_moveable(self, direction: Direction, all_objects: list) -> bool:
        objects_ahead = self.get_objects_ahead(direction, all_objects)

        if len(objects_ahead) == 0:
            # self.pos = [pos + direction.value for pos in self.pos]
            return True

        is_ahead_moveable = []
        for object_ahead in objects_ahead:
            if isinstance(object_ahead, Box2):
                is_ahead_moveable.append(
                    object_ahead.is_moveable(direction, all_objects))
            else:
                return False

        if not False in is_ahead_moveable:
            return True

        return False


class Warehouse:

    def __init__(self, robot: Box2, wh_objects: WarehouseObject, instructions: list):
        self.robot = robot
        self.wh_objects = wh_objects
        self.instructions = instructions
        self.width = self.find_width()
        self.height = self.find_height()

    def find_width(self):
        return max([max([pos.x for pos in o.pos]) for o in self.wh_objects])

    def find_height(self):
        return max([max([pos.y for pos in o.pos]) for o in self.wh_objects])

    def __str__(self):
        out = ""
        objects_dict = self.objects_to_dict()
        skip_next = False

        for y in range(self.height + 1):
            for x in range(self.width + 1):
                if (x, y) in objects_dict.keys():
                    if len(objects_dict[(x, y)]) > 1:
                        skip_next = True
                    out += objects_dict[(x, y)]
                elif skip_next:
                    skip_next = False
                else:
                    out += "."
            out += "\n"
        return out

    def objects_to_dict(self) -> dict:
        objects_dict = {}
        for o in self.wh_objects:
            objects_dict[o.pos[0].to_tuple()] = o.symbol
        objects_dict[self.robot.pos[0].to_tuple()] = "@"
        return objects_dict

    def run_instructions(self):
        for direction in instructions:
            self.robot.move(direction, self.wh_objects)
            # os.system('cls' if os.name == 'nt' else 'clear')
            print(self)

    def run_by_keys(self):
        print("running by keys")
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self)
            pressed = keyboard.read_key()
            if pressed == "up":
                self.robot.move(Direction.UP, self.wh_objects)
            if pressed == "left":
                self.robot.move(Direction.LEFT, self.wh_objects)
            if pressed == "down":
                self.robot.move(Direction.DOWN, self.wh_objects)
            if pressed == "right":
                self.robot.move(Direction.RIGHT, self.wh_objects)
            if pressed == "x":
                break
            time.sleep(0.15)

    def move_robot(self, direction: Direction):
        self.robot.move(direction, self.wh_objects)

    def get_gps_sum(self):
        sum = 0
        for o in self.wh_objects:
            if isinstance(o, Box2):
                sum += 100 * o.pos[0].y + o.pos[0].x
        return sum


def parse_input(robot: object, wh_objects: list, instructions: list, file_name="test_input.txt"):
    with open(file_name, "r") as file:
        for y, line in enumerate(file):
            for x, cell in enumerate(line.strip()):
                x *= 2
                if cell == "#":
                    wh_objects.append(WarehouseObject(
                        [Vector2(x, y), Vector2(x + 1, y)]))
                elif cell == "O":
                    wh_objects.append(Box2([Vector2(x, y), Vector2(x + 1, y)]))
                elif cell == "@":
                    robot.append(Box2([Vector2(x, y)]))
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
    robot = robot[0]

    wh = Warehouse(robot, wh_objects, instructions)
    # print(wh)
    # print(robot.objects_ahead(Direction.LEFT, wh_objects))
    # wh.move_robot(Direction.LEFT)
    # print(wh)
    # wh.move_robot(Direction.UP)
    # print(wh)
    # wh.move_robot(Direction.LEFT)
    # print(wh)
    # wh.move_robot(Direction.LEFT)
    # print(wh)
    # wh.move_robot(Direction.DOWN)
    # print(wh)
    # wh.run_by_keys()
    wh.run_instructions()
    print(wh.get_gps_sum())
