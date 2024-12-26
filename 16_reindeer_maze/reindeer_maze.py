from enum import Enum

global nodes
nodes = 0

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


class Node:
    def __init__(self, pos: Vector2, heading: Heading, branches: dict, trail: dict, cost: int):
        self.pos = pos
        self.heading = heading
        self.branches = branches
        self.trail = trail
        self.cost = cost

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.cost < other.cost

    def __repr__(self):
        return f"{self.pos}, {self.heading}, branches: {len(self.branches)}, trail: {len(self.trail)}, cost: {self.cost})"


class Maze:
    def __init__(self, file_name="test_input.txt"):
        self.paths = []
        self.start = None
        self.exit = None
        self.parse_input(file_name)
        self.root_node = self.create_root()
        self.trail = {}
        self.exit_nodes = []

    def parse_input(self, file_name):
        with open(file_name, "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == ".":
                        self.paths.append(Vector2(x, y))
                    elif char == "E":
                        self.exit = Vector2(x, y)
                        self.paths.append(self.exit)
                    elif char == "S":
                        self.start = (Vector2(x, y))
                        self.paths.append(self.start)

    def create_root(self):
        directions = self.see_ahead(self.start, Heading.EAST)
        branches = {}
        for direction in directions:
            branches[direction] = None
        return Node(self.start, Heading.EAST, branches, {}, 0)

    def see_ahead(self, player_pos: Vector2, player_heading: Heading) -> list:
        directions = []
        if player_pos + player_heading.turn_ccw().value in self.paths:
            directions.append(Direction.LEFT)
        if player_pos + player_heading.value in self.paths:
            directions.append(Direction.STRAIGHT)
        if player_pos + player_heading.turn_cw().value in self.paths:
            directions.append(Direction.RIGHT)
        return directions

    def extend_node(self, node: Node):
        for branch in node.branches.keys():
            node.branches[branch] = self.extend_branch(node, branch)
            global nodes
            nodes += 1
            print(f"nodes: {nodes}")
            self.extend_node(node.branches[branch])

    def extend_branch(self, node: Node, first_direction: Direction) -> Node:
        cost = node.cost
        trail = node.trail.copy()
        player_pos = node.pos
        player_heading = node.heading

        # commit to first direction
        if first_direction == Direction.LEFT:
            cost += 1001
            player_heading = player_heading.turn_ccw()
        elif first_direction == Direction.STRAIGHT:
            cost += 1
        elif first_direction == Direction.RIGHT:
            cost += 1001
            player_heading = player_heading.turn_cw()

        player_pos += player_heading.value
        trail[player_pos] = player_heading

        # then follow path
        directions = self.see_ahead(player_pos, player_heading)
        while len(directions) == 1:
            if Direction.LEFT in directions:
                cost += 1001
                player_heading = player_heading.turn_ccw()
            # go straight
            elif Direction.STRAIGHT in directions:
                cost += 1
            # go right
            elif Direction.RIGHT in directions:
                cost += 1001
                player_heading = player_heading.turn_cw()

            player_pos += player_heading.value

            # if previous trail is reached -> dead end node
            if player_pos in trail.keys():
                return Node(player_pos, player_heading, {}, trail, cost)

            # if exit is reached -> exit node
            if player_pos == self.exit:
                exit = Node(player_pos, player_heading, {}, trail, cost)
                self.exit_nodes.append(exit)
                return exit

            # continue to follow
            directions = self.see_ahead(player_pos, player_heading)
            trail[player_pos] = player_heading

        # if junction or dead end -> new node
        branches = {}
        for direction in directions:
            branches[direction] = None
        return Node(player_pos, player_heading, branches, trail, cost)

    def __str__(self):
        out = ""
        max_x = max([path.x for path in self.paths])
        max_y = max([path.y for path in self.paths])

        for y in range(max_y + 2):
            for x in range(max_x + 2):

                location = Vector2(x, y)

                if len(self.trail) > 0 and location in self.trail.keys():
                    out += self.trail[location].__str__()

                # elif location == self.player_pos:
                #     out += self.player_heading.__str__()
                elif location == self.start:
                    out += "S"
                elif location == self.exit:
                    out += "E"
                elif location in self.paths:
                    out += "."
                else:
                    out += "#"
            out += "\n"
        return out


if __name__ == "__main__":

    maze = Maze()
    # maze = Maze("input.txt")

    maze.extend_node(maze.root_node)
    cheapest_exit = min(maze.exit_nodes)
    maze.trail = cheapest_exit.trail
    print(maze)
    print(f"min cost: {cheapest_exit.cost}")
