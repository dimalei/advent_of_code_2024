def get_input(file="test_input.txt"):
    with open(file, "r") as f:
        data = []
        for line in f:
            row = []
            for value in line.strip():
                row.append(int(value))
            data.append(row)
        return data


class Waypoint:
    def __init__(self, x: int, y: int, val: int):
        self.x = x
        self.y = y
        self.val = val
        self.next_waypoints = []

    def __str__(self):
        out = ""
        out += "TH:" if self.val == 0 else ""
        out += f"({self.x},{self.y})#{self.val}"
        return out

    def __eq__(self, other: 'Waypoint'):
        return (self.x, self.y) == (other.x, other.y)

    def contains(self, other: 'Waypoint'):
        if self == other:
            return True
        for wp in self.next_waypoints:
            if wp.contains(other):
                return True
        return False

    def add_next(self, next: 'Waypoint'):
        self.next_waypoints.append(next)

    def find_next(self, map: list) -> list:
        next = []
        # north
        new_y = self.y - 1
        if new_y >= 0 and map[new_y][self.x] - 1 == self.val:
            next.append(
                Waypoint(self.x, new_y, map[new_y][self.x]))
        # south
        new_y = self.y + 1
        if new_y < len(map) and map[new_y][self.x] - 1 == self.val:
            next.append(
                Waypoint(self.x, new_y, map[new_y][self.x]))
        # west
        new_x = self.x - 1
        if new_x >= 0 and map[self.y][new_x] - 1 == self.val:
            next.append(
                Waypoint(new_x, self.y, map[self.y][new_x]))
        # east
        new_x = self.x + 1
        if new_x < len(map[self.y]) and map[self.y][new_x] - 1 == self.val:
            next.append(
                Waypoint(new_x, self.y, map[self.y][new_x]))
        
        return next

    def build_path(self, map: list):
        next_wps = self.find_next(map)
        self.next_waypoints.extend(next_wps)
        for wp in self.next_waypoints:
            wp.build_path(map)

    def string_tree(self) -> str:
        out = ""
        out += self.__str__()
        for i, wp in enumerate(self.next_waypoints):
            if i > 0:
                out += f"\n  {self.__str__()}-[{i+1}.branch]->"
            out += wp.string_tree()
        return out


if __name__ == "__main__":
    # data = get_input()
    data = get_input("input.txt")

    trailheads = []
    trailheads_points = []
    highpoints = []

    for y, line in enumerate(data):
        for x, val in enumerate(line):
            if val == 0:
                trailheads.append(Waypoint(x, y, val))
                trailheads_points.append(0)

    for y, line in enumerate(data):
        for x, val in enumerate(line):
            if val == 9:
                highpoints.append(Waypoint(x, y, val))

    for th in trailheads:
        th.build_path(data)

    for hp in highpoints:
        for i, th in enumerate(trailheads):
            if th.contains(hp):
                trailheads_points[i] += 1

    print(trailheads_points)
    print(sum(trailheads_points))

    # print(trailheads[1].string_tree())

    # wp0 = Waypoint(0, 0, 0)
    # wp1 = Waypoint(1, 2, 1)
    # wp2 = Waypoint(3, 4, 2)
    # wp3 = Waypoint(4, 5, 3)
    # wp4 = Waypoint(6, 7, 4)
    # wp5 = Waypoint(8, 10, 5)
    # wp6 = Waypoint(11, 12, 6)

    # wp4.add_next(wp5)
    # wp2.add_next(wp3)
    # wp2.add_next(wp4)
    # wp2.add_next(wp6)
    # wp1.add_next(wp2)
    # wp0.add_next(wp1)

    # print(wp0.string_tree())

    # print(wp1.contains(Waypoint(11, 10, 5)))
