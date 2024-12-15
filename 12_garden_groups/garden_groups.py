import copy


def get_input(file_name="12_garden_groups/test_input.txt"):
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


class Region:
    def __init__(self, label, initial_plot: Plot, map: list):
        self.label = label
        self.plots = []
        self.perimeter = []
        self.plots.append(initial_plot)
        self.grow_region(map)
        self.build_perimeter()

    def add_plot(self, plot: Plot):
        self.plots.append(plot)

    def grow_region(self, map: list):
        initial_plot = [self.plots[0]]
        self.grow_step(initial_plot, map)

    def grow_step(self, plots: Plot, map: list):
        for p in plots:
            map[p.y][p.x] = "."
            next_plots = self.get_adjacents(p, map)
            self.plots.extend(next_plots)
            self.grow_step(next_plots, map)

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

    def get_perimeter(self, plot: Plot):
        adjacent = []
        # north
        adjacent.append(Plot(plot.x, plot.y - 1))
        # east
        adjacent.append(Plot(plot.x - 1, plot.y))
        # south
        adjacent.append(Plot(plot.x, plot.y + 1))
        # west
        adjacent.append(Plot(plot.x + 1, plot.y))

        to_remove = []
        for p in adjacent:
            if p in self.plots:
                to_remove.append(p)

        for p in to_remove:
            adjacent.remove(p)

        return adjacent

    def build_perimeter(self):
        for p in self.plots:
            self.perimeter.extend(self.get_perimeter(p))

    def get_price(self):
        return len(self.plots) * len(self.perimeter)

    def __str__(self):
        max_x = 0
        max_y = 0
        min_x = self.plots[0].x
        min_y = self.plots[0].y

        out = ""
        for p in self.plots + self.perimeter:
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
                elif Plot(x, y) in self.perimeter:
                    out += "#"
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
    input = get_input("12_garden_groups/input.txt")
    # input = get_input()

    regions = get_regions(input)

    index = 0

    print(f"region0: \n{regions[index]}plots: {
          len(regions[index].plots)} perimeters: {len(regions[index].perimeter)} cost: {regions[index].get_price()}")

    print(sum([r.get_price() for r in regions]))
