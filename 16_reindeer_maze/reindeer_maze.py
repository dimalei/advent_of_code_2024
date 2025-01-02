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

    def turn_180(self):
        directions = list(Heading)
        current_index = directions.index(self)
        next_index = (current_index + 2) % len(directions)
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
    def __init__(self, pos: Vector2, heading: Heading, edges: dict, trail: dict, cost: int, previous: 'Node'):
        self.pos = pos
        self.heading = heading
        self.previous = previous
        self.edges = edges
        self.trail = trail
        self.cost = cost

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.pos == other.pos and (self.heading == other.heading or self.heading == other.heading.turn_180)
        return False

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.cost < other.cost

    def __repr__(self):
        return f"{self.pos}, {self.heading}, branches: {len(self.edges)}, trail: {len(self.trail)}, cost: {self.cost})"


class Maze:
    def __init__(self, file_name="test_input.txt"):
        self.paths = []
        self.start = None
        self.exit = None
        self.exit_node = None
        self.parse_input(file_name)
        self.start_node = self.create_root()
        self.processed_nodes = []
        self.trail = {}

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

    def create_root(self) -> Node:
        directions = self.see_ahead(self.start, Heading.EAST)
        edges = {}
        for direction in directions:
            edges[direction] = None
        return Node(self.start, Heading.EAST, edges, {}, 0, None)

    def see_ahead(self, player_pos: Vector2, player_heading: Heading) -> list:
        directions = []
        if player_pos + player_heading.turn_ccw().value in self.paths:
            directions.append(Direction.LEFT)
        if player_pos + player_heading.value in self.paths:
            directions.append(Direction.STRAIGHT)
        if player_pos + player_heading.turn_cw().value in self.paths:
            directions.append(Direction.RIGHT)
        return directions

    def grow_branch(self, node: Node, edge_direction: Direction) -> Node:
        """follows a path and returns the next node with it's cost, trail etc"""
        cost = node.cost
        trail = node.trail.copy()
        player_pos = node.pos
        player_heading = node.heading

        # commit to edge direction
        if edge_direction == Direction.LEFT:
            cost += 1001
            player_heading = player_heading.turn_ccw()
        elif edge_direction == Direction.STRAIGHT:
            cost += 1
        elif edge_direction == Direction.RIGHT:
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

            # if exit is reached -> exit node
            if player_pos == self.exit:
                exit = Node(player_pos, player_heading, {}, trail, cost, node)
                self.exit_node = exit
                return exit

            # continue to follow
            directions = self.see_ahead(player_pos, player_heading)
            trail[player_pos] = player_heading

        # dead end
        if len(directions) == 0:
            return None

        # if junction -> new node
        branches = {}
        for direction in directions:
            branches[direction] = None
        return Node(player_pos, player_heading, branches, trail, cost, node)

    def dijkstra(self):
        queue = []
        queue.append(self.start_node)
        steps = 0
        while len(queue) > 0 and self.exit_node == None:
            steps += 1
            # sort queue
            queue.sort()
            # get cheapest node
            current_node = queue.pop(0)
            self.processed_nodes.append(current_node)

            print(f"queue_len: {len(queue):>5} | processing node: {steps:>5}")

            for edge in current_node.edges:
                # create a new node at the end of an edge
                new_node = self.grow_branch(current_node, edge)
                # ignore dead ends and exit nodes
                if new_node == None:
                    continue
                # if node is already in queue, replace with cheaper node
                if new_node in queue:
                    index = queue.index(new_node)
                    if new_node.cost <= queue[index].cost:
                        # print("fond a smaller way to the same node")
                        queue.pop(index)
                        queue.append(new_node)
                    continue
                # if node was already processed, ignore
                elif new_node in self.processed_nodes:
                    continue

                queue.append(new_node)

    def print_cheapest(self):
        if self.exit_node == None:
            print(self)
            print("no exit node")
            return

        self.trail = self.exit_node.trail
        print(self)
        print(f"cost: {self.exit_node.cost}")

    def __str__(self):
        out = ""
        max_x = max([path.x for path in self.paths])
        max_y = max([path.y for path in self.paths])

        for y in range(max_y + 2):
            for x in range(max_x + 2):

                location = Vector2(x, y)

                if len(self.trail) > 0 and location in self.trail.keys():
                    out += self.trail[location].__str__()

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

    # maze = Maze("test_input_2.txt")
    maze = Maze("input.txt")

    maze.dijkstra()
    maze.print_cheapest()
