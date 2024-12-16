import copy


def get_input(file_name="test_input.txt"):
    with open(file_name, "r") as f:
        out = []
        for row in f:
            r = []
            for val in row.strip():
                r.append(val)
            out.append(r)
        return out


class Plot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Plot):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Plot({self.x},{self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


class Perimeter(Plot):
    def __init__(self, x, y, label: str):
        super().__init__(x, y)
        self.label = label

    def __repr__(self):
        return f"Perimeter({self.x},{self.y},{self.label})"


class Region:
    def __init__(self, label, initial_plot: Plot, map: list):
        self.label = label
        self.plots = []
        self.perimeters = []
        self.sides = []
        self.plots.append(initial_plot)
        self.build_region(map)
        self.build_perimeters()
        self.build_sides()

    def add_plot(self, plot: Plot):
        self.plots.append(plot)

    def build_region(self, map: list):
        initial_plot = [self.plots[0]]
        self.grow_region(initial_plot, map)

    def grow_region(self, plots: Plot, map: list):
        for p in plots:
            map[p.y][p.x] = "."
            next_plots = self.get_adjacents(p, map)
            self.plots.extend(next_plots)
            self.grow_region(next_plots, map)

    def get_adjacents(self, plot: Plot, map: list):
        adjacent = []
        # north
        if plot.y - 1 >= 0 and map[plot.y - 1][plot.x] == self.label:
            adjacent.append(Plot(plot.x, plot.y - 1))
        # east
        if plot.x - 1 >= 0 and map[plot.y][plot.x - 1] == self.label:
            adjacent.append(Plot(plot.x - 1, plot.y))
        # south
        if plot.y + 1 < len(map) and map[plot.y + 1][plot.x] == self.label:
            adjacent.append(Plot(plot.x, plot.y + 1))
        # west
        if plot.x + 1 < len(map[plot.y]) and map[plot.y][plot.x + 1] == self.label:
            adjacent.append(Plot(plot.x + 1, plot.y))

        for p in adjacent:
            if p in self.plots:
                self.plots.remove(p)

        return adjacent

    def get_perimeters(self, plot: Plot):
        adjacent = []
        # north
        adjacent.append(Perimeter(plot.x, plot.y - 1, "-"))
        # east
        adjacent.append(Perimeter(plot.x - 1, plot.y, "|"))
        # south
        adjacent.append(Perimeter(plot.x, plot.y + 1, "-"))
        # west
        adjacent.append(Perimeter(plot.x + 1, plot.y, "|"))

        to_remove = []
        for p in adjacent:
            if p in self.plots:
                to_remove.append(p)

        for p in to_remove:
            adjacent.remove(p)

        return adjacent

    def build_perimeters(self):
        for p in self.plots:
            self.perimeters.extend(self.get_perimeters(p))

    def build_sides(self):
        perimeters_copy = copy.deepcopy(self.perimeters)
        while len(perimeters_copy) > 0:
            side = [perimeters_copy[0]]
            perimeters_copy.remove(perimeters_copy[0])
            self.grow_side(side, perimeters_copy)
            self.sides.append(side)

    def grow_side(self, side: list, permieters_list: list):
        while True:
            prev = self.get_prev_perimeter(side[0], permieters_list)
            if prev is None:
                break
            side.insert(0, prev)
            permieters_list.remove(prev)
        while True:
            next = self.get_next_perimeter(side[-1], permieters_list)
            if next is None:
                break
            side.append(next)
            permieters_list.remove(next)

    def get_next_perimeter(self, sp: Perimeter, permieters_list: list):
        for p in permieters_list:
            if sp.label == "-" and p.label == "-" and sp.y == p.y and p.x-1 == sp.x:
                return p
            elif sp.label == "|" and p.label == "|" and sp.x == p.x and p.y-1 == sp.y:
                return p
        return None

    def get_prev_perimeter(self, sp: Perimeter, permieters_list: list):
        for p in permieters_list:
            if sp.label == "-" and p.label == "-" and sp.y == p.y and p.x+1 == sp.x:
                return p
            elif sp.label == "|" and p.label == "|" and sp.x == p.x and p.y+1 == sp.y:
                return p
        return None

    def get_price(self):
        return len(self.plots) * len(self.perimeters)

    def get_discount_price(self):
        return len(self.plots) * len(self.sides)

    def __str__(self):
        max_x = 0
        max_y = 0
        min_x = self.plots[0].x
        min_y = self.plots[0].y

        out = ""
        for p in self.plots + self.perimeters:
            if p.x > max_x:
                max_x = p.x
            if p.y > max_y:
                max_y = p.y

            if p.x < min_x:
                min_x = p.x
            if p.y < min_y:
                min_y = p.y

        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                if Plot(x, y) in self.plots:
                    out += self.label
                elif Plot(x, y) in self.perimeters:
                    index = self.perimeters.index(Plot(x, y))
                    out += self.perimeters[index].label
                else:
                    out += "."
            out += "\n"

        return out


def create_region(x, y, map: list):
    label = map[y][x]
    r = Region(label, Plot(x, y), map)
    return r


def get_regions(map: list):
    map = copy.deepcopy(map)
    regions = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == ".":
                continue
            regions.append(create_region(x, y, map))
    return regions


if __name__ == "__main__":
    input = get_input("input.txt")
    # input = get_input("test_input2.txt")
    # input = get_input()

    regions = get_regions(input)

    index = 0

    print(f"region0: \n{regions[index]}plots: {
          len(regions[index].plots)} perimeters: {len(regions[index].perimeters)} cost: {regions[index].get_price()} sides: {len(regions[index].sides)} discount price: {regions[index].get_discount_price()}")

    for i, side in enumerate(regions[index].sides):
        print(f"side {i}: {side}")

    print(f"full price: {sum([r.get_price() for r in regions])}")
    print(f"discount price: {sum([r.get_discount_price() for r in regions])}")
