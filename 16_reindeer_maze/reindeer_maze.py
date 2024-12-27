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
    def __init__(self, pos: Vector2, heading: Heading, edges: dict, trail: dict, cost: int, previous: 'Node'):
        self.pos = pos  # pos = unique identifier of a node
        self.heading = heading
        self.previous = previous
        self.edges = edges
        self.trail = trail
        self.cost = cost

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.pos == other.pos
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
        self.root_node = None
        self.nodes = []
        self.parse_input(file_name)
        self.create_root()
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
        edges = {}
        for direction in directions:
            edges[direction] = None
        print(f"initial brnaches: {edges}")
        self.root_node = Node(self.start, Heading.EAST, edges, {}, 0, None)
        self.nodes.append(self.root_node)

    def see_ahead(self, player_pos: Vector2, player_heading: Heading) -> list:
        directions = []
        if player_pos + player_heading.turn_ccw().value in self.paths:
            directions.append(Direction.LEFT)
        if player_pos + player_heading.value in self.paths:
            directions.append(Direction.STRAIGHT)
        if player_pos + player_heading.turn_cw().value in self.paths:
            directions.append(Direction.RIGHT)
        return directions

    def extend_branch(self, node: Node, first_direction: Direction) -> Node:
        """follows a path and returns the next node with it's cost"""
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

            # if exit is reached -> exit node
            if player_pos == self.exit:
                exit = Node(player_pos, player_heading, {}, trail, cost, node)
                self.exit_nodes.append(exit)
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
        queue.append(self.root_node)
        steps = 0
        while len(queue) > 0 and len(self.exit_nodes) < 1:
            steps += 1
            print(f"queue len: {len(queue)}")
            # sort queue
            queue.sort()
            # get cheapest node
            current_node = queue.pop(0)
            self.nodes.append(current_node)
            print(f"processing node: {steps}")
            for edge in current_node.edges:
                new_node = self.extend_branch(
                    current_node, edge)

                # ignore dead ends and exit nodes
                if new_node == None:
                    continue

                print(f"_____\nnew node: {new_node}")
                self.trail = new_node.trail
                print(self)

                # if node is in queue, replace with cheaper node
                if new_node in queue:
                    index = queue.index(new_node)
                    if new_node < queue[index]:
                        print("fond a smaller way to the same node")
                        queue.pop(index)
                        queue.append(new_node)
                    continue
                # ignore if node was already processed
                elif new_node in self.nodes:
                    print("node already processed")
                    continue

                queue.append(new_node)

    def print_cheapest(self):
        if len(self.exit_nodes) == 0:
            print(self)
            print("no exit node")
            return

        min_exit = min(self.exit_nodes)
        self.trail = min_exit.trail
        print(self)
        print(f"cost: {min_exit.cost}")

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

    maze.dijkstra()
    maze.print_cheapest()
