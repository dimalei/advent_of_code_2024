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

    def build_path(self, trailhead: 'Waypoint', map: list):
        found_wps = self.find_next(map)
        for wp in found_wps:
            if not trailhead.contains(wp):
                self.next_waypoints.append(wp)
        for wp in self.next_waypoints:
            wp.build_path(trailhead, map)

    def build_every_path(self, map: list):
        found_wps = self.find_next(map)
        self.next_waypoints.extend(found_wps)
        for wp in self.next_waypoints:
            wp.build_every_path(map)

    def string_tree(self) -> str:
        out = ""
        out += self.__str__()
        for i, wp in enumerate(self.next_waypoints):
            if i > 0:
                out += f"\n  {self.__str__()}-[{i+1}.branch]->"
            out += wp.string_tree()
        return out

    def distinct_paths_to(self, goal: int) -> int:
        paths = 0
        for wp in self.next_waypoints:
            paths += wp.distinct_paths_to(goal)
        if self.val == goal:
            return 1
        return paths


if __name__ == "__main__":
    # data = get_input()
    data = get_input("input.txt")

    trailheads = []
    trailheads_highpoints = []
    trailheads_distinct_paths = []
    highpoints = []

    for y, line in enumerate(data):
        for x, val in enumerate(line):
            if val == 0:
                trailheads.append(Waypoint(x, y, val))
                trailheads_highpoints.append(0)

    for y, line in enumerate(data):
        for x, val in enumerate(line):
            if val == 9:
                highpoints.append(Waypoint(x, y, val))

    # part 1:
    # for th in trailheads:
    #     th.build_path(th, data)

    # for hp in highpoints:
    #     for i, th in enumerate(trailheads):
    #         if th.contains(hp):
    #             trailheads_highpoints[i] += 1

    # print(trailheads_highpoints)
    # print(sum(trailheads_highpoints))

    # part 2:
    for th in trailheads:
        th.build_every_path(data)

    for i, th in enumerate(trailheads):
        trailheads_distinct_paths.append(th.distinct_paths_to(9))

    print(sum(trailheads_distinct_paths))
