import re


class Vector2:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other: object):
        if not isinstance(other, Vector2):
            return self
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other: object):
        if isinstance(other, int):
            return Vector2(self.x * other, self.y * other)
        return self

    def __mod__(self, operator: int):
        return Vector2(self.x % operator, self.y % operator)

    def to_tuple(self):
        return (self.x, self.y)


class Robot:
    def __init__(self, pos: Vector2, vel: Vector2):
        self.pos = pos
        self.vel = vel

    def tick(self, size_x: int, size_y: int):
        self.pos += self.vel
        self.pos = Vector2(self.pos.x % size_x, self.pos.y % size_y)

    def shift_ticks(self, ticks: int, size_x: int, size_y: int):
        self.pos += self.vel * ticks
        self.pos = Vector2(self.pos.x % size_x, self.pos.y % size_y)

    def __str__(self):
        return f"({self.pos.x},{self.pos.y})"


class Room:
    def __init__(self, size_x: int, size_y: int, robots: list):
        self.size_x = size_x
        self.size_y = size_y
        self.robots = robots
        self.ticks_passed = 0
        self.min_noises_factor = []

    def tick(self):
        self.ticks_passed += 1
        for robot in self.robots:
            robot.tick(self.size_x, self.size_y)

    def shift_time(self, ticks: int):
        self.ticks_passed = ticks
        for robot in self.robots:
            robot.shift_ticks(ticks, self.size_x, self.size_y)

    def locate_robots(self):
        locations = {}
        for robot in self.robots:
            if robot.pos.to_tuple() in locations.keys():
                locations[robot.pos.to_tuple()] += 1
            else:
                locations[robot.pos.to_tuple()] = 1
        return locations

    def get_safety_factor(self):
        locations = self.locate_robots()
        sum_nw = 0
        sum_ne = 0
        sum_sw = 0
        sum_se = 0
        for loc in locations.keys():
            if loc[0] < self.size_x//2 and loc[1] < self.size_y//2:
                sum_nw += locations[loc]
            if loc[0] > self.size_x//2 and loc[1] < self.size_y//2:
                sum_ne += locations[loc]
            if loc[0] < self.size_x//2 and loc[1] > self.size_y//2:
                sum_sw += locations[loc]
            if loc[0] > self.size_x//2 and loc[1] > self.size_y//2:
                sum_se += locations[loc]

        return sum_nw * sum_ne * sum_sw * sum_se

    def find_min_noise_factor(self, limit: int, start=0):
        if start > 0:
            self.shift_time(start)
        steps_min_noise = 0
        for i in range(limit):
            self.tick()
            noise_factor = self.get_noise_factor()

            if len(self.min_noises_factor) == 0 or self.min_noises_factor[-1] > noise_factor:
                self.min_noises_factor.append(noise_factor)
                steps_min_noise = self.ticks_passed

            print(f"min noise: {self.min_noises_factor[-1]} at {
                  steps_min_noise} ticks passed: {self.ticks_passed} of {limit}")

        return steps_min_noise

    def get_noise_factor(self):
        locations = self.locate_robots()
        noise_factor = 0
        prev_value = 0
        for y in range(self.size_y):
            for x in range(self.size_x):
                if (x, y) in locations:
                    current_value = locations[(x, y)]
                else:
                    current_value = 0

                if current_value != prev_value:
                    noise_factor += 1

                prev_value = current_value

        return noise_factor

    def __str__(self):
        locations = self.locate_robots()
        out = ""
        out += f"ticks passed: {self.ticks_passed}, Room W:{
            self.size_x} H:{self.size_y}\n"
        for y in range(self.size_y):
            for x in range(self.size_x):
                out += str(locations[(x, y)]) if (x,
                                                  y) in locations.keys() else "."
                self.size_x//2
                out += "|" if x == self.size_x//2 or x == self.size_x//2 - 1 else ""
            out += f"\n{self.size_x * "-" +
                        "--"}\n" if y == self.size_y//2 or y == self.size_y//2 - 1 else "\n"
        out += f"safety factor: {self.get_safety_factor()
                                 }, noise factor {self.get_noise_factor()}"
        return out


def get_robots(file_name="test_input.txt"):
    with open(file_name, "r") as file:
        robots = []
        for row in file:
            pos_x, pos_y, vel_x, vel_y = re.findall("\d+|-\d+", row.strip())
            robots.append(Robot(Vector2(pos_x, pos_y), Vector2(vel_x, vel_y)))
        return robots


if __name__ == "__main__":
    # robots = get_robots()
    # room = Room(11, 7, robots)

    # part 1

    # robots = get_robots("input.txt")
    # room = Room(101, 103, robots)

    # print(room)
    # room.shift_time(100)
    # print(room)

    # part 2
    robots = get_robots("input.txt")
    room = Room(101, 103, robots)

    min_noise_steps = room.find_min_noise_factor(10000)
    print(room.min_noises_factor)

    robots = get_robots("input.txt")
    room = Room(101, 103, robots)

    room.shift_time(min_noise_steps)
    print(room)
